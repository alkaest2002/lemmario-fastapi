from sqlalchemy import Column, Integer, String

from database__init_db import Base


class LemmaModel(Base):
	__tablename__ = "lemmi"

	rowid = Column(Integer, primary_key=True)
	lemma = Column(String, unique=True, nullable=False, index=True)
	letter = Column(String, nullable=False)
	definition = Column(String, nullable=False)
	created = Column(Integer, nullable=False)
	updated = Column(Integer, nullable=False)
