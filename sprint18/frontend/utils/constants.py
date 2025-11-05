from enum import Enum

class Menu(Enum):
    MOVIE_LIST = ("movie_list", "🎞 영화 목록")
    MOVIE_WRITE = ("movie_write", "➕ 영화 추가")
    # REVIEW_LIST = ("review_list", "🗒 리뷰 전체 보기")
    # REVIEW_WRITE = ("review_write", "✍ 리뷰 작성")
    
    @property
    def key(self) -> str:
        return self.value[0]
    
    @property
    def label(self) -> str:
        return self.value[1]
    
    @classmethod
    def keys(cls) -> list[str]:
        """모든 key 리스트"""
        return [m.key for m in cls]

    @classmethod
    def labels(cls) -> list[str]:
        """모든 label 리스트"""
        return [m.label for m in cls]

    @classmethod
    def label_from_key(cls, key: str) -> str:
        """key로 label 조회"""
        found = next((m.label for m in cls if m.key == key), None)
        return found or "❓ Unknown"