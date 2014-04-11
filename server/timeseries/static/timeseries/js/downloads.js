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
	// callback
	function download_csv(type){
		if(daterange.startDate == null || daterange.endDate == null){
			console.log('BAD FORM: cannot deal with null datetime');
			return;
		}
		url = "/data/download/"+type+"?tstart=" + daterange.startDate.toISOString() + "&tend=" + daterange.endDate.toISOString();
		downloadURL(url);
	}
	// set up interactivity for each button (on press, go to its specified csv downloader)
	$(".get_data_btn").each(function(idx, elem){
		$(elem).click(function(){
			download_csv($(elem).data("type"));
		})
	});
});