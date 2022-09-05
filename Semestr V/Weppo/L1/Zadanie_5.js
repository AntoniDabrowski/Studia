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

// n:                        0, 1, 2, 3, 4, 5,  6,  7
// n-ta liczba Fibonacciego: 1, 1, 2, 3, 5, 8, 13, 21

for(let i = 10; i<44; i++){
    console.time("test rec "+i.toString());
    fib_rec(i);
    console.timeEnd("test rec "+i.toString());
}

for(let i = 44; i==44; i++){
    console.time("test iter "+i.toString());
    fib_iter(i);
    console.timeEnd("test iter "+i.toString());
}