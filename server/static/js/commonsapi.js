var Commons = {
	
	// request systems' information from the api. see timeseries/views/data_api
	getSystems : function(onsuccess){
		return $.ajax({
			url : '/data/api/systems/',
			contentType : 'json'
		}).done(onsuccess);
	},

};