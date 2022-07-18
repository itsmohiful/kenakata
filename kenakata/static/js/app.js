// ---------Responsive-navbar-active-animation-----------
function test(){
	var tabsNewAnim = $('#navbarSupportedContent');
	var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
	var activeItemNewAnim = tabsNewAnim.find('.active');
	var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
	var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
	var itemPosNewAnimTop = activeItemNewAnim.position();
	var itemPosNewAnimLeft = activeItemNewAnim.position();
	$(".hori-selector").css({
		"top":itemPosNewAnimTop.top + "px", 
		"left":itemPosNewAnimLeft.left + "px",
		"height": activeWidthNewAnimHeight + "px",
		"width": activeWidthNewAnimWidth + "px"
	});
	$("#navbarSupportedContent").on("click","li",function(e){
		$('#navbarSupportedContent ul li').removeClass("active");
		$(this).addClass('active');
		var activeWidthNewAnimHeight = $(this).innerHeight();
		var activeWidthNewAnimWidth = $(this).innerWidth();
		var itemPosNewAnimTop = $(this).position();
		var itemPosNewAnimLeft = $(this).position();
		$(".hori-selector").css({
			"top":itemPosNewAnimTop.top + "px", 
			"left":itemPosNewAnimLeft.left + "px",
			"height": activeWidthNewAnimHeight + "px",
			"width": activeWidthNewAnimWidth + "px"
		});
	});
}
$(document).ready(function(){
	setTimeout(function(){ test(); });
});
$(window).on('resize', function(){
	setTimeout(function(){ test(); }, 500);
});
$(".navbar-toggler").click(function(){
	$(".navbar-collapse").slideToggle(300);
	setTimeout(function(){ test(); });
});



// --------------add active class-on another-page move----------
jQuery(document).ready(function($){
	// Get current path and find target link
	var path = window.location.pathname.split("/").pop();

	// Account for home page with empty path
	if ( path == '' ) {
		path = 'index.html';
	}

	var target = $('#navbarSupportedContent ul li a[href="'+path+'"]');
	// Add active class to target link
	target.parent().addClass('active');
});




// Add active class on another page linked
// ==========================================
// $(window).on('load',function () {
//     var current = location.pathname;
//     console.log(current);
//     $('#navbarSupportedContent ul li a').each(function(){
//         var $this = $(this);
//         // if the current path is like this link, make it active
//         if($this.attr('href').indexOf(current) !== -1){
//             $this.parent().addClass('active');
//             $this.parents('.menu-submenu').addClass('show-dropdown');
//             $this.parents('.menu-submenu').parent().addClass('active');
//         }else{
//             $this.parent().removeClass('active');
//         }
//     })
// });



//product details 

function OpenProduct(i){
	var i = $('.product-image[item-data="'+i+'"] img');
	var lbi = $('.lightbox-blanket .product-image img');
	console.log($(i).attr("src"));
	$(lbi).attr("src", $(i).attr("src"));  
	$(".lightbox-blanket").toggle();
	  
	$("#product-quantity-input").val("0");
	CalcPrice (0);
	
  }
  function GoBack(){
	$(".lightbox-blanket").toggle();
  }
  
  //Calculate new total when the quantity changes.
  function CalcPrice (qty){
	var price = $(".product-price").attr("price-data");
	var total = parseFloat((price * qty)).toFixed(2);
	$(".product-checkout-total-amount").text(total);
  }
  
  //Reduce quantity by 1 if clicked
  $(document).on("click", ".product-quantity-subtract", function(e){
	var value = $("#product-quantity-input").val();
	//console.log(value);
	var newValue = parseInt(value) - 1;
	if(newValue < 0) newValue=0;
	$("#product-quantity-input").val(newValue);
	CalcPrice(newValue);
  });
  
  //Increase quantity by 1 if clicked
  $(document).on("click", ".product-quantity-add", function(e){
	var value = $("#product-quantity-input").val();
	//console.log(value);
	var newValue = parseInt(value) + 1;
	$("#product-quantity-input").val(newValue);
	CalcPrice(newValue);
  });
  
  $(document).on("blur", "#product-quantity-input", function(e){
	var value = $("#product-quantity-input").val();
	//console.log(value);
	CalcPrice(value);
  });