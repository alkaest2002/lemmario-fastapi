from fastapi import APIRouter

from scrape__hoepli import HoepliScaprer


router = APIRouter(prefix="/olivetti",)



@router.get("/search/{lemma}")
async def search_lemma(lemma: str):
	return HoepliScaprer(lemma).search()