from pydantic import BaseModel


class Lemma_base(BaseModel):
	lemma: str
	letter: str
	definition: str
	created: int
	updated: int

class Lemma(Lemma_base):
	rowid: int
	
	class Config:
		orm_mode = True
	
class Lemma_create(Lemma_base):
	pass