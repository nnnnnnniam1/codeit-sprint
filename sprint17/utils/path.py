import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 모델 디렉토리
MODEL_DIR = os.path.join(BASE_DIR, "models")

# 저장 이미지 디렉토리
SAVED_IMG_DIR = os.path.join(BASE_DIR, "saved_images")

# 디렉토리 존재 확인 및 자동 생성
for _dir in [MODEL_DIR, SAVED_IMG_DIR]:
  os.makedirs(_dir, exist_ok=True)

