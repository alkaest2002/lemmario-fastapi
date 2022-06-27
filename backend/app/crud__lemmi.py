from sqlalchemy.orm import Session

from models__lemmi import Lemma as Tbl
from schemas__lemmi import Lemma as Lemma_schema


def get_lemma(db: Session, lemma: str):
	return db.query(Tbl).filter(Tbl.lemma == lemma).first()

def get_lemmi(db: Session, skip: int = 0, limit: int = 100):
	return db.query(Tbl).offset(skip).limit(limit).all()

def create_lemma(db: Session, lemma: Lemma_schema):
	db.add(lemma)
	db.commit()
	db.refresh(lemma)
	return lemma
