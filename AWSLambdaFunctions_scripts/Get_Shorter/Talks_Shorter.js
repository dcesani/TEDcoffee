const mongoose = require('mongoose'); //libreria che mi permette di interfacciarmi con MongoDB

//definisco lo schema su MongoDB
const talk_schema = new mongoose.Schema({
    _id: String,
    url: String,
    duration: String
}, { collection: 'TEDcoffee_data' });

module.exports = mongoose.model('talkShorter', talk_schema);

//definizione del modello dati
//mappo i quattro campi dalla collection TEDcoffee_data da MongoDB