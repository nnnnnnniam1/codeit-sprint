
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self):
        """soft delete: deleted_at 필드에 현재 시간 기록"""
        self.deleted_at = datetime.now(timezone.utc)