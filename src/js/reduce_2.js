function(keys, values) {

    // Values are the sequence of user names for each tweet author.  We need
    // to return the count of the number of tweets for each distinct ID.
    rv = {};
    for (var i = 0; i < values.length; ++i) {
        
        var val = values[i];
        if (val in rv) { ++rv[val]; }
        else { rv[val] = 1; }
    }
    return rv;
}