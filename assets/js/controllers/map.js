---
---
function go() {
  // create the map
  var map = new eventsMap().parent(d3.select('#map'));
  var dataURL = '{{site.baseurl}}/data/1000events.json';
  d3.json(dataURL, function(error, data) {
    map.data(data).render();
  });
}
