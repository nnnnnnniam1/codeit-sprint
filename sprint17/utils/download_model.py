import os
import requests
from utils.path import MODEL_DIR

# MNIST ONNX 모델 URL
MODEL_URLS = {
    "mnist-7.onnx": "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-7.onnx",
    "mnist-8.onnx": "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-8.onnx",
    "mnist-12.onnx": "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-12.onnx",
}

def ensure_models_exist():
  """models 폴더에 모델이 없으면 자동 다운로드"""
  for name, url in MODEL_URLS.items():
    dst_path = os.path.join(MODEL_DIR, name)
    if not os.path.exists(dst_path):
      print(f" {name} model 다운로드 중...")
      r = requests.get(url)
      
      with open(dst_path, "wb") as f:
        f.write(r.content)
      print(f"{name} model 저장 완료: {dst_path}")