const readline = require('line-reader');


let dict = {}
let add = function (d,k){
    if (k in d)
        d[k]+=1;
    else
        d[k]=1;
}

let findMax = function(d){
    var sortable = [];
    for (var item in d) {
        sortable.push([item, d[item]]);
    }
    sortable.sort(function(a, b) {
        return a[1] - b[1];
    });
    let l = sortable.length
    console.log(sortable[l-1][0],sortable[l-1][1])
    console.log(sortable[l-2][0],sortable[l-2][1])
    console.log(sortable[l-3][0],sortable[l-3][1])
}


readline.eachLine('./logs.txt',(line,last)=>{
    add(dict,line.split(' ')[1])
    if (last){
        findMax(dict)
    }
})