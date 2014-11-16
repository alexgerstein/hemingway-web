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

function download() {
  var pom = document.createElement('a');
  pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent($("#output").text()));
  pom.setAttribute('download', "output.txt");
  pom.click();
}

function compute_changes() {
	var original = $("#input_text").val().split(" ")
	var converted = $("#output").html().split(" ")

	var changes = 0;
	var total_words = original.length;

	for (var i = 0; i < original.length; i++) {
		if (original[i] != converted[i]) {
			var split_word = original[i].match(/[\w-']+|[^\w\s]+/g)
			var punctuation = ""
			if (split_word.length > 1) {
				punctuation = split_word[1];
			}

			var converted_text = converted[i].replace(punctuation, "");
			var original_text = original[i].replace(punctuation, "");

			converted[i] = '<highlight data-toggle="tooltip" title="' + original_text + '">' + converted_text + '</highlight>' + punctuation;
			changes += 1;
		}
	}

	$("#output").html(converted.join(" "));
	$("#status").text(changes + " out of " + total_words + " words replaced");
	$("highlight").tooltip();
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
	    	$('#output').html(response['output']);
	    	compute_changes();
	    }
	})
}

function set_progress() {
	var words = $('#input_text').val().split(" ").length;

	var progress = setInterval(function() {
		var $bar = $('.progress-bar');
	    
	    if (getWidthPercentage('.progress-bar')>=100) {
	        clearInterval(progress);
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
  		$('.progress-bar').width("100%");
	    $loading.hide();
  		$('.progress-bar').width("0%");
	  });

	$('#style').change(set_default_text).change();
});
