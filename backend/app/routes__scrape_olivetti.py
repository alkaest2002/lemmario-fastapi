from fastapi import APIRouter

from scrape__olivetti import OlivettiScaprer


router = APIRouter(prefix="/olivetti",)



@router.get("/search/{lemma}")
async def search_lemma(lemma: str):
	return OlivettiScaprer(lemma).search()