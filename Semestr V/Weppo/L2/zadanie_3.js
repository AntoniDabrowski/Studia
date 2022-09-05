// 1 -> zwraca zerową literę słowa false
console.log((![]+[])[+[]])

// 2 -> zwraca pierwszą literę słowa false
console.log((![]+[])[+!+[]]);

// 3 -> zwraca dziesiątą literę konkatenacji słów false undefined
console.log(([![]]+[][[]])[+!+[]+[+[]]])

// 4 -> zwraca drugą literę słowa false
console.log((![]+[])[!+[]+!+[]]);

// Total
console.log( (![]+[])[+[]]+(![]+[])[+!+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]] );