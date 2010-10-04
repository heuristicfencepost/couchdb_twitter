function(keys, values, rereduce) {

    if (rereduce) {
        return values.filter(function(obj) { obj != ""; });
    }
    else {

        // Strip keys out of (key,id) tuples
        var truekeys = keys.map(function(arr) { return arr[0][1]; });

        // Build an object containing key-value pairs.  It's a bit like
        // a simplified version of zip without all the error checking and
        // special case handling.'
        var foo = {};
        for (var i = 0; i < truekeys.length; ++i) { foo[truekeys[i]] = values[i]; }

        if ("name" in foo && foo["is_following"] == 1) {

            log("keys: " + keys + ", truekeys: " + truekeys + ", values: " + values);
            return foo["name"];
        }
    }
}