from bs4 import BeautifulSoup
import urllib3

def get_results():
    resultdict = {}
    urllib3.disable_warnings()
    url = "https://www.reddit.com/r/mechmarket/search?q=Planck&sort=new&restrict_sr=on&t=all"
    response = urllib3.connection_from_url(url)
    r = response.urlopen('GET', url)
    soup = BeautifulSoup(r.data.decode("utf-8"), "html.parser")
    contents = soup.find("div", {"class": "contents"})
    for header in contents.children:
        soup = BeautifulSoup(str(header), "html.parser")
        link = soup.find('a', href=True)
        resultdict[link['href']] = link.text
    print(resultdict)
    return resultdict

get_results()

