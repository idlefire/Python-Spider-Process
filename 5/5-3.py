from BrowserRender import BrowserRender

br = BrowserRender(show=False)
br.download('http://example.webscraping.com/places/default/search')
br.attr('#search_term', 'value', '.')
br.text('#page_size option[selected=""]', '1000')
br.click('#search')
# while True:
#     br.app.processEvents()
elements = br.wait_load('#results a')
countries = [e.toPlainText().strip() for e in elements]
print countries
