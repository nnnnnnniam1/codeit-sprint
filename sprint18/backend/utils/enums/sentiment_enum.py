from enum import Enum


class SentimentEnum(str, Enum):
    
    VERY_NEGATIVE = "VERY_NEGATIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"
    VERY_POSITIVE = "VERY_POSITIVE"
    
    

    @property
    def label(self) -> str:
        labels = {
            SentimentEnum.VERY_NEGATIVE: "너무 별로예요 😡",
            SentimentEnum.NEGATIVE: "별로예요 🙁",
            SentimentEnum.NEUTRAL: "보통이에요 😐",
            SentimentEnum.POSITIVE: "좋아요 🙂",
            SentimentEnum.VERY_POSITIVE: "너무 좋아요 🤩",
        }
        return labels.get(self.value, "알 수 없음 🤔")
