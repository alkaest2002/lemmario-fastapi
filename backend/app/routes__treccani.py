from fastapi import APIRouter, Depends

from scrape_lemmi import TreccaniScaprer


router = APIRouter(prefix="/treccani",)



@router.get("/search/{lemma}")
async def search_lemma(lemma: str):
	return TreccaniScaprer(lemma).search()


@router.get("/view/{lemma}")
async def lookup_lemma(lemma: str):
	return TreccaniScaprer(lemma).lookup()