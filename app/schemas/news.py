from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
from datetime import datetime

class SourceBase(BaseModel):
    name: str
    url: HttpUrl
    is_active: bool = True

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None

class Source(BaseModel):
    id: int
    name: str
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: HttpUrl
    published_at: datetime
    category: Optional[str] = None
    source_id: int

class NewsCreate(NewsBase):
    pass

class News(BaseModel):
    id: int
    title: str
    content: Optional[str]
    url: str
    published_at: datetime
    category: str
    source_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsStats(BaseModel):
    total_news: int
    by_category: Dict[Optional[str], int]
    by_source: Dict[Optional[str], int]
    last_24h: int

    class Config:
        from_attributes = True 