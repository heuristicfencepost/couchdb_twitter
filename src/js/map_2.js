// Feed a sequence of user names for each tweet into the reduce function.
function(doc) {

    if (doc.resource == "tweet") {

        emit(doc.from_user,1);
    }
}