const http = require("http");

(function () {
    const server = http.createServer( (req, res) => {
        res.setHeader("Content-Type", "text/html; charset=utf-8");
        res.setHeader("Content-Disposition", "attachment; filename=example.html");
        res.end("Some text")
    });
    server.listen(3000);
})()