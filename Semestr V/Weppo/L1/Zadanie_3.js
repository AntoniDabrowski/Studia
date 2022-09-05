function is_divisible(big_num,small_num){
    return big_num % small_num == 0;
}

function is_prime(num){
    for(let i = 2; i<num; i++){
        if (is_divisible(num,i)){
            return false
        }
    }
    return true
}

for (let i = 2; i < 100000; i++) {
    if(is_prime(i)){
        console.log(i);
    }
  }