
function initOpponents() {
  var e = document.getElementById("idOpponents");
  var strUser = e.options[e.selectedIndex].value;
  var opTotal = document.getElementById("idOpponentTotal");
  var opLast = document.getElementById("idOpponentLast");
  var oppScoreData = JSON.parse(window.sessionStorage.getItem('oppScoreData'));
  var opPoints = oppScoreData[strUser];

  opTotal.innerHTML = 'Opponent Total Points: '+ opPoints.total;
  opLast.innerHTML = 'Opponent Last Race Points: ' + opPoints.last;
}

function escapeHTML(html) {
  var pre = document.createElement('pre');
  var text = document.createTextNode(html);
  pre.appendChild(text);
  return pre.innerHTML;
}
