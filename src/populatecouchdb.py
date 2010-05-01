from itertools import ifilterfalse

from twitter.api import Twitter

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
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


search = Twitter(domain="search.twitter.com")
tweets = [(t["from_user"],t["from_user_id"],t["id"]) for t in search.search(q="#shotofjaq",rpp=100)["results"]]
authors = unique_everseen([user for (user,user_id,t_id) in tweets])
print " ".join(authors)
