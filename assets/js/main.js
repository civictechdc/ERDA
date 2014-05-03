function responseTimes(hist) {
  var apiURL = 'http://54.187.110.72/emr_data/?page=0&per_page=100';
  d3.json(apiURL, function(error, events) {
    if (error) return console.warn(error);
    var responseTimes = events.map(function(d) {
      return moment.duration(d.response_time).asSeconds();
    });
    hist.data(responseTimes)
      .render();
  });
}

function go() {
  // create the histogram chart object
  var hist = new histogram().parent(d3.select('#histogram'));
  responseTimes(hist);
}
