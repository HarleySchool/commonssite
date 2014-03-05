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
		return dateurl(datestring) + "T" + timeurl(timestring);
	}

	// callback
	function download_csv(type){
		var date_start = $("input.date.start").val();
		var time_start = $("input.time.start").val();
		var date_end = $("input.date.end").val();
		var time_end = $("input.time.end").val();

		url = "/data/"+type+"?tstart=" + datetime_url(date_start, time_start) + "&tend=" + datetime_url(date_end, time_end);
		console.log(url);
		downloadURL(url);
	}

	$("#submitvrf").click(function(event){
		download_csv("vrf");
	});

	$("#submiterv").click(function(event){
		download_csv("erv");
	});
});