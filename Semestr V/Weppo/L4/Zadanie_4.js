const readline = require("readline");
const it = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

it.question("Jak się nazywasz? ", function (name) {
    console.log(`Witaj ${name}`);
    it.close();
});

// Odpalać z poziomu terminala