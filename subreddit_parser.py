from bs4 import BeautifulSoup
import urllib3
from collections import OrderedDict

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
    #have to use OrderedDict because Python dicts before 3.7
    #do not keep order that keys are added
    resultdict = OrderedDict()
    #TODO make the connection secure so I don't have to do this
    urllib3.disable_warnings()
    sorts = ["new", "top", "relevance"] #three sorting options for Reddit search
    #properly format this for url construction
    if "/r/" not in sb:
        sb = "/r/" + sb
    #can't have spaces in URL
    if " " in search:
        search = search.replace(" ", "+")
    #default to new sorting if invalid sort is provided
    if sort.lower() not in sorts:
        sort = "new"
    #construct the URL
    url = "https://www.reddit.com%s/\
search?q=%s&sort=%s&restrict_sr=on&t=all" % (sb, search, sort.lower())
    #get HTML to parse and initialize parser
    response = urllib3.connection_from_url(url)
    r = response.urlopen('GET', url)
    soup = BeautifulSoup(r.data.decode("utf-8"), "html.parser")
    #find contents class
    contents = soup.find("div", {"class": "contents"})
    #some python versions don't iterate dictonaries in order of 
    #when each item was added, so we must keep track
    #index = 0
    #for each entry in the search
    for header in contents.children:
        #specific parsing to make sure that this works for subreddits
        #with custom CSS
        soup = BeautifulSoup(str(header), "html.parser")
        srheader = soup.find("header")
        soup =  BeautifulSoup(str(srheader), "html.parser")
        #get the flair if the user requested it
        if flair:
            flairt = soup.find("span", {"class": "linkflairlabel"})
            if flairt != None:
                flairt = flairt.text
        #get the part of the entry that contains the link and title
        link = soup.find('a', href=True)
        #prepend the flair to the title if requested or don't otherwise
        if flair and flairt != None:
            resultdict[link['href']] = flairt + " " + link.text
        else:
            resultdict[link['href']] = link.text
        #index += 1
    #allows us to print out each entry in order
    # for key in sorted(resultdict, key=lambda k: resultdict[k][1]):
       # print("%s: %s" % (key, resultdict[key]))
    for key in resultdict:
        print("%s: %s" % (key, resultdict[key]))
    return resultdict

#test run
get_results("mechmarket", "Planck", "new")
