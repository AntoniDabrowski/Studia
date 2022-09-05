
const Foo = (function (){
    function Qux(){
        // Private functoin
        console.log("Hello:", this.value)
    }
    function Foo(value){
        this.value = value
    }
    Foo.prototype.Bar = function (){
        Qux.call(this)
    }
    return Foo
})()

var instance1 = new Foo(1)
var instance2 = new Foo(2)

instance1.Bar()
instance2.Bar()

// instance1.Qux() zwraca błąd