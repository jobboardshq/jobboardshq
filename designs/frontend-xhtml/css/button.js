// JavaScript Document
	$(function() {
		// set opacity to nill on page load
		$("ul#menu span").css("opacity","0");
		// on mouse over
		$("ul#menu span").hover(function () {
			// animate opacity to full
			$(this).stop().animate({
				opacity: 1
			}, 'slow');
		},
		// on mouse out
		function () {
			// animate opacity to nill
			$(this).stop().animate({
				opacity: 0
			}, 'slow');
		});
	});