#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib3, getopt, sys
from collections import OrderedDict
import time


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
    #have to use OrderedDict because Python dicts before 3.6
    #do not keep order that keys are added
    resultdict = OrderedDict()
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
    if(contents == None):
        print("Invalid subreddit entered")
        sys.exit(2)
    #some python versions don't iterate dictonaries in order of 
    #when each item was added, so we must keep track
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
    #allows us to print out each entry in order
    for key in resultdict:
        print("%s: %s" % (key, resultdict[key]))
    return resultdict

'''
Print a standard usage message when using the parser by itself
'''
def usage_message():
    std_usage = "subreddit_parser [-f] [-s subreddit] [-m sort method] \
[-t search term]"
    print("usage: ")
    print(std_usage)
    print("Option\t\tDefault\t\tExample\t\t\t\tDescription")
    print("'-f'\t\tFalse\t\t-f\t\t\t\tAppend flair to entry title")
    print("'-t'\t\tNone\t\t-t Planck\t\t\tTerm to search for")
    print("'-s'\t\tNone\t\t-s mechmarket\t\t\tSubreddit to search for term")
    print("'-m'\t\tnew\t\t-m  new, -m relevance, -m top\tMethod to use for sorting results")
    print("'-h'\t\tN/A\t\t-h\t\t\t\tPrints this usage message")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfs:t:m:", ["help", "output="])
    except getopt.GetoptError as err:
        print(err)
        usage_message()
        sys.exit(2)
    sort = "new"
    sb = ""
    search = ""
    flair = False
    for opt, arg in opts:
        if opt == "-s":
            sb = arg
        elif opt == "-t":
            search = arg
        elif opt == "-m":
            sort = arg
        elif opt == "-f":
            flair = True
        elif opt == "-h":
            usage_message()
            sys.exit(1)
        else:
            assert False, "unrecognized option"
    fail = False
    if sb == "":
        fail = True
        print("Missing option for subreddit: -s")
    if search == "":
        fail = True
        print("Missing option for search term: -t")
    if fail:
        usage_message()
        sys.exit(2)
    get_results(sb, search, sort, flair)

if __name__ == "__main__":
    main()
