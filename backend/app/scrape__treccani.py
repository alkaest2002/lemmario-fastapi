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


class TreccaniScaprer():

  def __init__(self, lemma: str):
    self.lemma = lemma
    self.base_url = "https://www.treccani.it/vocabolario"

  def _process_search_lemma(self, occurences: list[Tag]) -> list[ScrapeSearchSchema]:
    result = []
    for found_lemma in occurences:
      title_element = found_lemma.find("h2", class_="search_preview-title")
      abstract_element = found_lemma.find("div", class_="abstract")
      lemma = clean_text(title_element.text).lower()
      definition = clean_text(abstract_element.getText())
      definition = re.sub("\s\.\.\.\sLeggi\sTutto", "", definition)
      result.append(ScrapeSearchSchema(**dict(lemma=lemma, definition=definition)))
    return result

  def search(self) -> list[ScrapeSearchSchema]:
    page = requests.get(f"{self.base_url}/ricerca/{self.lemma}/")
    soup = BeautifulSoup(page.content, "html.parser")
    occurences = soup.find("div", class_="treccani-container-left_container").find_all(
        "section", class_="module-article-search_preview")
    if len(occurences) > 0:
        return self._process_search_lemma(occurences)
    return []
