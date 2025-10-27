import os
import io
import json
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image, ImageOps
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils.path import MODEL_DIR, SAVED_IMG_DIR
from utils.download_model import ensure_models_exist
from utils.onnx_runtime import get_runtime_session
from utils.preprocess import preprocess_for_mnist
# from utils import get_session, preprocess_for_mnist, ensure_model


st.set_page_config(page_title="MNIST ONNX 데모", layout="wide")
st.title("✏️ MNIST 손글씨 숫자 인식 (ONNX + Streamlit)")

#### 사이드바: 모델 준비

ensure_models_exist()
AVAILABLE_MODELS = sorted(
  [f for f in os.listdir(MODEL_DIR) if f.endswith(".onnx")]
)
selected_model = st.sidebar.selectbox("🧠 사용할 모델 선택", AVAILABLE_MODELS)
MODEL_PATH = os.path.join(MODEL_DIR, selected_model)
st.sidebar.success(f"✅ 현재 모델: {selected_model}")
model = get_runtime_session(MODEL_PATH)

#### 화면 영역 나누기 2x2 그리드 배치

input_canvas, result = st.columns(2)
gallery, _ = st.columns(2)

SIZE = 280


# 1) 입력 캔버스
if "canvas_key" not in st.session_state:
    st.session_state["canvas_key"] = 0
with input_canvas:
  st.subheader("1) 입력 캔버스")
  bg_color = "#FFF"
  drawing_mode = "freedraw"
  canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=20,
    background_color=bg_color,
    height=SIZE,
    width=SIZE,
    drawing_mode=drawing_mode,
    key=f"canvas_{st.session_state['canvas_key']}"
  )
  st.caption("마우스로 0~9 숫자를 크게 그려주세요")
  
  do_predict = st.button("예측 및 저장", type="primary")

with result:
  st.subheader("2) 추론 및 저장")
  pre_img = None
  probs = None
  pred = None
  
  if do_predict and canvas_result and canvas_result.image_data is not None:
    # 캔버스 ndarray -> PIL
    rgba = (canvas_result.image_data * 255).astype(np.uint8)
    pil_img = Image.fromarray(rgba).convert("RGB")
    
    # MNIST 입력 전처리 (28x28, 1x1x28x28 float32)
    input_tensor, pre_img = preprocess_for_mnist(pil_img)
    st.image(pre_img, caption="전처리된 28x28 이미지", width=280)
    
    # ONNX 실행 (입력/출력 이름 자동 감지)
    input_name = model.get_inputs()[0].name
    output_name = model.get_outputs()[0].name
    logits = model.run([output_name], {input_name: input_tensor})[0]  # (1,10)
    
    # 소프트맥스
    e = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    probs = (e / e.sum(axis=1, keepdims=True))[0] 
    pred = int(np.argmax(probs))
    
    # 막대차트
    df = pd.DataFrame({"label": list(range(10)), "prob": probs})
    st.bar_chart(df, x="label", y="prob", use_container_width=True)
    st.metric("예측 결과", f"{pred}", f"{probs[pred]*100:.1f}%")
    
    
    # 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_name = f"mnist_{timestamp}"
    
    # 저장경로
    base = os.path.join(SAVED_IMG_DIR, save_name)
    
    # 원본 이미지 저장
    pil_img.save(base + ".png")

    # 예측 결과 메타데이터 저장
    meta = {"pred": int(pred), "probs": probs.tolist()}
    with open(base + ".json", "w", encoding="utf-8") as f:
      json.dump(meta, f, ensure_ascii=False, indent=2)
      
    st.success(f"✅ 이미지 저장 완료: saved_images/{save_name}.png")
    st.session_state["canvas_key"] += 1
    st.experimental_rerun()
  else:
    st.warning("캔퍼스에 숫자를 그려주세요!")
    
      
    
# 사진 저장
with gallery:
  st.subheader("이미지 저장소")
  entries = []
  for name in sorted(os.listdir(SAVED_IMG_DIR)):
    if name.endswith(".png"):
      stem = name[:-4]
      entries.append(stem)
      
  if not entries:
    st.info("아직 저장한 이미지가 없습니다.")
  else:
    for stem in reversed(entries):
      img_p = os.path.join(SAVED_IMG_DIR, stem + ".png")
      meta_p = os.path.join(SAVED_IMG_DIR, stem + ".json") 
      cols = st.columns([1, 2])
      with cols[0]:
        st.image(img_p, width=120) 
      with cols[1]:
        st.write(f"**{stem}.png**")
        if os.path.exists(meta_p):
          with open(meta_p, "r", encoding="utf-8") as f:
            meta = json.load(f)
          st.write(f"예측: **{meta.get('pred')}** | 확률 Top: {np}")
        else:
          st.caption('메타 정보 없음')
        