
function AnalyticEvents_Download_Downloaded (eventLabel) {
	eventAction = "Downloaded";
	eventCategory = "Download";
	
	eventData = {
		"event_category": eventCategory,
		"event_label": eventLabel
	};
	
	gtag("event", eventAction, eventData);
}

function AnalyticEvents_Download_ViewedLicense (eventLabel) {
	eventAction = "Viewed license";
	eventCategory = "Download";
	
	eventData = {
		"event_category": eventCategory,
		"event_label": eventLabel
	};
	
	gtag("event", eventAction, eventData);
}