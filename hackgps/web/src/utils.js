function isValid(r, c, gridH, gridW) {
  return !(r < 0 || r >= gridH || c < 0 || c >= gridW);
}

function toNode(r, c, gridH, gridW) {
  return r * gridW + c;
}

function toCoord(node, gridH, gridW) {
  return [(node - node % gridW) / gridW, node % gridW];
}

export { isValid, toNode, toCoord };