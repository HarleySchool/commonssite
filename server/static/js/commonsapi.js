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

// thanks to django docs
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
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

function epoch(date_obj){
	return date_obj / 1000;
}

var Commons = {
	
	// request systems' information from the api. see timeseries/views/data_api
	getSystems : function(onsuccess){
		return $.ajax({
			url : '/data/api/systems/',
			contentType : 'json'
		}).done(onsuccess);
	},

	csrf : function(){
		return getCookie('csrftoken');
	},

	create_chart : function(params){
		// set up default options
		chart_options = {
			chart: {
				type: 'spline' // http://api.highcharts.com/highcharts#plotOptions
			},
			title: {
				text: (params.system + ":" + params.subsystem)
			},
			xAxis: {
				type: 'datetime', // 'linear' 'logarithmic' 'category'
				title : {
					text : 'Time'
				}
			},
			tooltip: {
				formatter: function() {
						return '<b>'+ this.series.name +'</b><br/>'+
						Highcharts.dateFormat('%x %R', this.x) +': '+ this.y;
				}
			}
		}
		// override default options with anything specified by params.chart
		if(params.hasOwnProperty('chart'))
			for (var prop in chart_options)
				chart_options[prop] = params['chart'][prop] || chart_options[prop];
		// create query object
		var filter_list = [];
		for(var header_filter in params['headers']){
			// convert a dict of {header : value, ...}
			// to the get notation: header1=value1&header2=value2
			filter_list.push($.param(header_filter));
		}
		var composite_name = params.system + ":" + params.subsystem;
		query = {};
		query[composite_name] = {
				'from' : epoch(params.from),	// params.from is a Date object
				'to' : epoch(params.to),		// TODO - handle timezones here???
				'series' : filter_list,
				'columns' : params.columns
		};
		// query server for data
		$.ajax({
			url : '/data/api/query/',
			type : 'POST',
			contentType : 'json',
			data : JSON.stringify(query)
		}).done(function(data){
			console.log(data);
			var series = [];
			for(var group in data){
				if(!data.hasOwnProperty(group)) continue;
				var npts = data[group]['Time'].length;
				// each 'group' is a header section
				for(var ser in data[group]){
					if(ser !== 'Time'){
						points = [];
						for(var i=0; i<npts; i++){
							points.push([1000*data[group]['Time'][i], data[group][ser][i]]);
						}
						series.push({
							name: group+": "+ser,
							data: points
						});
					}
				}
			}

			chart_options.series = series;
			// create chart
			var newdiv = $("<div style='width:600px'></div>");
			var container = $(params.container) || $("section#content");
			container.append(newdiv);
			newdiv.highcharts(chart_options);
		});
	}
};