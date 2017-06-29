from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
import lxml.html


url = 'http://example.webscraping.com/places/default/search'
app = QApplication([])
webview = QWebView()
loop = QEventLoop()
webview.loadFinished.connect(loop.quit)
webview.load(url)
loop.exec_()
webview.show()
# html = webview.page().mainFrame().toHtml()
# tree = lxml.html.fromstring(html)
# print tree.cssselect('#result')[0].text_content()
frame = webview.page().mainFrame()
frame.findFirstElement('#search_term').setAttribute('value', '.')
frame.findFirstElement('#page_size option[selected=""]').setPlainText('1000')
frame.findFirstElement('#search').evaluateJavaScript('this.click()')
app.exec_()
# elememts = None
# while not elememts:
#     app.processEvents()
#     elememts = frame.findAllElements('#results a')
# countries = [e.toPlainText().strip() for e in elememts]
# print countries
