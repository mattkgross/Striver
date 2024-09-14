from  clients.quote_client import QuoteHttpClient

quoteClient: QuoteHttpClient = QuoteHttpClient()
quote = quoteClient.GetRandomQuote()
quoteText = f"{quote['content']}\n - {quote['author']}"
print(quoteText)