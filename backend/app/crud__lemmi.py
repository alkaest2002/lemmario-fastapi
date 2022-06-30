from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models__lemmi import Lemma as TableLemmi
from schemas__lemmi import LemmaBase

from core_enums import PageDirEnum, OrderDirEnum

def get_lemmi(
	db: Session, 
	offset: int | str | None, 
	order_by: str,
	order_dir: str,
	page_dir: str,
	page_size: int,
):
	# init query
	q = db.query(TableLemmi)
	# define field to operate on
	field = getattr(TableLemmi, order_by)
	# add order by to query
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc: q = q.order_by(field)
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc: q = q.order_by(field)
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc: q = q.order_by(field.desc())
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc: q = q.order_by(field.desc())
	# if offset is set
	if offset:
		# add offset clause to query
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc: q = q.where(field >= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc: q = q.where(field >= offset)
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc: q = q.where(field <= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc: q = q.where(field <= offset)
	# retrieve records
	records = q.limit(page_size).all()
	# reverse records if needed
	return records[::-1 if page_dir == PageDirEnum.prev else 1]


def get_lemma(db: Session, lemma: str):
	return db.query(TableLemmi).filter(TableLemmi.lemma == lemma).first()


def create_lemma(db: Session, lemma: LemmaBase):
	data = TableLemmi(**lemma.dict())
	try:
		db.add(data)
		db.commit()
	except IntegrityError:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"word '{lemma.lemma}' is already present in the database")
	return lemma
