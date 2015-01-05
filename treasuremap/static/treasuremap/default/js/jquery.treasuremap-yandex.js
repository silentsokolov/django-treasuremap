(function($) {
    function addMarker(position, map, latinput, lnginput, markers) {
        // del markers
        deleteMarkers(map, markers);

        // create new placemark
        var placemark = new ymaps.Placemark(position, {});

        // add placemark to map
        map.geoObjects.add(placemark);

        // update value
        latinput.val(placemark.geometry.getCoordinates()[0].toFixed(6));
        lnginput.val(placemark.geometry.getCoordinates()[1].toFixed(6));

        // save marker
        markers.push(placemark);

        // move map to new position in center
        map.panTo(position);
    }

    function deleteMarkers(map, markers) {
        for (var i = 0; i < markers.length; i++) {
            map.geoObjects.remove(markers[i]);
        }
        markers = [];
    }

    $(document).ready(function() {
        return ymaps.ready(function() {
            $('.treasure-map').each(function (index, element) {
                var map_element = $(element).children('.map').get(0);
                var latitude_input = $(element).children('input:eq(0)');
                var longitude_input = $(element).children('input:eq(1)');

                var options = $.parseJSON($(element).children('script').text()) || {};
                var markers = [];

                var defaultMapOptions = {};

                // init default map options
                defaultMapOptions.center = [
                    parseFloat(latitude_input.val()) || options.latitude,
                    parseFloat(longitude_input.val()) || options.longitude
                ];

                // merge user and default options
                var mapOptions = $.extend(defaultMapOptions, options);

                // create map
                var map = new ymaps.Map(map_element, mapOptions);

                // add default marker
                if (latitude_input.val() && longitude_input.val()) {
                    addMarker(defaultMapOptions.center, map, latitude_input, longitude_input, markers);
                }

                // init listener
                return map.events.add("click",
                    function(e) {
                        addMarker(e.get('coords'), map, latitude_input, longitude_input, markers);
                    }
                );
            });
        });
    });
})((typeof window.jQuery == 'undefined' && typeof window.django != 'undefined') ? django.jQuery : jQuery);
