from sqlalchemy.orm import Session

from models__lemmi import Lemma as Tbl
from schemas__lemmi import Lemma as Lemma_schema

from core_enums import PageDirEnum

def get_lemma(db: Session, lemma: str):
	return db.query(Tbl).filter(Tbl.lemma == lemma).first()

def get_lemmi(
	db: Session, 
	offset: int | str | None, 
	page_size: int,
	page_dir: str,
	order_by: str,
):
	q = db.query(Tbl)
	if offset and page_dir == PageDirEnum.next:
		q = q.where(getattr(Tbl, order_by) >= offset)
	if offset and page_dir == PageDirEnum.prev:
		q = q.where(getattr(Tbl, order_by) <= offset)
	if (page_dir == PageDirEnum.next):
		q = q.order_by(getattr(Tbl, order_by))
	if (page_dir == PageDirEnum.prev):
		q = q.order_by(getattr(Tbl, order_by).desc())
	records = q.limit(page_size).all()
	return records[::-1 if page_dir == PageDirEnum.prev else 1]

def create_lemma(db: Session, lemma: Lemma_schema):
	db.commit()
	db.add(lemma)
	db.refresh(lemma)
	return lemma
