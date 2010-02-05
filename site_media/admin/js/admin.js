hide_messages = function(){
	$("#loading_message").fadeOut("slow");
	
}
$(function(){
	setTimeout(hide_messages, 1000);	
});


rich_text_handler = function(){	
       try {
			$('.richtext, .rich_text').tinymce({
			// Location of TinyMCE script
			script_url : '/site_media/tiny_mce/tiny_mce.js',
 
			// General options
			theme : "advanced"});
					
				} catch (e) {
					
		}
	
}

$(rich_text_handler)
