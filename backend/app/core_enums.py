from enum import Enum


class FieldEnum(str, Enum):
  lemma = "lemma"
  letter = "letter"
  updated = "updated"


class PageDirEnum(str, Enum):
  next = "NEXT"
  prev = "PREV"


class OrderDirEnum(str, Enum):
  asc = "ASC"
  desc = "DESC"
