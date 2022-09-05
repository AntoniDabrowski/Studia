function fib_rec(n){
    if (n==0 || n==1){
        return 1;
    }
    return fib_rec(n-2)+fib_rec(n-1)
}

function fib_iter(n){
    if (n==0 || n==1){
        return 1;
    }
    var first = 1;
    var second = 1;
    var temp;
    for(let i = 2;i<=n;i++){
        temp = first;
        first = second;
        second += temp;
    }
    return second;
}

function fib(n){
    if (n==0 || n==1){
        return 1;
    }
    return fib(n-2)+fib(n-1)
}

function memoize(fn) {
    var cache = {};
    
    return function(n) {
        if ( n in cache ) {
            return cache[n]
        } else {
            var result = fn(n);
            cache[n] = result;
            return result;
        }
    }
}
var fib = memoize(fib);

t = new Date();
var start = new Date().getTime();
var elapsed = new Date().getTime() - start;
    
function mesure_time(func,n){
    var start = new Date().getTime();
    func(n)
    var elapsed = new Date().getTime() - start;
    return elapsed.toString()
}


for(let i = 30; i<41; i++){
    console.log("fib("+i.toString()+")")
    console.log("test rec: "+mesure_time(fib_rec,i)+" ms")
    console.log("test iter: "+mesure_time(fib_iter,i)+" ms")
    console.log("test memo: "+mesure_time(fib,i)+" ms")
}

// for(let i = 30; i<41; i++){
//     console.log("fib("+i.toString()+")")
//     console.log("test rec: "+mesure_time(fib_rec,i)+" ms")
//     console.log("test iter: "+mesure_time(fib_iter,i)+" ms")
//     console.log("test memo: "+mesure_time(fib,i)+" ms")
// }