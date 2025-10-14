# Dockerfile - 연구자1
FROM python:3.11-slim

# 환경 변수 설정
# PYTHONDONTWRITEBYTECODE=1 : .pyc 캐시 파일 생성 방지
# PYTHONUNBUFFERED=1 : 로그 출력 버퍼링 없이 즉시 표시
# DATA_DIR : 학습 데이터가 위치할 디렉토리 경로
# SHARED_DIR : 학습 결과(model.pkl)를 저장할 공유 디렉토리
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data \
    SHARED_DIR=/app/shared

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 코드 + 데이터 복사
COPY train.py ./train.py
COPY data/ ${DATA_DIR}/

# researcher1의 학습 결과 저장
# COPY shared/ ${SHARED_DIR}


# 실행 시 공유할 폴더 지정
VOLUME ["/app/data", "/app/shared"]

# 컨테이너 실행시 자동 학습
ENTRYPOINT ["python", "train.py"]

# ---------------------------------------------------------
# 1. 이미지 필드
# docker build -t mission15-train .
# 2. 컨테이너 실행
# docker run: 이미지 실행
# --rm: 컨테이너 끝나면 자동 삭제(결과만 남기고 컨테이너 자동 정리)
# -v ~~: 로컬(shared 폴더)을 도커 안 폴더(/app/shared)랑 연결
# docker run --rm -v $(pwd)/shared:/app/shared mission15-train

# 빌드 + dockerhub push
# docker build -t yena1/mission15-train:latest .

# --entrypoint /bin/bash -> train.py 실행하지 말고 쉘로 접속
# docker run -it -v $(pwd)/shared:/app/shared --entrypoint /bin/bash yena1/mission15-train

# ---------------------------------------------------------
