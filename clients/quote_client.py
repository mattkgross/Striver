import requests
from typing import *

# https://github.com/lukePeavey/quotable
class QuoteHttpClient():
  apiUrl = "https://api.quotable.io/quotes/random"

  def __init__(self) -> None:
    pass

  def GetRandomQuote(self) -> Any:
    return requests.get(self.apiUrl).json()