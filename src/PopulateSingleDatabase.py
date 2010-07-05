from itertools import ifilterfalse
import httplib
import json

# Use Twitter APIs at http://mike.verdone.ca/twitter/, mainly because it's
# a good illustration of a novel yet useful interface into REST APIs
# corresponding to a well-defined URL space.
from twitter.api import Twitter

# Populate a CouchDB instance with a set of data obtained from Twitter.  These
# include the following:
#
# - The first 100 tweets corresponding to a search term
# - Information about the set of authors for these tweets
# - The set of followers for each of these authors
#
# Unlike the prior version of this script we store all information in a single
# database in order to enable CouchDB's view mechanisms.  No need to think
# relationally anymore; we're not correlating relations of data anymore.
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
        return"Database %s already exists" % dbname
    elif r.status == 201:
        return ""
    else:
        return "Unable to create database %s: %s" % (dbname,r.reason)

def createDocument(dbconn,dbname,docname,doc):

    dbconn.request("PUT","/%s/%s" % (dbname,docname),json.dumps(doc))
    r = dbconn.getresponse()
    r.read() # body must be read in order for subsequent HTTP requests to work
    if r.status == 409:
        return "Version conflict detected for document %s" % (docname)
    elif r.status == 201:
        return ""
    else:
        return "Unable to create document %s: %s" % (docname,r.reason)

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

    dbname = "couchdb-twitter"

    search = Twitter(domain="search.twitter.com")
    twitter = Twitter()

    conn = httplib.HTTPConnection(dbhost,dbport)

    # Create the DB before continuing
    createDatabase(conn,dbname)

    searchresults = search.search(q=searchquery,rpp=100)
    tweets = searchresults["results"]
    def createTweet(tweet):
        doc = tweet
        doc['resource'] = 'tweet'
        tmp = createDocument(conn,dbname,"tweet.%s" % tweet["id"],doc)
        return (tweet["id"],tmp)
    tweetmap = dict(map(createTweet,tweets))
    print "Tweets created: %s" % ",".join([str(k) for (k,v) in tweetmap.iteritems() if not v])

    authors = list(unique_everseen([t["from_user"] for t in tweets]))
    def createAuthor(authorname):
        doc = twitter.users.show(id=authorname)
        doc['resource'] = 'author'
        tmp = createDocument(conn,dbname,"author.%s" % authorname,doc)
        return (authorname,tmp)
    authormap = dict(map(createAuthor,authors))
    print "Authors created: %s" % ",".join([k for (k,v) in authormap.iteritems() if not v])

    def getFollowers(authorname):
        doc = dict(ids=twitter.followers.ids(id=authorname))
        doc['resource'] = 'followers'
        doc['screen_name'] = authorname
        tmp = createDocument(conn,dbname,"followers.%s" % authorname,doc)
        return (authorname,tmp)
    followermap = dict(map(getFollowers,authors))
    print "Followers created: %s" % ",".join([k for (k,v) in followermap.iteritems() if not v])
    