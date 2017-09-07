$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

$(document).ready(function(){
    $("#flip").click(function(){
        $("#panel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#sflip").click(function(){
        $("#spanel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#mflip").click(function(){
        $("#mpanel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#aflip").click(function(){
        $("#apanel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#rflip").click(function(){
        $("#rpanel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#tflip").click(function(){
        $("#tpanel").slideToggle("slow");
    });
});

$(document).ready(function(){
    $("#logo").click(function(){
        $("nav").hide();
    });
});

$(document).ready(function(){
    $("#reveal-nav").click(function(){
        $("nav").show();
    });
});