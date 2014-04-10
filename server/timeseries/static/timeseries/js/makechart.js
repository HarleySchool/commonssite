$(document).ready(function(){
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
		if(daterange['start'] == null || daterange['end'] == null){
			console.log('BAD FORM: cannot deal with null datetime');
			return;
		}

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
			'from' : daterange['start'].toISOString(),
			'to' : daterange['end'].toISOString(),
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