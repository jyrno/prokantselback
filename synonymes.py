import urllib3
from lxml import html

def list_of_synonymes(word) -> list:
    http = urllib3.PoolManager()
    url = 'http://www.eki.ee/dict/sys/index.cgi?Q='+word+'&F=M&C06=et'
    response = http.request('GET', url)
    html_string = str(response.data)
    tree = html.fromstring(html_string)
    values = tree.xpath("//*[@class='x_syn syn']/text()")
    return values
