import os
import pandas as pd
import numpy as np
from joblib import dump
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
# 1. 데이터 경로

DATA_DIR = os.environ.get("DATA_DIR", './data')
train_path = os.path.join(DATA_DIR, 'mission15_train.csv')

df = pd.read_csv(train_path)

# 2. Feature / Target 분리
X = df.drop(columns=['Performance Index'])
y = df['Performance Index']

# 3. 전처리
num_features = ['Hours Studied', 'Previous Scores', 'Sleep Hours', 'Sample Question Papers Practiced']
category_features = ['Extracurricular Activities']

preprocessor = ColumnTransformer(
  transformers=[
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(handle_unknown="ignore"), category_features)
  ]
)

# 4. 데이터 분할
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"📊 학습 데이터: {X_train.shape}, 검증 데이터: {X_val.shape}")

# 5. 모델
models = {
  'Ridge': {
    'estimator': Pipeline([
      ('preprocess', preprocessor),
      ('model', Ridge())
    ]),
    'param_grid': {
      'model__alpha': [0.01, 0.1, 1.0, 10.0, 100.0],
      'model__solver': ['auto', 'saga']
    }
  },
  'RandomForest': {
    'estimator': Pipeline([
      ('preprocess', preprocessor),
      ('model', RandomForestRegressor(random_state=42))
    ]),
    'param_grid': {
      'model__n_estimators': [100, 200, 300],
      'model__max_depth': [None, 5, 10, 20],
      'model__min_samples_split': [2, 5, 10],
      'model__max_features': ['sqrt', 'log2', None]
    }
  }
}

# 6. 모델 학습 및 RMSE 평가

best_rmse = float('inf')
best_model_name = None
best_model = None


# 한국 표준시 (UTC+9)
KST = timezone(timedelta(hours=9))
timestamp = datetime.now(KST).strftime("%Y%m%d_%H%M%S")


# 결과 저장 폴더 생성(날짜_시간)
SHARED_DIR = os.environ.get("SHARED_DIR", "/app/shared")
save_dir = os.path.join(SHARED_DIR, timestamp)
os.makedirs(save_dir, exist_ok=True)
print(f"📁 결과 저장 경로: {save_dir}")


# 6. 모델 학습 및 RMSE 평가
for name, cfg in models.items():
  print(f'\n🚀 {name} 모델 튜닝 중...')
  grid = GridSearchCV(
    estimator=cfg['estimator'],
    param_grid=cfg['param_grid'],
    scoring='neg_root_mean_squared_error',
    cv=5,
    n_jobs=-1
  )
  
  grid.fit(X_train, y_train)
  rmse = -grid.best_score_
  
  
  # GridSearch 결과 저장
  results_df = pd.DataFrame(grid.cv_results_)
  results_df.to_csv(f"{save_dir}/{name}_gridsearch_results.csv", index=False)

  
  print(f"✅ {name} Best RMSE (CV): {rmse:.4f}")
  print(f"✅ {name} Best Params: {grid.best_params_}")
  
  if rmse < best_rmse:
    best_rmse = rmse
    best_model_name = name
    best_model = grid.best_estimator_
  

# 7. 검증 데이터 최종평가
y_pred = best_model.predict(X_val)
val_rmse = root_mean_squared_error(y_val, y_pred)
print(f"\n🎯 최종 선택 모델: {best_model_name}")
print(f"📉 Validation RMSE: {val_rmse:.4f}")

# 8. 피처 중요도 / 가중치 출력
model = best_model.named_steps['model']
pre = best_model.named_steps['preprocess']
feature_names = pre.get_feature_names_out()

if best_model_name == 'Ridge':
  coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Weight': model.coef_
  }).sort_values(by='Weight', ascending=False)
  
  print("\n📊 Ridge Feature Weights:")
  print(coef_df)
  
  plt.figure(figsize=(8, 4))
  plt.barh(coef_df["Feature"], coef_df["Weight"], color="steelblue")
  plt.title("Ridge Feature Weights (After Tuning)")
  plt.gca().invert_yaxis()
  plt.tight_layout()
  plt.show()

elif best_model_name == 'RandomForest':
  importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': model.feature_importances_
  }).sort_values(by='Importance', ascending=False)
  
  print("\n🌲 RandomForest Feature Importances:")
  print(importance_df)
  
  plt.figure(figsize=(8, 4))
  plt.barh(importance_df["Feature"], importance_df["Importance"], color="forestgreen")
  plt.title("RandomForest Feature Importances (After Tuning)")
  plt.gca().invert_yaxis()
  plt.tight_layout()
  plt.show()
  


# 9. 최종 모델 저장
dump(best_model, f'{save_dir}/model.pkl')
print("💾 model.pkl 저장 완료")
print(f"🏁 Best Model: {best_model_name} (RMSE={val_rmse:.4f})")

