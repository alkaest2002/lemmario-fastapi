import re

def clean_text(lemma: str) -> str:
  lemma = re.sub(r"\t", "", lemma)
  lemma = re.sub(r"\n|\s{2,}", " ", lemma)
  lemma = lemma.strip()
  return lemma