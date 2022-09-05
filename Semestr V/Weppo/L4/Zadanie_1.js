function Tree(val, left, right) {
    this.left = left;
    this.right = right;
    this.val = val;
}
Tree.prototype[Symbol.iterator] = function* () {
    const queue =  [this];
    while (queue.length > 0){
        node = queue.shift();
        yield node.val;
        if (node.right) 
            queue.push(node.right);
        if (node.left)
            queue.push(node.left);
    }
}
var root = new Tree(1,
    new Tree(2, new Tree(3)), new Tree(4));


for (var e of root) {
    console.log(e);
}
// 1 4 2 3
