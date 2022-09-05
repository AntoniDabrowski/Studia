var http = require('http');
const express = require('express');
const multer = require('multer');

const app = express();

// app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');
app.set('views',__dirname + '/views');

app.get('/', (req,res) => {
    res.render('upload')
})

const storage = multer.diskStorage({
    destination: __dirname + "/files",
    filename: 'some_name'
});

const upload = multer({ storage })

app.post('/upload', upload.single('avatar'), (req, res) => {
    console.log(req.file)
    res.send("Udało się")
})

http.createServer(app).listen(3000);
console.log("started");