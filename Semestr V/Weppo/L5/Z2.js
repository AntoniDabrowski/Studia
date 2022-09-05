var http = require('http')
var express = require('express')

var app = express()

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');


app.use(express.urlencoded({extended: true}));

app.get( '/', (req, res) => {
    res.render('index', {imie: "", nazwisko:"", nazwa_zajec:"", punkty:[]});
});


app.post( '/', (req, res) => {
    if (req.body.imie && req.body.nazwisko && req.body.nazwa_zajec) {
        res.redirect('print?imie=${req.body.imie}&nazwisko=${req.body.nazwisko}&nazwa_zajec=${req.body.nazwa_zajec}&zad1=${req.body.zad1}&zad2=${req.body.zad2}&zad3=${req.body.zad3}&zad4=${req.body.zad4}&zad5=${req.body.zad5}&zad6=${req.body.zad6}&zad7=${req.body.zad7}&zad8=${req.body.zad8}&zad9=${req.body.zad9}&zad10=${req.body.zad10}')
    } else {
        res.render('index', {imie: req.body.imie, nazwisko: req.body.nazwisko, nazwa_zajec: req.body.nazwa_zajec, punkty:[req.query.zad1, req.query.zad2, req.query.zad3, req.query.zad4, req.query.zad5, req.query.zad6, req.query.zad7, req.query.zad8, req.query.zad9, req.query.zad10], message: "Nalezy podac imie, nazwisko i nazwe zajec!"});
    }
});

app.get('/print', (req, res) => {
    res.render('print', {imie: req.body.imie, nazwisko: req.body.nazwisko, nazwa_zajec: req.body.nazwa_zajec, punkty:[req.query.zad1, req.query.zad2, req.query.zad3, req.query.zad4, req.query.zad5, req.query.zad6, req.query.zad7, req.query.zad8, req.query.zad9, req.query.zad10]});
});

http.createServer(app).listen(3000);
console.log('started')