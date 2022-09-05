function *fib() {
    memo = [1,1]
    for(var i=1;true;i++){
        memo.push(memo[i]+memo[i-1])    
        yield memo[i] 
    }
}

function* take(it, top) {
    for( let i=0; i<top;i++){
        yield it.next().value
    }
}

// zwróć dokładnie 10 wartości z potencjalnie
// "nieskończonego" iteratora/generatora

for (let num of take( fib(), 10 ) ) {
    console.log(num);
}
    