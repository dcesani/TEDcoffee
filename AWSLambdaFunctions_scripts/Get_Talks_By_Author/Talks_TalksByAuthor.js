const mongoose = require('mongoose'); //libreria che mi permette di interfacciarmi con MongoDB

//definisco lo schema su MongoDB
const talk_schema = new mongoose.Schema({
    title: String,
    url: String,
    details: String,
    main_spea: String
}, { collection: 'TEDcoffee_data' });

module.exports = mongoose.model('talkByAuthor', talk_schema);

//definizione del modello dati
//mappo i quattro campi dalla collection TEDcoffee_data da MongoDB