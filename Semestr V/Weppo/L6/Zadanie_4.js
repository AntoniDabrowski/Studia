
// https://en.wikipedia.org/wiki/Universally_unique_identifier
const { v4: uuidv4 } = require('uuid');

var http = require('http');
var express = require('express');

var app = express();

const database = new Map();

database.set(uuidv4(), "Sensitive data 1");
database.set(uuidv4(), "Sensitive data 2");
database.set(uuidv4(), "Sensitive data 3");
database.set(uuidv4(), "Sensitive data 4");
database.set(uuidv4(), "Sensitive data 5");


app.get('/', (req,res) => {
    res.end("hello world");
})

app.get("/faktura/:id", (req, res) => {
    // Podatne na ataki:
    //res.end('dynamicznie generowana faktura: ' + req.params.id) 
    
    // Poprawione:
    res.end('dynamicznie generowana faktura: ' + database.get(req.params.id))
    
});

http.createServer(app).listen(3000);

console.log('started');
console.log(database)