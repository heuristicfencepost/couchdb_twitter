from itertools import ifilterfalse
import httplib
import json

from twitter.api import Twitter

dbhost = "localhost"
dbport = 5984
conn = httplib.HTTPConnection(dbhost,dbport)

# Borrowed from the itertools docs
def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def createDatabase(name):

    # Most straightforward approach is to just try and create the DB; if it
    # already exists we get a 412 back (according to the CouchDB API).
    conn.request("PUT","/%s/" % name,None)
    r = conn.getresponse()
    data = r.read()
    if r.status == 412:
        print "Database %s already exists" % name
    elif r.status != 201:
        print "Unable to create database %s: %s" % (name,r.reason)

def createDocument(database,name,doc):

    conn.request("PUT","/%s/%s" % (database,name),json.dumps(doc))
    r = conn.getresponse()
    data = r.read()
    if r.status == 409:
        print "Version conflict detected for document %s" % (name)
    elif r.status == 201:
        print "Document %s created" % name
    elif r.status == 202:
        print "Document %s created" % name
    else:
        print "Unable to create document %s: %s" % (name,r.reason)


search = Twitter(domain="search.twitter.com")
searchresults = search.search(q="#shotofjaq",rpp=100)
tweets = searchresults["results"]

# Make sure our database exists
createDatabase("tweets")

# Add some content to aforementioned database
def createTweet(tweet):
    createDocument("tweets",tweet["id"],tweet)
map(createTweet,tweets)


authors = unique_everseen([t["from_user"] for t in tweets])
print " ".join(authors)
