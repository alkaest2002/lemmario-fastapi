from sqlalchemy.orm import Session

from models__lemmi import Lemma as Tbl
from schemas__lemmi import Lemma as Lemma_schema

from core_enums import PageDirEnum, OrderDirEnum

def get_lemma(db: Session, lemma: str):
	return db.query(Tbl).filter(Tbl.lemma == lemma).first()

def get_lemmi(
	db: Session, 
	offset: int | str | None, 
	order_by: str,
	order_dir: str,
	page_size: int,
	page_dir: str,
):
	# init query
	q = db.query(Tbl)
	# define order clause
	order_by_clause = getattr(Tbl, order_by)
	# add order by to query
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc: q = q.order_by(order_by_clause)
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc: q = q.order_by(order_by_clause)
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc: q = q.order_by(order_by_clause.desc())
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc: q = q.order_by(order_by_clause.desc())
	q = q.order_by(order_by_clause)
	# add offset to query
	if offset:
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc: q = q.where(getattr(Tbl, order_by) >= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc: q = q.where(getattr(Tbl, order_by) >= offset)
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc: q = q.where(getattr(Tbl, order_by) <= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc: q = q.where(getattr(Tbl, order_by) <= offset)
	# retrieve records
	records = q.limit(page_size).all()
	# reverse records if needed
	return records[::-1 if page_dir == PageDirEnum.prev else 1]

def create_lemma(db: Session, lemma: Lemma_schema):
	db.commit()
	db.add(lemma)
	db.refresh(lemma)
	return lemma
