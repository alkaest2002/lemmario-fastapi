from pydantic import BaseModel


class LemmaSchema(BaseModel):
	lemma: str
	definition: str
	

class LemmaORMSchema(LemmaSchema):
	rowid: int
	letter: str
	created: int
	updated: int

	class Config:
		orm_mode = True


class LemmaSearchaMetadataSchema(BaseModel):
	offset: int | str | None = None
	order_by: str | None = None
	order_dir: str | None = None
	page_by: str | None = None
	page_size: int = 5


class LemmaListSchema(BaseModel):
	data: list[LemmaORMSchema]
	metadata: LemmaSearchaMetadataSchema


class LemmaLookupSchema(BaseModel):
	lemma: str
	definition: str


class LemmaSearchSchema(LemmaLookupSchema):
	link: str
