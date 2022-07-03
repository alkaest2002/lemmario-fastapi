from fastapi import APIRouter, Depends

from scrape_lemmi import Scaprer


router = APIRouter(prefix="/scrape",)



@router.get("/search/{lemma}")
async def search_lemma(lemma: str):
	return Scaprer(lemma).scrape_search()


@router.get("/view/{lemma}")
async def lookup_lemma(lemma: str):
	return Scaprer(lemma).scrape_lookup()