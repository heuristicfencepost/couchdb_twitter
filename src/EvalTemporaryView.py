import httplib
import json

from optparse import OptionParser

dbhost = "localhost"
dbport = 5984

def eval_view(dbconn,dbname,doc):

    dbconn.request("POST","/%s/_temp_view" % dbname,json.dumps(doc),{"Content-Type": "application/json"})
    r = dbconn.getresponse()
    rv = r.read() # body must be read in order for subsequent HTTP requests to work
    if r.status == 200:
        return (rv,"")
    else:
        return (rv,"Unable to process view: %s" % r.reason)

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-m", "--mapfile", dest="mapfile", help="File containing map function")
    parser.add_option("-r", "--reducefile", dest="reducefile", help="File containing reduce function")
    parser.add_option("-d", "--database", dest="dbname", help="Name of CouchDB database")

    (options, args) = parser.parse_args()

    view = {}

    if not options.dbname:
        print "Must provide a database name"
        exit(1)

    if not options.mapfile:
        print "Must provide at least map file"
        exit(2)

    mapf = open(options.mapfile)
    view["map"] = "\n".join(mapf.readlines())
    mapf.close()

    if options.reducefile:
        reducef = open(options.reducefile)
        view["reduce"] = "\n".join(reducef.readlines())
        reducef.close()

    # Do the POST
    conn = httplib.HTTPConnection(dbhost,dbport)
    (rv,errors) = eval_view(conn,options.dbname,view)

    print rv