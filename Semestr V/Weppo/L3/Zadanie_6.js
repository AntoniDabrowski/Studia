function iter(n){
    return function createIterator() {
        var _state = 0;
        return {
            next : function() {
                return {
                    value : _state,
                    done : _state++ >= n
                }
            }
        }
    }
}


var foo1 = {
    [Symbol.iterator] : iter(11)
};

var foo2 = {
    [Symbol.iterator] : iter(5)
};
    
for ( var f of foo1 )
    console.log(f);

for ( var f of foo2 )
    console.log(f);

