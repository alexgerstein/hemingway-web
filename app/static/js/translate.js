var WORDS_PER_MILLISEC = 4
var MILLISECS = 400

function getWidthPercentage(selector) {
	return 100 * parseFloat($(selector).css('width')) / parseFloat($(selector).parent().css('width'));
}

function translate() {
	clearFormSubmission()
	var posting = $.post('/translate', $('#input-form').serialize())

	posting.fail (function(response) {
		alert("There was an error translating the text!")
	})

	posting.done (function(response) {
		if ('errors' in response) {
			for (field in response['errors']) {
				var input = $('#' + field).parent();
				input.addClass('has-error')
				input.append('<p class="help-block">' + response['errors'][field][0] +'</p>')
			}
	    }
	    else {
	    	$('#output').text(response['output'])
	    }
	})
}

function set_progress() {
	var words = $('#input_text').val().split(" ").length
	var progress = setInterval(function() {
		var $bar = $('.progress-bar');
	    
	    if (getWidthPercentage('.progress-bar')>=100) {
	        clearInterval(progress);
	        $bar.width("0%");
	    } else {
	        $bar.width(getWidthPercentage('.progress-bar') + ((WORDS_PER_MILLISEC * MILLISECS) / words) * 100 + "%");
	    }
	}, MILLISECS);
}

function clearFormSubmission() {
	$('#output').empty();
	$('.help-block').remove();
	$('.form-group').removeClass('has-error');
}

$(document).ready(function() {
    var $loading = $('.progress').hide();
	$(document)
	  .ajaxStart(function () {
	    $loading.show();
	    set_progress();
	  })
	  .ajaxStop(function () {
	    $loading.hide();
	  });
});
