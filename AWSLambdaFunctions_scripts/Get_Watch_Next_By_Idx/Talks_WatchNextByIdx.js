const mongoose = require('mongoose'); //libreria che mi permette di interfacciarmi con MongoDB

//definisco lo schema su MongoDB
const talk_schema = new mongoose.Schema({
    _id: String,
    next_idx: Array,
    next_url: Array
}, { collection: 'TEDcoffee_data' });

module.exports = mongoose.model('WatchNexttalk', talk_schema);

//definizione del modello dati
//mappo i quattro campi dalla collection TEDcoffee_data da MongoDB