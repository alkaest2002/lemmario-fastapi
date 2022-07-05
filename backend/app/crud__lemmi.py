from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from models__lemmi import LemmaModel, LemmaFullTextSerachModel
from schemas__lemmi import LemmaSchema

from core_enums import PageDirEnum, OrderDirEnum


def get_lemmi(db: Session, offset: int | str | None, order_by: str, order_dir: str, page_dir: str, page_size: int) -> list[LemmaModel]:
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


def get_lemma(db: Session, lemma: str) -> LemmaModel:
	return db.query(LemmaModel).filter(LemmaModel.lemma == lemma).first()



def create_lemma(db: Session, lemma: LemmaSchema) -> LemmaModel:
	data = LemmaModel(**lemma.dict())
	db.add(data)
	db.commit()
	db.refresh(data)
	return data


def search_lemma(db: Session, lemma: str, exact: bool) -> LemmaFullTextSerachModel:
	q = db.query(text("highlight(lemmi_fts, 1, '<b>', '</b>') as 'definition'")).filter(LemmaFullTextSerachModel.definition\
		.match(f"{lemma}{'' if exact else '*'}")).order_by(text('rank desc')).limit(20)
	return [LemmaFullTextSerachModel(definition=l) for l in db.execute(q).scalars().all()]


def delete_lemma(db: Session, lemma_id: int) -> LemmaModel:
	lemma_to_delete = db.query(LemmaModel).filter(LemmaModel.rowid == lemma_id).first()
	if not lemma_to_delete:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found.")
	db.delete(lemma_to_delete)
	db.commit()
	return lemma_to_delete