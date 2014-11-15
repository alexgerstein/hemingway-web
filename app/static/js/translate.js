// Progress Bar Constants
var WORDS_PER_MILLISEC = 3
var MILLISECS = 200

// Default Author Text
var HEMINGWAY = "The best way to find out if you can trust somebody is to trust them."
var DICKENS = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair…"
var SHAKESPEARE = "Shall I compare thee to a summer's day?\nThou art more lovely and more temperate:\nRough winds do shake the darling buds of May,\nAnd summer's lease hath all too short a date."
var RAPPERS = "If you having girl problems I feel bad for you son. I got 99 problems but a bitch ain’t one."

function getWidthPercentage(selector) {
	return 100 * parseFloat($(selector).css('width')) / parseFloat($(selector).parent().css('width'));
}

function set_default_text(e) {
	$("#input_text").val(window[e.target.value.toUpperCase()]);
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

	$('#style').change(set_default_text).change();
});
