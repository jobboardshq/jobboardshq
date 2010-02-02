hide_messages = function(){
	$("#loading_message").fadeOut("slow");
	
}
$(function(){
	setTimeout(hide_messages, 1000);	
});


rich_text_handler = function(){
	try {
		$(".richtext").wymeditor();
		$(".rich_text").wymeditor();
	
	} catch (e) {
	
}
}

$(rich_text_handler)
