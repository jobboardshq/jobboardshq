search_handler = function(){
	$("input[name=q]").one("focus", function(){
		$(this).val("");
		
	});
}

$(search_handler);
