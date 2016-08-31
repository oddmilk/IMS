from lxml import html
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.guahao.com/expert/a7944b06-a639-49c9-82da-b8386ffce2a6000').text
tree = html.fromstring(page.content)

# Data we want is contained in the following XPath
# physican name: //*[@id="g-cfg"]/div[1]/section/div[1]/div[2]/h1/strong
# wkp name: //*[@id="g-cfg"]/div[1]/div[3]/ul/li[1]/div[1]/dl/dd/a[1]
HCPNAME = tree.xpath('//*[@id="g-cfg"]/div[1]/section/div[1]/div[2]/h1/strong/text()')
HCPTITLE = tree.xpath('//*[@id="g-cfg"]/div[1]/section/div[1]/div[2]/h1/span/text()')
HCONAME = tree.xpath('//*[@id="card-hospital"]/p[1]/a[1]/text()')
WKPNAME_1 = tree.xpath('//*[@id="card-hospital"]/p[1]/a[2]/text()')
WKPNAME_2 = tree.xpath('//*[@id="card-hospital"]/p[2]/a[1]/text()')
SP = tree.xpath('//*[@id="card-hospital"]/p[2]/a[2]/text()')

test = tree.xpath('//*[@id="g-cfg"]/div[1]/div[3]/ul/li[1]/div[1]/dl/dt/a/@href/text()')
# //*[@id="g-cfg"]/div[1]/div[3]/ul/li[1]/div[1]/dl/dt/a[@href]/text()

html = requests.get('https://www.guahao.com/search/expert?q=精神科&pageNo=1').text
bs = BeautifulSoup(html, "lxml")
HCPNAME = bs.xpath('//*[@id="g-cfg"]/div[1]/section/div[1]/div[2]/h1/strong/text()')

bs.find_all(['dt', 'dd'])

