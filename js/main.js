//$('.idOpponents').click(
//		function (){
//			alert("hey");
//			window.console.log($('.idOpponents'));
//		});

function f() {
	var e = document.getElementById("idOpponents");
	var strUser = e.options[e.selectedIndex].value;
	var opTotal = document.getElementById("idOpponentTotal");
	var opLast = document.getElementById("idOpponentLast");
	var opLastPoints = document.getElementById(e.options[e.selectedIndex].text).innerHTML;
	
	opTotal.innerHTML = 'Opponent Total Points: '+ strUser;
	opLast.innerHTML = 'Opponent Last Race Points: ' + opLastPoints;
}
