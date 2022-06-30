import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from schemas__lemmi import LemmaSearch, LemmaLookup


class Scaprer():

  def __init__(self, lemma: str):
    self.lemma = lemma
    self.url = "https://www.treccani.it/vocabolario"

  def _clean_text(self, text_to_clean: str) -> str:
    cleaned_text = re.sub(r"\t", "", text_to_clean)
    cleaned_text = re.sub(r"\n|\s{2,}", " ", cleaned_text)
    return cleaned_text.strip()

  def _process_search_lemma(self, occurences: list) -> str:
    result = []
    for found_lemma in occurences:
      title_element = found_lemma.find("h2", class_="search_preview-title")
      abstract_element = found_lemma.find("div", class_="abstract")
      definition = self._clean_text(abstract_element.getText())
      definition = re.sub("\s\.\.\.\sLeggi\sTutto", "", definition)
      lemma = self._clean_text(title_element.text).lower()
      lemma = re.sub("\d", "", lemma)
      lemmaWithoutAccents = definition[:len(lemma)]
      link = self._clean_text(abstract_element.find("a")["href"])
      result.append(
        LemmaSearch(**dict(lemma=lemma, lemmaWithoutAccents=lemmaWithoutAccents, link=link, definition=definition))
      )
    return result

  def _process_lookup_lemma(self, found_lemma: Tag) -> LemmaLookup:
    lemma = found_lemma.find("span", class_="tc-title").text
    lemma = self._clean_text(lemma)
    definition = " ".join([ elm.get_text() for elm in found_lemma.findAll("p")[2:] ])
    definition = self._clean_text(definition)
    return LemmaLookup(**dict(lemma=lemma, definition=definition))

  def scrape_search(self) -> list[LemmaSearch]:
    page = requests.get(f"{self.url}/ricerca/{self.lemma}/")
    soup = BeautifulSoup(page.content, "html.parser")
    occurences = soup.find("div", class_="treccani-container-left_container").find_all("section", class_="module-article-search_preview")
    if len(occurences) > 0: 
        return self._process_search_lemma(occurences)
    return []
  
  def scrape_lookup(self) -> list[LemmaLookup]:
    page = requests.get(f"{self.url}/{self.lemma}/")
    soup = BeautifulSoup(page.content, "html.parser")
    occurences = soup.find_all("div", class_="text spiega")
    if len(occurences) == 0: 
      return []
    return self._process_lookup_lemma(occurences[0])