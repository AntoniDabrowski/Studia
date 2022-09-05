var express = require("express");
var ejs = require("ejs");
var app = express();
var path = require('path')
var multer = require('multer')


app.set("view engine", "ejs");


var storage = multer.diskStorage({
  destination: function(req, file, callback) {
    callback(null, "./uploads");
  },
  filename: function(req, file, callback) {
    console.log(file);
    callback(null, file.fieldname + "-" + Date.now() + path.extname(file.originalname))
  }
});



app.get("/", function(req, res) {
  res.render("zad01");
});

app.post("/", function(req, res) {
  var upload = multer({
  storage: storage
  }).single('userFile');
  upload(req, res, function(err) {
    res.end('File is uploaded');
  });
});

app.listen(3000, function() {
  console.log("Node.js start");
});