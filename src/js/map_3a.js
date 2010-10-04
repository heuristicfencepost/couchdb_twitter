function(doc) {

    // Add keys for each author, keyed by their distinct Twitter ID
    if (doc.resource == "author") {

        emit([doc.id,"name"],doc.screen_name);
    }
    else if (doc.resource == "followers" && doc.screen_name == "damienkatz") {

        // Also add keys for each follower of Damien's, again keyed by
        // Twitter ID.  This will allow us to use CouchDB's grouping
        // functionality to correlate author IDs to followers.
        for (var i = 0; i < doc.ids.length; ++i) {

            emit([doc.ids[i],'is_following'],1);
        }
    }
}
