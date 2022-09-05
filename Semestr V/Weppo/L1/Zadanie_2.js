function is_divisible(big_num,small_num){
    return big_num % small_num == 0;
  }

function is_ok(num){
    var c = num;
    var divisor;
    var sum = 0;
    while (c!=0){
        divisor = c%10;
        sum += divisor;
        c = (c/10>>0); // !!!
        if (!(is_divisible(num,divisor))){
            return false;
        }
    }
    if (!(is_divisible(num,sum))){
        return false;
    }
    return true;
}

for (let i = 1; i < 100000; i++) {
    if(is_ok(i)){
        console.log(i);
    }
}