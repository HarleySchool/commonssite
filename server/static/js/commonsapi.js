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

function server_to_highcharts_series(data){
	var highcharts_construction = {}; // temporary, under-construction, series of data
	// for each of the series that was initially requested, add it to the highcharts series...
	for (var i = data.length - 1; i >= 0; i--) {
		var t = data[i].Time;
		var h = data[i].H; // dict of headers
		var d = data[i].D; // dict of datums
		
		var headers_name = ""; // e.g. "Panel 1: Channel #4"
		for(var head in h){
			if(headers_name !== "")
				headers_name += ": ";
			headers_name += h[head];
		}

		for(var col in d){
			var full_name = headers_name + ": " + col; // e.g. "Panel 1: Channel #4: MaxPower"
			// create new series if not already exists
			if(!highcharts_construction.hasOwnProperty(full_name))
				highcharts_construction[full_name] = {'name' : full_name, 'data' : []}
			// add data point
			highcharts_construction[full_name].data.push([new Date(t), d[col]]);
		}
	};

	// done constructing series. now just the values of highcharts_construction are relevant
	var highcharts_series = [];
	for(var name in highcharts_construction){
		highcharts_series.push(highcharts_construction[name]);
	}

	return highcharts_series;
}

var Commons = {

	csrf : function(){
		return getCookie('csrftoken');
	},
	
	// request systems' information from the api. see timeseries/views/data_api
	get_systems : function(onsuccess){
		return $.ajax({
			url : '/data/api/systems/',
			contentType : 'json'
		}).done(onsuccess);
	},

	create_chart : function(series, tstart, tend, container_selector){
		// set up default options
		chart_options = {
			chart: {
				type: 'spline' // http://api.highcharts.com/highcharts#plotOptions
			},
			title: {
				text: 'Historical Data'
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
						Highcharts.dateFormat('%m/%d %H:%M', this.x) +': '+ this.y;
				}
			},
		}
		// create query object from series
		query = {
			"from" : tstart.toISOString(),
			"to" : tend.toISOString(),
			"series" : series
		};
		// query server for data
		$.ajax({
			url : '/data/api/series/',
			type : 'POST',
			contentType : 'json',
			data : JSON.stringify(query)
		}).done(function(data){ // do this when the server response (see timeseries.helpers.series_filter regarding how `data` is formatted)
			var highcharts_series = server_to_highcharts_series(data);
			chart_options.series = highcharts_series;
			// create chart
			var container = $(container_selector);
			if(container === undefined){
				container = $("<div style='width:600px'></div");
				$("div.container").append(container);
			}
			container.highcharts(chart_options);
		});
	},

	live_chart : function(series, title, container_selector, timespan_mins, chart_type){
		// default arguments
		timespan_mins = timespan_mins || 60*24*7; // default to one week
		var timespan_millis = timespan_mins * 60 * 1000;
		chart_type = chart_type || 'spline';
		// set up default options
		chart_options = {
			chart: {
				type: chart_type // http://api.highcharts.com/highcharts#plotOptions
			},
			title: {
				text: title
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
						Highcharts.dateFormat('%m/%d %H:%M', this.x) +': '+ this.y;
				}
			},
		}
		// keep track of the chart itself
		var thechart;
		// query server for initial data
		console.log("live data init: "+title);
		$.ajax({
			url : '/data/api/single/',
			type : 'POST',
			contentType : 'json',
			data : JSON.stringify({'series' : series})
		}).done(function(data){ // do this when the server response (see timeseries.helpers.series_filter regarding how `data` is formatted)
			console.log("live data response: "+title);
			var highcharts_series = server_to_highcharts_series(data);
			chart_options.series = highcharts_series;
			// create chart
			var container = $(container_selector);
			if(container === undefined){
				container = $("<div style='width:600px'></div");
				$("div.container").append(container);
			}
			container.highcharts(chart_options);
			thechart = container.highcharts();
		});

		// set up updater function (new data every 10 seconds)
		setInterval(function(){
			console.log("live data update: "+title);
			console.log(thechart);
			// query server for new data
			$.ajax({
				url : '/data/api/single/',
				type : 'POST',
				contentType : 'json',
				data : JSON.stringify({'series' : series})
			}).done(function(data){ // do this when the server response (see timeseries.helpers.series_filter regarding how `data` is formatted)
				var new_data = server_to_highcharts_series(data);

				// update each series
				for (var i = new_data.length - 1; i >= 0; i--) {
					var existing_series = thechart.series[i].options.data;
					console.log(existing_series);
					var update = new_data[i].data;
					// remove old/expired points (each point is [Time, val0])
					var span = update[0] - existing_series[0];
					while(span > timespan_millis){
						existing_series.shift(); // removes the first element
						span = update[0] - existing_series[0];
					}
					// add new point
					existing_series.push(update[0]);
					thechart.series[i].setData(existing_series, false);
					console.log(existing_series);
				};
				// redraw chart
				thechart.redraw();
			});
			}
		, 10000);
	}
};
