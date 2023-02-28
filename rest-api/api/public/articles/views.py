from typing import List
from api.utils.logger import logger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.db import DatabaseManager, get_database
from api.models.generic import Error
from api.public.articles.models import Article
from api.utils.logger import logger


router = APIRouter()

# asynchronous method exposed on end point,
# returns all by using articles_get_all() from DatabaseManager
# take as many calls as allowed by cpu, while waiting for articles_get_all()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Article]},
        status.HTTP_406_NOT_ACCEPTABLE: {"model": Error},
    },
)
async def get_all_articles(
    db: DatabaseManager=Depends(get_database),
        ) -> List[Article]:
    """Returns all articles.
    """
    articles = await db.articles_get_all()
    if articles:
        logger.info("returning endpoint response for articles_get_all()")
        return JSONResponse(status_code=status.HTTP_200_OK, content=articles)
    
    logger.error("endpoint response error on articles_get_all()")
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="database not ready"
    )

# asynchronous method exposed on end point,
# returns articles by using articles_by_sentence() from
# DatabaseManagertake as many calls as allowed by resources,
# while waiting for articles_by_sentence()


@router.get("/match/sentence/{content_text}",
    responses={
        status.HTTP_200_OK: {"model": Article},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
async def get_articles_by_sentence(
    content_text: str,
    db: DatabaseManager=Depends(get_database)
        ) -> Article:
    """Get articles by providing a sentence, will return
       Articles that have content text exactly matching the sentence.
    """
    articles = await db.articles_by_sentence(content_text=content_text)

    if articles:
        logger.info("returning endpoint response for get_articles_by_sentence()")
        return JSONResponse(status_code=status.HTTP_200_OK, content=articles)

    logger.error("endpoint response error on articles_get_all()")
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"No articles found containing the following: {content_text}",
    )


@router.get("/search/keywords/{keywords}",
    responses={
        status.HTTP_200_OK: {"model": Article},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
async def get_articles_by_keywords(
    keywords: str,
    db: DatabaseManager=Depends(get_database)
        ) -> Article:

    """
       Get articles by providing keywords, will return
       articles where the provided keywords match
       keywords from articles' content text
    """
    articles = await db.articles_by_keywords(keywords=keywords)

    if articles:
        logger.info("returning endpoint response for get_articles_by_keywords()")
        return JSONResponse(status_code=status.HTTP_200_OK, content=articles)

    logger.error("endpoint response error on articles_get_all()")
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"No articles found containing the following: {keywords}",
    )