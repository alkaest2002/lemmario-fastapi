import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from schemas__scrape import ScrapeSearchSchema


def clean_text(lemma: str) -> str:
  lemma = re.sub(r"\t", "", lemma)
  lemma = re.sub(r"\n|\s{2,}", " ", lemma)
  lemma = lemma.strip()
  return lemma


class HoepliScaprer():

  def __init__(self, lemma: str):
    self.lemma = lemma
    self.base_url = "https://www.dizionario-italiano.it/dizionario-italiano.php"

  def _process_search_lemma(self, accented_lemma: str, occurences: list[Tag]) -> list[ScrapeSearchSchema]:
    result = []
    definitions = []
    for definition_number, definition in enumerate(occurences, 1):
      cleaned_definition = clean_text(definition.getText())
      if len(occurences) > 1:
        definitions.append(f"({definition_number}) {cleaned_definition}")
      else:
        definitions.append(cleaned_definition)
    accented_lemma = clean_text(accented_lemma).lower()
    definition = "\n".join(definitions)
    definition = f"{accented_lemma} {definition}"
    result.append(ScrapeSearchSchema(**dict(lemma=self.lemma, definition=definition)))
    return result

  def search(self) -> list[ScrapeSearchSchema]:
    page = requests.get(f"{self.base_url}", params=dict(parola=self.lemma))
    soup = BeautifulSoup(page.content, "html.parser")
    lemma_element = soup.find("div", id="myth1")
    occurences = lemma_element.find_all("span", class_="italiano")
    if len(occurences) > 0:
      processed_lemma = lemma_element.find("span", class_="lemma").getText()
      return self._process_search_lemma(processed_lemma, occurences)
    return []