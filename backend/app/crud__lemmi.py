from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models__lemmi import Lemma
from schemas__lemmi import LemmaBase

from core_enums import PageDirEnum, OrderDirEnum


def get_lemmi(db: Session, offset: int | str | None, order_by: str, order_dir: str, page_dir: str, page_size: int) -> list[Lemma]:
	# init query
	q = db.query(Lemma)
	# define field to operate on
	field = getattr(Lemma, order_by)
	# add order by to query
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc:
		q = q.order_by(field)
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc:
		q = q.order_by(field)
	if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc:
		q = q.order_by(field.desc())
	if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc:
		q = q.order_by(field.desc())
	# if offset is set
	if offset:
		# add offset clause to query
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.asc:
			q = q.where(field >= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.desc:
			q = q.where(field >= offset)
		if page_dir == PageDirEnum.next and order_dir == OrderDirEnum.desc:
			q = q.where(field <= offset)
		if page_dir == PageDirEnum.prev and order_dir == OrderDirEnum.asc:
			q = q.where(field <= offset)
	# retrieve records
	records = q.limit(page_size).all()
	# reverse records if needed
	return records[::-1 if page_dir == PageDirEnum.prev else 1]


def get_lemma(db: Session, lemma: str) -> Lemma:
	return db.query(Lemma).filter(Lemma.lemma == lemma).first()


def create_lemma(db: Session, lemma: LemmaBase) -> Lemma:
	data = Lemma(**lemma.dict())
	db.add(data)
	db.commit()
	return data
