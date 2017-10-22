from bs4 import BeautifulSoup
import urllib3

'''
Scans a subreddit for a search with a certain sorting method and 
optionaally appends the flair to the beginning of the title
@param sb - subreddit to search
@param search - search term
@param sort - sorting method, which can be: new, top, relevance
@param flair - whether or not to append the flair to the title 
@return resultdict - dictionary mapping the search result urls to their 
titles
'''
def get_results(sb, search, sort="new", flair=False):
    resultdict = {}
    urllib3.disable_warnings()
    sorts = ["new", "top", "relevance"]
    if "/r/" not in sb:
        sb = "/r/" + sb
    if sort.lower() not in sorts:
        sort = "new"
    url = "https://www.reddit.com%s/\
search?q=%s&sort=%s&restrict_sr=on&t=all" % (sb, search, sort.lower())
    response = urllib3.connection_from_url(url)
    r = response.urlopen('GET', url)
    soup = BeautifulSoup(r.data.decode("utf-8"), "html.parser")
    contents = soup.find("div", {"class": "contents"})
    for header in contents.children:
        soup = BeautifulSoup(str(header), "html.parser")
        srheader = soup.find("header")
        soup =  BeautifulSoup(str(srheader), "html.parser")
        if flair:
            flairt = soup.find("span", {"class": "linkflairlabel"})
            flairt = flairt.text
        link = soup.find('a', href=True)
        if flair:
            resultdict[link['href']] = flairt + " " + link.text
        else:
            resultdict[link['href']] = link.text
    print(resultdict)
    return resultdict

get_results("mechmarket", "Planck", "new")
