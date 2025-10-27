import os
import io
import requests
import numpy as np
from PIL import Image, ImageOps
import onnxruntime as ort
import streamlit as st


def preprocess_for_mnist(pil_rgb: Image.Image):
  """"
  입력: RGB PIL 이미지 (280x280 캔버스)
  처리:
    1. 흑백 변환
    2. 여백 제거 (손글씨 부분 crop)
    3. 정사각형으로 패딩 (MNIST 입력 형태와 맞춤)
    4. 28x28 크기로 축소 (모델 입력 크기)
    5. 자동 반전 처리 (배경/글자색 판단)
    6. 0~1 정규화 + 모델 입력 형태 (1, 1, 28, 28)
  출력:
    - tensor: 모델 입력용 numpy 배열 (1, 1, 28, 28)
    - vis: 시각화용 확대 이미지 (280x280)
  """
  
  # RGB -> 흑백(grayscale)
  g = pil_rgb.convert("L")
  
  # 여백 자동 crop
  # 이미지 전체 반전 -> 글씨 부분의 bounding box 계산 후 crop
  bbox = ImageOps.invert(g).getbbox()
  if bbox:
    g = g.crop(bbox)
  
  # 정사각형으로 패딩 (글씨를 중앙 정렬)
  max_dim = max(g.size)
  sq = Image.new("L", (max_dim, max_dim), color=255)  # 흰색 배경
  offset = ((max_dim - g.size[0]) // 2, (max_dim - g.size[0]) // 2)
  sq.paste(g, offset)
  
  # 28x28 축소 (MNIST 입력 크기)
  small = sq.resize((28, 28), Image.Resampling.LANCZOS)
  
  # 자동 반전
  # 평균 픽셀값이 어두울 경우, 배경이 검정이므로 반전 수행
  if np.array(small).mean() < 128:
    small = ImageOps.invert(small)
  
  # 0~1 정규화 -> (1, 1, 28, 28)
  arr = np.array(small).astype(np.float32) / 255.0
  arr = 1.0 - arr # 검정선(1)에 가중치가 높게 되도록 반전
  tensor = arr.reshape(1,1,28,28)
  
  # 시각화 이미지
  vis = small.resize((28*10, 28*10), Image.NEAREST)
  return tensor, vis
  