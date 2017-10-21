from bs4 import BeautifulSoup
import urllib3

def get_results(sb, sort, search, flair=False):
    resultdict = {}
    urllib3.disable_warnings()
    if "/r/" not in sb:
        sb = "/r/" + sb
    url = "https://www.reddit.com%s/\
search?q=%s&sort=%s&restrict_sr=on&t=all" % (sb, search, sort)
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

get_results("mechmarket", "new", "Planck")

