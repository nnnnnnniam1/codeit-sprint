# 프로젝트 구조
```
mission17/      
└─ {팀명}_{이름}/       
   ├─ app.py                # Streamlit 메인 앱     
   ├─ utils.py              # 모델 다운로드/로딩, 전처리 유틸     
   ├─ requirements.txt      
   ├─ Dockerfile      
   ├─ .dockerignore       
   ├─ saved_images/         # 저장되는 그린 이미지 + 메타(JSON)       
   └─ README.md             # 실행/배포 방법 요약       

```


# docker build
```
docker build -t yena1/mnist_streamlit:latest .              
docker run -p 8501:8501 -v $(pwd):/app --name yena-streamlit yena1/mnist-streamlit # app.py 변환 확인용

docker start yena-streamlit
docker stop yena-streamlit
```