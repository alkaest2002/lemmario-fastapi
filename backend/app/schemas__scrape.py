from pydantic import BaseModel


class ScrapeSearchSchema(BaseModel):
	lemma: str
	definition: str
