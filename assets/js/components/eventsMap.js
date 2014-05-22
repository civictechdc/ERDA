/*
Map of emergency response events. Uses Google Maps JavaScript API.

By default, the map is centered approximately on the intersection of 4th Street
NW, and L Street NW.
*/
function eventsMap() {
  // defaults
  var parent = undefined;
  var data = [];
  var map = undefined;
  var overlay = undefined;
  var options = {
    center: new google.maps.LatLng(38.903725,-77.016202),
    zoom: 12
  };
  var aspect = 1.0;
  var r = d3.scale.linear()
    .domain([9, 19])
    .range([1, 20.0])
    .clamp(true);

  // The object that will be returned.
  var chart = {};

  function width() {
    return $(parent.node()).width();
  }

  function height() {
    return $(parent.node()).height();
  }

  function resize() {
    parent.style('width', '100%').style('height', width()*aspect + 'px');
  }

  function renderAll() {
    resize();
    renderMap();
  }

  function renderMap() {
    if (!map) {
      map = new google.maps.Map(document.getElementById('map'), options);
    }
    if (!overlay) {
      overlay = new google.maps.OverlayView();
      overlay.onAdd = onAddOverlay;
      overlay.setMap(map);
      //google.maps.event.addListener(map, 'zoom_changed', renderOverlay);
    }
  }

  function onAddOverlay() {
    overlay.draw = renderOverlay;
  }

  function renderOverlay() {
    var overlayLayer = d3.select(overlay.getPanes().overlayLayer);
    var projection = overlay.getProjection();
    var zoom = map.getZoom();
    var rz = r(zoom);

    var events = overlayLayer.selectAll('svg.emergency-event')
      .data(data);
    events.enter()
      .append('svg')
      .attr('class', 'emergency-event')
      .append('circle');
    events.style('width', function(d) {
        return rz*3 + 'px';
      })
      .style('height', function(d) {
        return rz*3 + 'px';
      });

    function updateMarker(d) {
      var coords = new google.maps.LatLng(d.latitude, d.longitude);
      xy = projection.fromLatLngToDivPixel(coords);
      d3.select(this)
        .style("left", (xy.x - rz*1.5) + "px")
        .style("top",  (xy.y - rz*1.5) + "px")
        .select('circle')
        .attr('cx', rz*1.5)
        .attr('cy', rz*1.5)
        .attr('r', rz);
    }

    events.each(updateMarker);
  }

  // interface functions

  chart.data = function(value) {
    if (!arguments.length) return data;
    data = value;

    return chart;
  };

  chart.parent = function(value) {
    if (!arguments.length) return parent;
    parent = value;

    return chart;
  };

  // render the chart
  chart.render = function() {
    renderAll();
    d3.select(window).on('resize.events-map', function() {
      renderAll();
    });

    return chart;
  };

  return chart;
}
