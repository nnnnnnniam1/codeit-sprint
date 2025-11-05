
from transformers import pipeline

from utils.enums.sentiment_enum import SentimentEnum


sentiment_pipeline = pipeline("text-classification",
                              model="tabularisai/multilingual-sentiment-analysis")

def analyze_sentiment(text: str):
    """리뷰 내용 감정 분석 후 sentiment와 score 반환"""
    result = sentiment_pipeline(text)
    # Very Negative, Negative, Neutral, Positive, Very Positive
    label = result[0]['label'].upper().replace(" ", "_")  # 감정 라벨 
    score = result[0]['score']     # 확신도 점수 (0.0 ~ 1.0)
    print(f"analyze_sentiment: label={label}, score={score}")
    
    try:
        sentiment = SentimentEnum[label]
    except KeyError:
        sentiment = SentimentEnum.NEUTRAL   # 예외 발생 시, 중립 처리        
        
    return sentiment, score
    
    
    