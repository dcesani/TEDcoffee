// CONNECTION TO DB

//la creazione della connessione è più lenta.. poi sono più veloci
const mongoose = require('mongoose');
mongoose.Promise = global.Promise;
let isConnected;


require('dotenv').config({ path: './variables_TalksByTitle.env' });

module.exports = connect_to_db = () => {
    if (isConnected) {
        console.log('=> using existing database connection');
        return Promise.resolve();
    }
 
    console.log('=> using new database connection');
    return mongoose.connect(process.env.DB, {dbName: 'TEDcoffeeDB', useNewUrlParser: true, useUnifiedTopology: true}).then(db => {
        isConnected = db.connections[0].readyState;
    });
};

//devo mantenere attiva la connessione all'interno del contesto
//se è già presente allora uso quella altrimenti ne creo un'altra