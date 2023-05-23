// Rendering the map
var mymap = L.map('map').setView([42.37034, -72.505769], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(mymap);

// Declaring variables to interact with the map
var popup = L.popup();
var sourceMarker, destinationMarker;
var routingControl;
var routeFromWaypoints;

// Function to handle map clicks
function onMapClick(e) {
    if (!sourceMarker) {
        sourceMarker = L.marker(e.latlng).addTo(mymap);
    } else if (!destinationMarker) {
        destinationMarker = L.marker(e.latlng).addTo(mymap);
        calculateRoute();
    } else {
        sourceMarker.removeFrom(mymap);
        destinationMarker.removeFrom(mymap);
        sourceMarker = L.marker(e.latlng).addTo(mymap);
        destinationMarker = null;
        mymap.removeControl(routingControl);
        mymap.removeControl(routeFromWaypoints);
    }
}

// Function to calculate and render route on the map
function calculateRoute() {
    var waypoints = [
        sourceMarker.getLatLng(),
        destinationMarker.getLatLng()
    ];

    console.log(waypoints);

    var options = {
        waypoints: waypoints,
        profile: 'cycling',
        preference: 'shortest',
        routeWhileDragging: true
    };

    // Send the waypoints to the Flask backend
    $.ajax({
        type: 'POST',
        url: '/calculate_route', // Replace with the Flask endpoint URL
        data: JSON.stringify({
            waypoints: waypoints,
            option: $('#maxmin').val(),
            percentage: $('#percentage').val()
        }),
        contentType: 'application/json',
        success: function(response) {
            // Fetch response from Flask
            console.log(response);
            var routeFromBackend = response.route.map(([first, second]) => [second, first]);

            document.getElementById("source").innerHTML = [waypoints[0].lat.toFixed(5), waypoints[0].lng.toFixed(5)];
            document.getElementById("dest").innerHTML = [waypoints[1].lat.toFixed(5), waypoints[1].lng.toFixed(5)];
            document.getElementById("totaldist").innerHTML = response.curr_dist.toFixed(4);
            document.getElementById("elevgain").innerHTML = response.elevation_dist.toFixed(4);
            document.getElementById("elevdrop").innerHTML = response.drop_dist.toFixed(4);

            routingControl = L.Routing.control({
                waypoints: waypoints,
                lineOptions: {
                    styles: [{ className: 'leaflet-dashed-line' }] // Apply the custom style to the route polyline
                }
            }).addTo(mymap);

            routeFromWaypoints = L.Routing.control({
                waypoints: routeFromBackend,
                lineOptions: {
                    styles: [{ className: 'leaflet-solid-line' }] // Apply the custom style to the route polyline
                },
                createMarker: function() {
                    return null;
                }
            }).addTo(mymap);

            routingControl.hide();
            routeFromWaypoints.hide();
        }
    });
}

// Adding on click listener to handle the map clicks
mymap.on('click', onMapClick);
var _geocoderType = L.Control.Geocoder.nominatim();
var geocoder = L.Control.geocoder({
geocoder: _geocoderType,
defaultMarkGeocode: false,
collapsed: true,
placeholder: "Search for a location",
}).on('markgeocode', function(e) {
mymap.setView(e.geocode.center, 13);
}).addTo(mymap);