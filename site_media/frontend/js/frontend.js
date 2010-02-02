search_handler = function(){
	$("input[name=q]").one("focus", function(){
		$(this).val("");
		
	});
}

$(search_handler);

rich_text_handler = function(){
	try {
		$(".richtext").wymeditor();
		$(".rich_text").wymeditor();
	
	} catch (e) {
	
}
}
$(rich_text_handler);
