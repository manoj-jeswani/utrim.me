




    function copyToClipboard(element) {
  		$(element).select();
  		document.execCommand("copy");
  		$('#cmsg').show();
	}


	

    function showshbtns(element) {
  		$(element).show();
  	
	}	


  


/*



$(document).ready(function(){



if ($('#shortened').css('display') == 'none') {
console.log('yes');
}
else{


console.log('no');

$('html,body').animate({scrollTop: $('#shortened').offset().top});



}




});

*/

