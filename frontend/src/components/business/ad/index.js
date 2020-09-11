var inorderTraversal = function(root) {
  const result = [];
  function bianli(node) {
    if (node) {
      bianli(node.left);
      result.push(root.val);
      bianli(node.right);
    }
  }
  bianli(root);
  return result;
};

console.log(inorderTraversal());
