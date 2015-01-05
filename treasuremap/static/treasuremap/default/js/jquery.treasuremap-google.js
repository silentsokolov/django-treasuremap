(function($) {
    function addMarker(position, map, latinput, lnginput, markers) {
        // del markers
        deleteMarkers(null, markers);

        // create new marker
        var marker = new google.maps.Marker({
            position: position,
            map: map
        });

        // update value
        latinput.val(marker.getPosition().lat().toFixed(6));
        lnginput.val(marker.getPosition().lng().toFixed(6));

        // save marker
        markers.push(marker);

        // move map to new position in center
        map.panTo(position);
    }

    function deleteMarkers(map, markers) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
        }
        markers = [];
    }

    $(document).ready(function() {
        $('.treasure-map').each(function (index, element) {
            var map_element = $(element).children('.map').get(0);
            var latitude_input = $(element).children('input:eq(0)');
            var longitude_input = $(element).children('input:eq(1)');

            var options = $.parseJSON($(element).children('script').text()) || {};
            var markers = [];

            // var zoom = options.zoom || 4;

            var defaultMapOptions = {};

            // init default map options
            defaultMapOptions.center = new google.maps.LatLng(
                parseFloat(latitude_input.val()) || options.latitude,
                parseFloat(longitude_input.val()) || options.longitude
            );

            // merge user and default options
            var mapOptions = $.extend(defaultMapOptions, options);

            // create map
            var map = new google.maps.Map(map_element, mapOptions);

            // add default marker
            if (latitude_input.val() && longitude_input.val()) {
                addMarker(defaultMapOptions.center, map, latitude_input, longitude_input, markers);
            }

            // init listener
            google.maps.event.addListener(map, 'click', function (e) {
                addMarker(e.latLng, map, latitude_input, longitude_input, markers);
            });
        });
    });
})((typeof window.jQuery == 'undefined' && typeof window.django != 'undefined') ? django.jQuery : jQuery);
