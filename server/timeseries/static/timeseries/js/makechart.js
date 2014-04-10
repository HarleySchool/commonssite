$(document).ready(function(){
	// set up date and time pickers
	$('#datepairExample .time').timepicker({
		'showDuration': true,
		'timeFormat': 'g:ia'
	});
	$('#datepairExample .date').datepicker({
		'format': 'yyyy-mm-dd',
		'autoclose': true
	});

	// initialize pairs
	$('#datepairExample').datepair();

	// helper functions
	function pad(n){
		return (n < 10) ? "0"+n : ""+n;
	}

	function dateurl(datestring){
		var datefmt_in  = /(\d+)\/(\d+)\/(\d+)/i;
		var datefmt_out = "$3-$1-$2";
		return datestring.replace(datefmt_in, datefmt_out);
	}

	function timeurl(timestring){
		var timefmt_in = /(\d+)\:(\d+)([ap]m)/i;
		var regmatch = timestring.match(timefmt_in);
		var hour12 = parseInt(regmatch[1]);
		var hour24 = hour12;
		if(regmatch[3] == 'pm'){
			// if in PM, add 12. so 1pm is 13 o'clock, 11pm is 23 o'clock
			hour24 += 12;
		} else if(regmatch[3] == 'am' && hour12 == 12){
			// '12am' is actually "zero o'clock"
			hour24 = 0;
		}
		return pad(hour24)+":"+regmatch[2]+":00";
	}

	function datetime_input_to_iso(datestring, timestring){
		// TODO there must be built-in methods for doing this local timezone business
		var localTime = new Date();
		var tz_offset_mins = localTime.getTimezoneOffset();
		var tz_sign = tz_offset_mins < 0 ? '+' : '-'; // deliberately opposite sign
		var tz_hour_str = pad(Math.floor(tz_offset_mins / 60));
		var tz_mins_str = pad(tz_offset_mins % 60);
		return dateurl(datestring) + "T" + timeurl(timestring) + tz_sign + tz_hour_str + tz_mins_str;
	}
	
	// set up the on-change handler for when a system is selected
	$("select.system_select").change(function(){
		var target_show_id = $(this).find(':selected').data("subsysid");
		var target_show_div = $("div#"+target_show_id);
		$(".params_wrapper").hide();
		target_show_div.show();
	});
	$("select.system_select").change(); // call it immediately so that the initial system's parameters appear on the screen

	// this handles when the "(select all)" options are checked
	$(".check_all").change(function(){
		// step up to the parent div, then set the checked-ness of all of its children
		// (siblings(".check_option") could have been used if it weren't for the <label><input /> text</label> construct)
		$(this).closest("div").find("input.check_option").prop('checked', this.checked);
	});

	// callback for actually making the graph
	$("#makegraph_btn").click(function(){
		var dtstart = datetime_input_to_iso($("input.date.start").val(), $("input.time.start").val());
		var dtend = datetime_input_to_iso($("input.date.end").val(), $("input.time.end").val());

		var params_id = $("select.system_select").find(":selected").data("subsysid");
		var params_div = $("div#"+params_id);

		var headers = [];

		var columns = [];
		params_div.find("div.column_select input.check_option").each(function(idx, elem){
			if(elem.checked){
				columns.push($(elem).data("colname"));
			}
		});

		var chart_options = {
			'container' : "#charts-container",
			'from' : dtstart,
			'to' : dtend,
			'system' : $("select.system_select").find(":selected").data("sys"),
			'subsystem' : $("select.system_select").find(":selected").data("sub"),
			'headers' : headers,
			'columns' : columns
		};

		Commons.create_chart(chart_options);
	});
});

// $("#testbtn").click(function(){
// 	console.log("TESTING");
// 	$.ajax({
// 		type: 'POST',
// 		contentType: 'json',
// 		data: JSON.stringify({
// 			'HVAC:VRF' : {
// 				'from' : new Date() / 1000 - 24*60*60,
// 				'to' : new Date() / 1000,
// 				'series' : ['Name=Control Room'],
// 				'columns' : ['SetTemp', 'InletTemp']
// 			}
// 		}),
// 		beforeSend: function(xhr, settings) {
// 			if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
// 				// Send the token to same-origin, relative URLs only.
// 				// Send the token only if the method warrants CSRF protection
// 				// Using the CSRFToken value acquired earlier
// 				xhr.setRequestHeader("X-CSRFToken", Commons.csrf());
// 			}
// 		}
// 	}).done(function(data){
// 		for(name in data){
// 			make_chart(data[name]);
// 		}
// 	});
// });