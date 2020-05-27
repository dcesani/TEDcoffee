const connect_to_db = require('./db_TalksByTitle'); //carico il DB, carica il file db.js

// GET BY TALK HANDLER

const talk = require('./Talks_TalksByTitle'); //carico il modello dati nel file Talk.js

//gestisco l'evento
//evento
//contesto: non lo useremo
//callback: 
module.exports.get_by_title = (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false;//tipicamente si mette a false per evitare problemi
    //altrimenti rimarrebbe in attesa di eventi vuoti
    console.log('Received event:', JSON.stringify(event, null, 2)); //stampo su log
    let body = {} //gestione del payload (contenuto in formato Json stringa): devo fare un parse
    if (event.body) {
        body = JSON.parse(event.body) //prendo la stringa nel body e lo traduco in un JSON vero e proprio
    }
    // set default
    //vedo se è definito il campo tag
    if(!body.title) {
        //errore se tag non è definito
        callback(null, {
                    statusCode: 500,
                    headers: { 'Content-Type': 'text/plain' },
                    body: 'Could not fetch the talks. Title is null.'
        })
    }
    //definisco variabili di default
    //faccio una paginazione: se l'utente non ha definito i parametri non genero un errore ma imposto dei valori di default
    if (!body.doc_per_page) {
        body.doc_per_page = 10
    }
    if (!body.page) {
        body.page = 1
    }
    //devo fare la ricerca
    //invoco funzione (presente in db.js)
    //mi connetto e poi faccio la query
    connect_to_db().then(() => {
        console.log('=> get_all talks');
        //funzione così come faccio le query su mongo DB
        //quando v'è un array, mi restituisce tutti gli oggetti che hanno nell'array almeno un'occorrenza di quel dato
        //in MongoDB non si fanno quasi mai le proiezioni
        //.skip --> sposto l'inizio della ricerca
        //.limit --> imposto un limite alla ricerca
        //per aggiungere più filtri, si mettono nel .find separati da ",". tipicamente sono in AND, devo specificare con il $ se voglio un OR
        
        talk.find({title: {'$regex': body.title, '$options': 'i'}})
            .skip((body.doc_per_page * body.page) - body.doc_per_page)
            .limit(body.doc_per_page)
            .then(talks => {
                    callback(null, {
                        statusCode: 200,
                        body: JSON.stringify(talks)
                    })
                }
            )//traduco il risultato in formato JSON, la serializzo
            .catch(err =>
                callback(null, {
                    statusCode: err.statusCode || 500,
                    headers: { 'Content-Type': 'text/plain' },//in caso di errori, è un TRY-CATCH
                    body: 'Could not fetch the talks.'
                })
            );
    });
};


