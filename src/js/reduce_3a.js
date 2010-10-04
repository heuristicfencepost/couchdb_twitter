function(keys, values, rereduce) {

    // Make our reduce function safe for rereduce
    if (rereduce) {
        return values
    }
    else {

        // Strip keys out of (key,id) tuples.  Even though we're using
        // a grouping function keys are of the form [Twitter ID, keyname]
        // so we need to take teh second item from whatever we find.
        var truekeys = keys.map(function(arr) { return arr[0][1]; });

        // Build an object containing key-value pairs.  It's a bit like
        // a simplified version of zip without all the error checking and
        // special case handling.'
        var foo = {};
        for (var i = 0; i < truekeys.length; ++i) { foo[truekeys[i]] = values[i]; }

        // If we have a "name" and an "is_following" value of 1 we've found
        // an author who is also following Damien.
        if (("name" in foo) && ("is_following" in foo) && foo["is_following"] == 1) {

            log("keys: " + keys + ", truekeys: " + truekeys + ", values: " + values);
            return foo["name"];
        }
    }
}