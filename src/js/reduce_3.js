function(keys, values, rereduce) {

    // Find the index of the followers array.  The [key,id] format of
    // keys makes this a bit tricky; we could do it with Scala-style
    // pattern matching but we don't have that available at the moment.'
    var idx = 0;
    for (var i = 0; i < keys.length; ++i) {
        
        var tmp = keys[i];
        if (tmp[0] == "followers") { idx = i; }
    }

    var followers = values[idx];

    var rv = [];

    // Check all elements before the followers list
    for (i = 0; i < idx; ++i) {

        if (followers.indexOf(values[i]) != -1) { rv.push(values[i]); }
    }

    // Check all elements after the follows list
    for (i = idx + 1; i < keys.length; ++i) {

        if (followers.indexOf(values[i]) != -1) { rv.push(values[i]); }
    }

    return rv;
}