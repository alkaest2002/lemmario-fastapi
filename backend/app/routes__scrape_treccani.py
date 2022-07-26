from fastapi import APIRouter

from scrape__treccani import TreccaniScaprer


router = APIRouter(prefix="/treccani",)



@router.get("/search/{lemma}")
async def search_lemma(lemma: str):
	return TreccaniScaprer(lemma).search()
