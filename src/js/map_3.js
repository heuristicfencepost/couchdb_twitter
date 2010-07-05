function(doc) {

    // Make the set of followers for the targetted author available to our
    // reduce function
    if (doc.resource == "followers" && doc.screen_name == "shotofjaq") {

        emit("followers",doc.ids);
    }

    // Need to make all authors available as well
    else if (doc.resource == "author") {

        emit(doc.screen_name,doc.id);
    }
}