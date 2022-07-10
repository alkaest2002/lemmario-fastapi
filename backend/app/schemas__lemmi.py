from pydantic import BaseModel
from core_enums import FieldEnum, OrderEnum

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
	filter_by: FieldEnum | None = None
	filter_value: str | None = None
	order_by: FieldEnum | None = None
	order_value: OrderEnum | None = None
	page_dir: str | None = None
	page_size: int = 5
	offset: int | str | None = None


class LemmaListSchema(BaseModel):
	data: list[LemmaORMSchema]
	metadata: LemmaSearchaMetadataSchema


class LemmaLookupSchema(BaseModel):
	lemma: str
	definition: str


class LemmaSearchSchema(LemmaLookupSchema):
	link: str
