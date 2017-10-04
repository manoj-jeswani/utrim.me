




    function copyToClipboard(element) {
  		$(element).select();
  		document.execCommand("copy");
  		$('#cmsg').show();
	}


	

    function showshbtns(element) {
  		$(element).show();
  	
	}	


  



/*
#slideshow img { display: none }
#slideshow img.first { display: block }*/


$(document).ready(function(){


$('#shuffle').cycle({ 
    fx:     'shuffle', 
    easing: 'easeOutBack', 
    delay:  -4000 
});

/*if ($('#shortened').css('display') == 'none') {
console.log('yes');
}
else{


console.log('no');

$('html,body').animate({scrollTop: $('#shortened').offset().top});



}

*/


});



