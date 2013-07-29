
function f() {
	var e = document.getElementById("idOpponents");
	var strUser = e.options[e.selectedIndex].value;
	var opTotal = document.getElementById("idOpponentTotal");
	var opLast = document.getElementById("idOpponentLast");
        var oppScoreData = JSON.parse(window.sessionStorage.getItem('oppScoreData'));
        var opLastPoints = oppScoreData[e.options[e.selectedIndex].text];

	opTotal.innerHTML = 'Opponent Total Points: '+ strUser;
	opLast.innerHTML = 'Opponent Last Race Points: ' + opLastPoints;
}
