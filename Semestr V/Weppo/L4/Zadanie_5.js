const fs = require('fs')

fs.readFile('./tekst.txt', 'utf8' , (err, data) => {
  if (err) {
    console.error(err)
    return
  }
  console.log(data)
})