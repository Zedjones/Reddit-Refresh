from html.parser import HTMLParser
import urllib3

class SubredditParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if("search-result-group" in tag):
            print(tag)

parser = SubredditParser()
url = "https://www.reddit.com/r/mechmarket/search?q=Planck&sort=new&restrict_sr=on&t=all"
response = urllib3.connection_from_url('https://www.reddit.com/r/mechmarket/\
        search?q=Planck&sort=new&restrict_sr=on&t=all')
r = response.urlopen('GET', url)
parser.feed(r.data.decode('utf-8'))
