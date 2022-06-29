import re
import requests
from bs4 import BeautifulSoup
from schemas__lemmi import LemmaSearch

URL = "https://www.treccani.it/vocabolario/ricerca"

class Scaprer():

  def __init__(self, lemma: str):
    self.lemma = lemma
    self.url = URL

  def _clean_text(self, text_to_clean: str) -> str:
    cleaned_text = re.sub(r"\t", "", text_to_clean)
    cleaned_text = re.sub(r"\n|\s{2,}", " ", cleaned_text)
    return cleaned_text.strip()

  def _process_data(self, occurences)-> str:
    result = []
    for found_lemma in occurences:
      title_elm = found_lemma.find("h2", class_="search_preview-title")
      abstract_elm = found_lemma.find("div", class_="abstract")
      definition = self._clean_text(abstract_elm.getText())
      definition = re.sub("\s\.\.\.\sLeggi\sTutto", "", definition)
      lemma = re.sub("\d", "", self._clean_text(title_elm.text)).lower()
      lemmaWithoutAccents = definition[:len(lemma)]
      link = self._clean_text(abstract_elm.find("a")["href"])
      result.append(
        LemmaSearch(**dict(
          lemma=lemma, 
          lemmaWithoutAccents=lemmaWithoutAccents, 
          link=link, 
          definition=definition)
        ))
    return result

  def scrape(self):
    page = requests.get(f"{URL}/{self.lemma}/")
    soup = BeautifulSoup(page.content, "html.parser")
    occurences = soup.find("div", class_="treccani-container-left_container")\
        .find_all("section", class_="module-article-search_preview")
    if len(occurences) > 0: return self._process_data(occurences)
    return []