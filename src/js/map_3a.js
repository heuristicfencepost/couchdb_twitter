// Feed a sequence of user names for each tweet into the reduce function.
function(doc) {

    if (doc.resource == "author") {

        emit([doc.id,"name"],doc.screen_name);
    }
    else if (doc.resource == "followers" && doc.screen_name == "damienkatz") {

        for (var i = 0; i < doc.ids.length; ++i) {

            emit([doc.ids[i],'is_following'],1);
        }
    }
}
