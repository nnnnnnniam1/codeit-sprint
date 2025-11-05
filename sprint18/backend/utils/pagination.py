from math import ceil


class Pagination:
    """페이지네이션 클래스"""
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page if page > 0 else 1
        self.page_size = page_size if page_size > 0 else 10
    
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    def set_total(self, total_count: int):
        self.total_count = total_count
        self.total_pages = ceil(total_count / self.page_size) if self.page_size > 0 else 1
        return self
    
    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "total_count": self.total_count
        }