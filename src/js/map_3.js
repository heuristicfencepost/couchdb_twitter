function(doc) {

    if (doc.type == "followers" && doc.screen_name == "shotofjaq") {

        emit("followers",doc.ids);
    }
    else if (doc.type == "author") {

        emit(doc.screen_name,doc.id);
    }
}