hide_messages = function(){
	$("#loading_message").fadeOut("slow");
	
}
$(function(){
	setTimeout(hide_messages, 1000);	
});


rich_text_handler = function(){	
       try {
			$('.richtext, .rich_text, .RTEField').tinymce({
			// Location of TinyMCE script
			script_url : '/site_media/tiny_mce/tiny_mce.js',
 
			// General options
			theme : "advanced"});
					
				} catch (e) {
					
		}
	
}

$(rich_text_handler);

jQuery.fn.slugify = function(obj) {
    jQuery(this).data('obj', jQuery(obj));
    jQuery(this).keyup(function() {
        var obj = jQuery(this).data('obj');
        var slug = jQuery(this).val().replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
        obj.val(slug);
    });
}
