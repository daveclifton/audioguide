///////////////////////////////////////////////////////////////////////////
// Audio Player
//
function AudioPlayer( waypoint ) {
    href = $('#audio').children('a').attr('href');
    $('#audio_title').html(waypoint.title);

    $.template('audioTemplate', '<audio src="'+waypoint.audio_file+'" controls>');
    if (Modernizr.audio.mp3) {
        $('#audio').empty();
        $.tmpl('audioTemplate', {src: href}).appendTo($('#audio'));
    }
};

///////////////////////////////////////////////////////////////////////////
// RouteModel is the data class for a route
//
RouteModel = function(source) {
    var that = this;

    try {
        if ( ! source ) {
            this.source_data = {
                "title":       "New RouteModel",
                "description": "New RouteModel",
                "color":       "black",
                "waypoints":    []
            };
        } else if (typeof(source) == "string" ) {
            this.source_data = JSON.parse(source);
        } else {
            this.source_data = source;
        }

    } catch(err) {
        alert(err.message);
        return;
    }

    this.bounds = new google.maps.LatLngBounds();

    this.source_data.waypoints.forEach( function(waypoint) {
        marker = MapModel.add( waypoint );
        that.bounds.extend(marker.position );
    });

    this.register_display = function(route_display) {
        that.route_display = route_display
    };

    this.waypoints = function() {
        return(that.source_data.waypoints)
    };

    this.title = function() {
        return(that.source_data.title)
    };

    this.description = function() {
        return(that.source_data.description)
    };

    this.color = function() {
        return(that.source_data.color)
    };


    this.add = function(waypoint) {
        that.source_data.waypoints.push( waypoint );
        that.route_display.add( waypoint );
    };

    this.delete = function(waypoint_id) {
            for ( i in that.source_data.waypoints ) {
                if ( that.source_data.waypoints[i].waypoint_id == waypoint_id ) {
                    that.source_data.waypoints[i].remove_marker();  // from map
                    that.source_data.waypoints.splice(i,1);     // from route
                }
            }
        that.draw();
    };


    this.sort = function(waypoint_ids) {
        that.source_data.waypoints = that.source_data.waypoints.sort(function(a,b){
              return waypoint_ids.indexOf(a.waypoint_id) > waypoint_ids.indexOf(b.waypoint_id) ? 1:0
        });
        that.draw();
    };


    var polyline = new google.maps.Polyline({
                path:        [],
                strokeColor: that.source_data.color,
                strokeWeight: 2
            });


    this.draw = function() {
        polyline.setMap( MapModel.map );
        polyline.setPath(
            that.source_data.waypoints.map(
                function(waypoint){ return new google.maps.LatLng( waypoint.lat, waypoint.lng ) })
        );
    };


    this.undraw = function() {
        that.source_data.waypoints.forEach( function(waypoint) {
            waypoint.remove_marker();
        } );

        polyline.setMapModel(null);
    }


    this.to_json = function() {
        return( JSON.stringify(that.source_data,null,4) );
    }
};


///////////////////////////////////////////////////////////////////////////
// RouteView: display class for a RouteModel relates to a div.route.
//
RouteView = function(route) {
    var that = this;

    this.route = route;
    this.route.register_display(this);

    this.div = $("#route_template .route")
            .clone()
            .appendTo($(".routes"))
            .css("border-color",route.color());

    this.div.find(".title")
            .text(route.title())
            .click( function(){ that.div.find(".body").toggle() } );

    this.div.find(".description")
            .text(route.description());

    // Sort the route when the list is updated
    this.div.find("ul").disableSelection()
        .sortable({ update: function(event,ui) { that.route.sort( that.div.find("ul").sortable('toArray') ) } });

    this.div.find(".save" ).click( function() { that.save() } );
    this.div.find(".close").click( function() { that.close() } );


    this.add = function( waypoint ) {
        ul = $('<li><span class="delete">[X]</span></li>')
            .attr("id",waypoint.waypoint_id)
            .appendTo(that.div.find("ul"))
            .append(waypoint.title);

        ul.find(".delete").click( function() {
            that.route.delete( waypoint.waypoint_id );
            that.div.find("li#"+waypoint.waypoint_id).remove();
        });
    };


    this.save = function() {
        alert( "route = "+ that.route.to_json() );
    };

    this.close = function() {
        RouteController.remove(that.route);
        this.div.remove();
    };


    route.waypoints().forEach( function(waypoint) { that.add( waypoint ) });
};


///////////////////////////////////////////////////////////////////////////
// RouteController (static class)
//
RouteController = {
    routes: [],

    add_route: function(source) {
        route     = new RouteModel(source);
        waypoints = new RouteView(route);
        RouteController.routes.push(route);
        MapModel.resize(RouteController.routes);
        RouteController.redraw();
    },

    add_waypoint: function(waypoint) {

        MapModel.add( waypoint );

        // Add the waypoint to all routes
        // TODO: Find a way to add to selected route only
        RouteController.routes.forEach( function(route) {
            route.add( waypoint );
        });
        RouteController.redraw();
    },

    remove: function(route) {
        RouteController.routes = RouteController.routes.filter( function(r) { return r != route } );
        route.undraw();
    },

    redraw: function() {
        MapModel.redraw(RouteController.routes);
    },
};


$(".routes .create").click( function(){
    url = $(".routes .json").val();
    $.getJSON(url, function(data) {RouteController.add_route(data)});
});


//////////////////////////////////////////////////////////////////////////
// MapModel class (static class)
//
MapModel = {
    init: function() {

        MapModel.map = new google.maps.Map(document.getElementById('map'), {styles: MapModel.styles});

        MapModel.map.addListener( 'click', function(event){
            RouteController.add_waypoint( {
                waypoint_id: Math.floor((1 + Math.random()) * 0x100000000).toString(16),
                lat:       event.latLng.G,
                lng:       event.latLng.K,
                title:     JSON.stringify( [event.latLng.G, event.latLng.K] ),
                audio:     "no audio"
            });
        });
    },

    styles: [{ stylers: [
            { hue: "#00ffe6" },
            { saturation: -20 }
            ]
        },{ featureType: "road",
            elementType: "geometry",
            stylers: [
              { lightness: 100 },
              { visibility: "simplified" }
            ]
        },{
            featureType: "road",
            elementType: "labels",
            stylers: [ { visibility: "off" } ]
        }
    ],


    resize: function(routes) {
        bounds = new google.maps.LatLngBounds();
        routes.forEach( function(route) {
            bounds.union( route.bounds );
        });
        MapModel.map.fitBounds(bounds);
    },

    redraw: function(routes) {
        routes.forEach( function(route) {
            route.draw();
        });
    },

    add: function(waypoint) {
        var marker = new google.maps.Marker({
            "map":       MapModel.map,
            "position":  new google.maps.LatLng(waypoint.lat, waypoint.lng),
            "title":     waypoint.title,
            "audio":     waypoint.audio,
            "source":    waypoint,
            "draggable": true,
            "icon":      "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
        });

        marker.addListener('click', function() {
            AudioPlayer( waypoint );
        });

        marker.addListener('dragend', function(event) {
            waypoint.lat = event.latLng.G;
            waypoint.lng = event.latLng.K;
            RouteController.redraw();
        });

        waypoint.remove_marker = function(){ marker.setMapModel(null); };
        return(marker);
    }
}



//////////////////////////////////////////////////////////////////////////
// main()
//
function map_init() {


    var route_1 = {
    "title":       "Bath Walking Tour",
    "description": "Example tour, copied from http://channels.visitbath.co.uk/janeausten/audio-tour",
    "color":       "#0000FF",
    "waypoints": [
        {
            "title": "Introduction and Abbey Court Yard",
            "lat": 51.38136,
            "lng": -2.359578000000056,
            "audio_file": "http://channels.visitbath.co.uk/downloads/Chapter%2013%20The%20Assembly%20Rooms.mp3",
            "waypoint_id": "159f2f9ff"
        },
        {
            "title": "Sally Lunn's House",
            "lat": 51.380754,
            "lng": -2.3586689999999635,
            "audio_file": "http://channels.visitbath.co.uk/downloads/Chapter%2003%20Sally%20Lunns%20House.mp3",
            "waypoint_id": "1b051baea"
        },
        {
            "title": "The Lower Rooms",
            "lat": 51.380737,
            "lng": -2.357934,
            "audio_file": "http://channels.visitbath.co.uk/downloads/Chapter%2004%20The%20Lower%20Rooms.mp3",
            "waypoint_id": "1eb474b41"
        }
        ]
    };

    var map = new google.maps.Map(document.getElementById('map'), {});

    MapModel.init();
    RouteController.add_route(route_1);

    //$.getJSON( "https:bath_route_1.json", function(data) {RouteController.add_route(data)});
}
