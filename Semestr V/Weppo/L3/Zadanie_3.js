


function forEach(a,f){
    for (var i = 0; i<a.length; i++){
        f(a[i])
    }
}

function map(a,f){
    let new_array = []
    forEach(a,_ => {new_array.push(f(_))})
    return new_array
}

function filter(a,f){
    let new_array = []
    forEach(a, _ => {if (f(_)){new_array.push(_)}})
    return new_array
}




var a = [1,2,3,4]

forEach( a, _ => { console.log( _ ) } )
// a.forEach( _ => { console.log( _ ) } )
// [1,2,3,4]
console.log(filter( a, _ => _ < 3 ))
// [1,2]
console.log(map( a, _ => _ * 2 ))
// [2,4,6,8]
