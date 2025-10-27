FROM python:3.12-slim

# 시스템 패키지
RUN apt-get update && apt-get install -y \
  libglib2.0-0 libsm6 libxext6 libxrender1 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Streamlit 기본 포트
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]

# docker run -p 8501:8501 \
  # -v $(pwd):/app \
  # --name yena-streamlit \
  # yena1/mnist-streamlit \
  # streamlit run app.py --server.runOnSave true