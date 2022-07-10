from datetime import datetime
from time import time
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from models__lemmi import LemmaModel, LemmaFullTextSerachModel
from schemas__lemmi import LemmaSchema

from core_enums import PageDirEnum, OrderEnum

def retrieve_or_die(db: Session, lemma_id: int):
	lemma_to_check = db.query(LemmaModel).filter(LemmaModel.rowid == lemma_id).first()
	if not lemma_to_check:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found.")
	return lemma_to_check


def list_lemmi(
	filter_by: str | None,
	filter_value: str | None,
	order_by: str, 
	order_value: str, 
	page_dir: str, 
	page_size: int,
	offset: int | str | None,
	db: Session
) -> list[LemmaModel]:
	# init query
	q = db.query(LemmaModel)
	# define order_by_field to operate on
	order_by_field = getattr(LemmaModel, order_by)
	# add order by to query
	if page_dir == PageDirEnum.next and order_value == OrderEnum.asc:
		q = q.order_by(order_by_field)
	if page_dir == PageDirEnum.prev and order_value == OrderEnum.desc:
		q = q.order_by(order_by_field)
	if page_dir == PageDirEnum.next and order_value == OrderEnum.desc:
		q = q.order_by(order_by_field.desc())
	if page_dir == PageDirEnum.prev and order_value == OrderEnum.asc:
		q = q.order_by(order_by_field.desc())
	# if offset is set
	if offset:
		# add offset clause to query
		if page_dir == PageDirEnum.next and order_value == OrderEnum.asc:
			q = q.where(order_by_field >= offset)
		if page_dir == PageDirEnum.prev and order_value == OrderEnum.desc:
			q = q.where(order_by_field >= offset)
		if page_dir == PageDirEnum.next and order_value == OrderEnum.desc:
			q = q.where(order_by_field <= offset)
		if page_dir == PageDirEnum.prev and order_value == OrderEnum.asc:
			q = q.where(order_by_field <= offset)
	# if filter is set
	if (filter_by and filter_value):
		# define filter_by_field to operate on
		filter_by_field = getattr(LemmaModel, filter_by)
		print(filter_by_field, filter_value)
		# add filter by to query
		q = q.filter(filter_by_field.startswith(filter_value))
	# retrieve records
	records = q.limit(page_size).all()
	# reverse records if needed
	return records[::-1 if page_dir == PageDirEnum.prev else 1]


def search_lemma(lemma: str, exact: bool, db: Session) -> list[LemmaFullTextSerachModel]:
	q = db.query(text("highlight(lemmi_fts, 1, '<b>', '</b>') as 'definition'")).filter(LemmaFullTextSerachModel.definition\
		.match(f"{lemma}{'' if exact else '*'}")).order_by(text('rank desc')).limit(20)
	return [LemmaFullTextSerachModel(definition=l) for l in db.execute(q).scalars().all()]


def view_lemma(lemma_id: int, db: Session) -> LemmaModel:
	lemma_to_view = retrieve_or_die(db=db, lemma_id=lemma_id)
	return lemma_to_view


def insert_lemma(lemma: LemmaSchema, db: Session) -> LemmaModel:
	lemma_to_insert = LemmaModel(**lemma.dict())
	timestamp = datetime.timestamp(datetime.now())
	lemma_to_insert.letter = lemma.lemma[0].upper()
	lemma_to_insert.created = timestamp
	lemma_to_insert.updated = timestamp
	db.add(lemma_to_insert)
	db.commit()
	db.refresh(lemma_to_insert)
	return lemma_to_insert


def update_lemma(lemma_id: int, lemma: LemmaSchema, db: Session)-> LemmaModel:
	lemma_to_update = retrieve_or_die(db=db, lemma_id=lemma_id)
	for key, value in lemma.__dict__.items():
		setattr(lemma_to_update, key, value) 
	LemmaModel.letter = lemma.lemma[0].upper()
	lemma_to_update.updated = datetime.timestamp(datetime.now())
	db.commit()
	db.refresh(lemma_to_update)
	return lemma_to_update


def delete_lemma(lemma_id: int, db: Session) -> LemmaModel:
	lemma_to_delete = retrieve_or_die(db=db, lemma_id=lemma_id)
	db.delete(lemma_to_delete)
	db.commit()
	return lemma_to_delete