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

function toLocalDate (inDate) {
	var date = new Date();
	date.setTime(inDate.valueOf() - 60000 * inDate.getTimezoneOffset());
	return date;
}

function server_to_highcharts_format(server_serieses){
	var highcharts_serieses = [];
	// for each of the series that was initially requested, add it to the highcharts series...
	for (var s = 0; s < server_serieses.length; s++) {
		var server_series = server_serieses[s];
		var data_points = server_series.data;
		if(data_points.length == 0) continue;

		/* The data come in as [{Time: 'ISO', Col1: val1, Col2: val2}, ...]
		 * And need to go out as [{Time: 'ISO', Col1: val1},...], [{Time: 'ISO', Col2: val2}]
		 * (in other words, each 'column' gets its own highcharts series)
		 */
		var under_construction = {};
		// using the 0th entry as a 'typical' example, make a separate list of data points for each column
		var col_names = Object.keys(data_points[0]);
		var time_index = col_names.indexOf('Time');
		if(time_index > -1) col_names.splice(time_index,1);
		for(var i=0; i<col_names.length; i++)
			under_construction[col_names[i]] = [];

		for(var i=0; i<data_points.length; i++){
			var point = data_points[i];
			var t = new Date(point.Time);
			for(var j=0; j<col_names.length; j++){
				under_construction[col_names[j]].push({x: toLocalDate(t).valueOf(), y: point[col_names[j]]});
			}
		}

		// now we have an object which maps from colname => [list of data points]
		for(var named_data in under_construction){
			var series_name = named_data;
			if(server_series.index){
				series_name = server_series.index + " " + series_name;
			}
			highcharts_serieses.push({'name' : series_name, 'data' : under_construction[named_data]});
		}
	};
	return highcharts_serieses;
}

var Commons = {

	live_intervals : [],

	kill_live : function(){
		for(var id in this.live_intervals){
			clearInterval(id);
		}
		this.live_intervals = [];
	},

	csrf : function(){
		return getCookie('csrftoken');
	},
	
	// request systems' schema and other information from the api. see timeseries/views/data_api
	get_systems : function(onsuccess){
		return $.ajax({
			url : '/data/api/systems/',
			contentType : 'json'
		}).done(onsuccess);
	},

	create_chart : function(series, title, tstart, tend, container_selector, chart_type, temporary, averages, callback){
		temporary = typeof(temporary) === "undefined" ? false : temporary;
		averages = typeof(averages) === "undefined" ? true : averages;
		// set up default options
		var chart_options = {
			chart: {
				type: chart_type || "spline" // http://api.highcharts.com/highcharts#plotOptions
			},
			plotOptions : {
				series : {
					marker : {
						enabled : false
					}
				}
			},
			title: {
				text: title,
			},
			xAxis: {
				type: 'datetime', // 'linear' 'logarithmic' 'category'
				title : {
					text : 'Time'
				}
			},
			yAxis: {
				title : null
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
			"temporary" : temporary,
			"averages" : averages,
			"series" : series
		};
		// query server for data
		$.ajax({
			url : '/data/api/series/',
			type : 'POST',
			contentType : 'json',
			data : JSON.stringify(query)
		}).done(function(data){ // do this when the server response (see timeseries.helpers.series_filter regarding how `data` is formatted)
			var highcharts_serieses = server_to_highcharts_format(data);
			chart_options.series = highcharts_serieses;
			// create chart
			var container = $(container_selector);
			if(container === undefined){
				container = $("<div style='width:600px'></div");
				$("div.container").append(container);
			}
			container.highcharts(chart_options);
			if(typeof(callback) !== "undefined")
				callback(container.highcharts());
		});
	},

	live_chart : function(series, title, container_selector, timespan_mins, chart_type){
		// default arguments
		timespan_mins = timespan_mins || 60*3; // default to 3 hours
		var timespan_millis = timespan_mins * 60000;
		// make a chart of data up till now
		var now = new Date();
		this.create_chart(series, title, new Date(now - timespan_millis), now, container_selector, chart_type, true, false, function(chart_obj){
			// set up updater function (new data every 10 seconds)
			var interval_id = setInterval(function(){
				// query server for new data
				$.ajax({
					url : '/data/api/single/',
					type : 'POST',
					contentType : 'json',
					data : JSON.stringify({'series' : series})
				}).done(function(data){ // do this when the server response (see timeseries.helpers.series_filter regarding how `data` is formatted)
					var new_data = server_to_highcharts_format(data);
					// update each series
					for (var i = new_data.length - 1; i >= 0; i--) {
						var existing_series = chart_obj.series[i].options.data;
						var update = new_data[i].data;
						// remove old/expired points (each point is {x: time, y: value})
						var span = update[0].x - existing_series[0].x;
						console.log("timespan of "+title+": "+span);
						while(span > timespan_millis){
							existing_series.shift(); // removes the first element
							span = update[0].x - existing_series[0].x;
						}
						// add new point
						existing_series.push(update[0]);
						chart_obj.series[i].setData(existing_series, false);
					};
					// redraw chart
					chart_obj.redraw();
				});
				}
			, 10000);
			Commons.live_intervals.push(interval_id);
		});
	}
};
