from pydantic import BaseModel


class Error(BaseModel):
    """Error reponses schema"""

    detail: str
    status_code: int

    class Config:
        schema_extra = {
            "example": {
                "detail": "MongoDb not ready",
                "status_code": 406,
            }
        }


class Article(BaseModel):

    content: str
    url: str
    label: str
    published_at: str
    headline: str
    author: list

    class Config:
        """Article structure example
        """
        schema_extra = {
            "example": {
        "content": "Teachers in north of England to strike..",
        "url": "https://www.theguardian.com/education/2023...",
        "label": "tens of thousands teachers prepare..",
        "published_at": "2023-02-27T00:00:00",
        "author": "[Sally Weale]"
    }
        }
