from pydantic import BaseModel

class LemmaBase(BaseModel):
	lemma: str
	letter: str
	definition: str
	created: int
	updated: int

class Lemma(LemmaBase):
	rowid: int
	
	class Config:
		orm_mode = True

class LemmaMetadata(BaseModel):
	offset: int | str | None = None
	order_by: str | None = None
	order_dir: str | None = None
	page_by: str | None = None
	page_size: int = 5

class LemmaOut(BaseModel):
	data: list[Lemma]
	metadata: LemmaMetadata	

class LemmaLookup(BaseModel):
	lemma: str
	definition: str

class LemmaSearch(LemmaLookup):
	link: str

