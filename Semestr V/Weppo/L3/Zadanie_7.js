function fib1() {
    var _state = 1;
    var memo = [0,1]
    return {
        next : function() {
            memo.push(memo[_state]+memo[_state-1]);
            _state=_state+1
            return {
                value : memo[_state],
                done : false
            }
        }
    }
}

function *fib2() {
    memo = [1,1]
    for(var i=1;true;i++){
        memo.push(memo[i]+memo[i-1])    
        yield memo[i] 
    }
}

var _it1 = fib1();
for ( var _result; _result = _it1.next(), !_result.done; ) {
    console.log( _result.value );
    if ( _result.value >20)
        break;
}


var _it2 = fib2();
for ( var _result; _result = _it2.next(), !_result.done; ) {
    console.log( _result.value );
    if ( _result.value >20)
    break;
}

var iter_1 = {
    [Symbol.iterator]: fib1
}
   
var iter_2 = {
    [Symbol.iterator]: fib2
}

for ( var i of iter_1 ) {
    if (i>20){
        break;
    }
    console.log( i );
}
    
for ( var i of iter_2 ) {
    console.log( i );
    if (i>20){
        break;
    }
}