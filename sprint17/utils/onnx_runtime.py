import onnxruntime as ort
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_runtime_session(model_path: str):
  """ONNX Runtime 세션 캐싱"""
  providers = ort.get_available_providers()
  return ort.InferenceSession(model_path, providers=providers)

