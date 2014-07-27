function go() {
  // create the histogram chart object
  var hist = new histogram().parent(d3.select('#histogram'));
  var dataURL = '/ERDA/data/responseTimeDistribution.json';
  d3.json(dataURL, function(error, data) {
    if (error) return console.warn(error);
    var bins = data.map(function(count, i) {
      return {
        x: i,
        y: count,
        dx: 1,
      };
    });
    hist.bins(bins).render();
  });
}
