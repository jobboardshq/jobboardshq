delete_handler = function(){
	$(this).html("deleting");
	url = $(this).attr("href");
	$.post(url, {}, function(data){
		to_hide = "#job_"+data.pk;
		$(to_hide).hide("slow");
		
	}, "json");
	return false;
}
$(function(){
	$(".delete_link").click(delete_handler);
});


