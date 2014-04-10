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
	// ajax query for building page content
	Commons.getSystems(function(systems){
		var container = $("div.buttons-container");
		for(sysname in systems){
			var classname = "buttons-"+sysname.toLowerCase();
			container.append("<div class='"+classname+"'><h3>"+sysname+"</h3></div>");
			var sysdiv = $("div."+classname);
			for(subsys in systems[sysname]){
				sysdiv.append("<button type='button' class='btn btn-xs btn-primary get_data_btn' data-type='"+subsys+"''>Get "+subsys+"</button>")
			}
		}
		// set up interactivity for each button (on press, go to its specified csv downloader)
		$(".get_data_btn").each(function(idx, elem){
			$(elem).click(function(){
				download_csv($(elem).data("type"));
			})
		});
	});

	// callback
	function download_csv(type){
		if(daterange['start'] == null || daterange['end'] == null){
			console.log('BAD FORM: cannot deal with null datetime');
			return;
		}
		url = "/data/download/"+type+"?tstart=" + daterange['start'].toISOString() + "&tend=" + daterange['end'].toISOString();
		downloadURL(url);
	}
});