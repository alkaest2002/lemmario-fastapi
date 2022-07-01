from sqlalchemy import Column, Integer, String

from database__init_db import Base


class Lemma(Base):
	__tablename__ = "lemmi"

	rowid = Column(Integer, primary_key=True)
	lemma = Column(String, unique=True, index=True)
	letter = Column(String)
	definition = Column(String)
	created = Column(Integer)
	updated = Column(Integer)
