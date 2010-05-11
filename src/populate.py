from itertools import ifilterfalse
import httplib
import json

# Use Twitter APIs at http://mike.verdone.ca/twitter/, mainly because it's
# a good illustration of a novel yet useful interface into REST APIs
# corresponding to a well-defined URL space.
from twitter.api import Twitter

# Populate a CouchDB instance with a set of data obtained from Twitter.  These
# include the following:
# - The first 100 tweets corresponding to a search term
# - Information about the set of authors for these tweets
# - The set of followers for each of these authors
dbhost = "localhost"
dbport = 5984

# Query to use when finding tweets.
searchquery = "#shotofjaq"

# CouchDB REST API is fairly straightforward so we don't bother with any of
# the various external Python modules for accessing them; httplib is just fine.
def createDatabase(dbconn,dbname):

    # Most straightforward approach is to just try and create the DB; if it
    # already exists we get a 412 back (according to the CouchDB API).
    dbconn.request("PUT","/%s/" % dbname,None)
    r = dbconn.getresponse()
    r.read() # body must be read in order for subsequent HTTP requests to work
    if r.status == 412:
        print "Database %s already exists" % dbname
    elif r.status != 201:
        print "Unable to create database %s: %s" % (dbname,r.reason)

def createDocument(dbconn,dbname,docname,doc):

    dbconn.request("PUT","/%s/%s" % (dbname,docname),json.dumps(doc))
    r = dbconn.getresponse()
    r.read() # body must be read in order for subsequent HTTP requests to work
    if r.status == 409:
        print "Version conflict detected for document %s" % (docname)
    elif r.status == 201:
        print "Document %s created" % docname
    elif r.status == 202:
        print "Document %s created" % docname
    else:
        print "Unable to create document %s: %s" % (docname,r.reason)

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

if __name__ == "__main__":

    search = Twitter(domain="search.twitter.com")
    searchresults = search.search(q=searchquery,rpp=100)
    tweets = searchresults["results"]

    conn = httplib.HTTPConnection(dbhost,dbport)
    tweetdb = "tweets"

    # Make sure our database exists
    createDatabase(conn,tweetdb)

    # Create a doc in the tweet database, one for each distinct tweet
    def createTweet(tweet):
        createDocument(conn,tweetdb,tweet["id"],tweet)
    map(createTweet,tweets)


    authors = unique_everseen([t["from_user"] for t in tweets])
    print " ".join(authors)
