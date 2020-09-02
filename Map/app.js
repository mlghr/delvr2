

const mymap = L.map('mapid').setView([26.505, 20], 13);

	L.tileLayer('gameMap.png', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1,
		access_token: "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"
				}).addTo(mymap);

	const bounds = [[0,0], [1000,1000]];
	const image = L.imageOverlay('gameMap.png', bounds).addTo(gameMap);

	game.fitBounds(bounds);
				

//const gameMap = L.map('gameMap', {
//	crs: L.CRS.Simple,
//	minZoom: -5
//});
//
//L.tileLayer('gameMap.png', {
//    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//}).addTo(gameMap);
//
//const bounds = [[0,0], [1000,1000]];
//const image = L.imageOverlay('gameMap.png', bounds).addTo(gameMap);
//
//gameMap.fitBounds(bounds);
//
//
//const mark = L.latLng([ 145, 175.2 ]);
//L.marker(mark).addTo(map);
//map.setView( [70, 120], 1);