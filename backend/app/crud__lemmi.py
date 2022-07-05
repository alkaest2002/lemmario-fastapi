from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import text, update
from sqlalchemy.orm import Session

from models__lemmi import LemmaModel, LemmaFullTextSerachModel
from schemas__lemmi import LemmaSchema

from core_enums import PageDirEnum, OrderDirEnum


def list_lemmi(db: Session, offset: int | str | None, order_by: str, order_dir: str, page_dir: str, page_size: int) -> list[LemmaModel]:
	# init query
	q = db.query(LemmaModel)
	# define field to operate on
	field = getattr(LemmaModel, order_by)
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


def view_lemma(db: Session, lemma_id: int) -> LemmaModel:
	lemma_to_view = db.query(LemmaModel).filter(LemmaModel.rowid == lemma_id).first()
	if not lemma_to_view:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found.")
	return lemma_to_view


def search_lemma(db: Session, lemma: str, exact: bool) -> LemmaFullTextSerachModel:
	q = db.query(text("highlight(lemmi_fts, 1, '<b>', '</b>') as 'definition'")).filter(LemmaFullTextSerachModel.definition\
		.match(f"{lemma}{'' if exact else '*'}")).order_by(text('rank desc')).limit(20)
	return [LemmaFullTextSerachModel(definition=l) for l in db.execute(q).scalars().all()]


def insert_lemma(db: Session, lemma: LemmaSchema) -> LemmaModel:
	lemma_to_insert = LemmaModel(**lemma.dict())
	db.add(lemma_to_insert)
	db.commit()
	db.refresh(lemma_to_insert)
	return lemma_to_insert

def update_lemma(db: Session, lemma_id: int, lemma: LemmaSchema)-> LemmaModel:
	lemma_to_update = db.query(LemmaModel).filter(LemmaModel.rowid == lemma_id).first()
	if not lemma_to_update:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found.")
	for key, value in lemma.__dict__.items():
		setattr(lemma_to_update, key, value) 
	lemma_to_update.updated = datetime.timestamp(datetime.now())
	db.commit()
	db.refresh(lemma_to_update)
	return lemma_to_update

def delete_lemma(db: Session, lemma_id: int) -> LemmaModel:
	lemma_to_delete = db.query(LemmaModel).filter(LemmaModel.rowid == lemma_id).first()
	if not lemma_to_delete:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found.")
	db.delete(lemma_to_delete)
	db.commit()
	return lemma_to_delete