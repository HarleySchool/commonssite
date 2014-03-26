function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			// Using the CSRFToken value acquired earlier
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function makeLineChart(selector){
	getTimeseries(function(tseries){
		console.log(tseries);
		var chartdata = [];
		var npoints = tseries.Time.data.length;
		for(var i=0; i<npoints; i++){
			graphpoint = {};
			for(header in tseries){
				if(header == 'Time') graphpoint['Time'] = new Date(tseries['Time'][i]);
				else graphpoint[header] = teries[header][i];
			}
		}
		if($(selector).find("#chart").length == 0) $(selector).append("<canvas id='chart'></canvas>");
		var ctx = $(selector + " #chart").get(0).getContext("2d");
		var linechart = new Chart(ctx).Line(chartdata);
	});
}

function getTimeseries(callback){
	$.ajax({
		dataType : "json", // parse incoming data as json
		url : "/data/request/", // server url
		type : "POST", // POST so that it can have request body
		data : JSON.stringify({
			// DUMMY DATA FOR TESTING
			'start time' : Date.now() - 1000*60*60*24*14, // a day ago
			'end time' : Date.now(),
			'daily' : {'Enabled' : false},
			'system' : {
				'name' : 'HVAC-VRF',
				'cols' : ['SetTemp']
			}
		}), // the json spec according to MaxB
		success : function(data){
			callback(data);
		}
	});
}