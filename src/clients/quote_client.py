import requests
from typing import *

# https://zenquotes.io
class QuoteHttpClient():
  """An HTTP client to make requests to the ZenQuotes API."""
  __API_URL = "https://zenquotes.io/api/random"

  def __init__(self) -> None:
    pass

  def GetRandomQuote(self) -> Any:
    """Gets a random quote from ZenQuotes in JSON format.
    Returns dict with 'content' and 'author' keys for compatibility."""
    data = requests.get(self.__API_URL).json()[0]
    return {"content": data["q"], "author": data["a"]}
