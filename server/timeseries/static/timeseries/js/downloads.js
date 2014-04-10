// thanks to http://stackoverflow.com/questions/3749231/download-file-using-javascript-jquery
var downloadURL = function downloadURL(url) {
	var hiddenIFrameID = 'hiddenDownloader',
		iframe = document.getElementById(hiddenIFrameID);
	if (iframe === null) {
		iframe = document.createElement('iframe');
		iframe.id = hiddenIFrameID;
		iframe.style.display = 'none';
		document.body.appendChild(iframe);
	}
	iframe.src = url;
};

$(document).ready(function(){
	// set up date and time pickers
	$('#datepairExample .time').timepicker({
		'showDuration': true,
		'timeFormat': 'g:ia'
	});
	$('#datepairExample .date').datepicker({
		'format': 'yyyy-m-d',
		'autoclose': true
	});

	// initialize pairs
	$('#datepairExample').datepair();

	// ajax query for building page content
	Commons.getSystems(function(systems){
		var container = $("div.buttons-container");
		for(sysname in systems){
			var classname = "buttons-"+sysname.toLowerCase();
			container.append("<div class='"+classname+"'><h3>"+sysname+"</h3></div>");
			var sysdiv = $("div."+classname);
			for(subsys in systems[sysname]){
				sysdiv.append("<input type='button' class='get_data_btn' data-type='"+subsys+"' value='Get "+subsys+"' />")
			}
		}
		// set up interactivity for each button (on press, go to its specified csv downloader)
		$(".get_data_btn").each(function(idx, elem){
			$(elem).click(function(){
				console.log("csv trigger set for "+elem);
				download_csv($(elem).data("type"));
			})
		});
	});

	// helper functions

	function dateurl(datestring){
		var datefmt_in  = /(\d+)\/(\d+)\/(\d+)/i;
		var datefmt_out = "$3$1$2";
		return datestring.replace(datefmt_in, datefmt_out);
	}

	function pad(n){
		return (n < 10) ? "0"+n : ""+n;
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
		return pad(hour24)+regmatch[2]+"00";
	}

	function datetime_url(datestring, timestring){
		// TODO there must be built-in methods for doing this local timezone business
		var localTime = new Date();
		var tz_offset_mins = localTime.getTimezoneOffset();
		var tz_sign = tz_offset_mins < 0 ? '+' : '-'; // deliberately opposite sign
		var tz_hour_str = pad(Math.floor(tz_offset_mins / 60));
		var tz_mins_str = pad(tz_offset_mins % 60);
		return dateurl(datestring) + "T" + timeurl(timestring) + tz_sign + tz_hour_str + tz_mins_str;
	}

	// callback
	function download_csv(type){
		var date_start = $("input.date.start").val();
		var time_start = $("input.time.start").val();
		var date_end = $("input.date.end").val();
		var time_end = $("input.time.end").val();

		url = "/data/download/"+type+"?tstart=" + datetime_url(date_start, time_start) + "&tend=" + datetime_url(date_end, time_end);
		downloadURL(url);
	}
});