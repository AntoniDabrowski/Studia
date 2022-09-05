function sum(...a){
    var total_sum = 0;
    a.forEach(_ => total_sum+=_)
    return total_sum
}

console.log(sum(1,2,3,4,5))