import requests
from typing import *

# https://github.com/lukePeavey/quotable
class QuoteHttpClient():
  """An HTTP client to make requests to the Quotable API."""
  __API_URL = "http://api.quotable.io/quotes/random"

  def __init__(self) -> None:
    pass

  def GetRandomQuote(self) -> Any:
    """Gets a random quote from quotable in JSON format."""
    return requests.get(self.__API_URL).json()[0]
