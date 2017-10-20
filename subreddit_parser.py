from bs4 import BeautifulSoup
import urllib3

url = "https://www.reddit.com/r/mechmarket/search?q=Planck&sort=new&restrict_sr=on&t=all"
response = urllib3.connection_from_url('https://www.reddit.com/r/mechmarket/\
        search?q=Planck&sort=new&restrict_sr=on&t=all')
r = response.urlopen('GET', url)
soup = BeautifulSoup(r.data.decode("utf-8"))
mydivs = soup.findAll("div", {"class": "contents"})
for div in mydivs:
    case = BeautifulSoup(str(div.contents))
