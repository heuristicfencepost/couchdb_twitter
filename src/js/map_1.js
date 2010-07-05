// Generate a basic report on tweet authors.  We'd like to gather a few
// basic facts: who is the author, what language do they write in and
// how many followers do they have.
function(doc) {

    if (doc.resource == "author") {

        emit(doc.id,{name: doc.name, language: doc.lang, followers: doc.followers_count});
    }
}
