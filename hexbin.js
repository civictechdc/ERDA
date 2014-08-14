
/**
 * Hexbin for coordinates, to, like create Leaflet Polygons
 */

function hexbin(data, opts) {
  var caccessor = opts.caccessor || function(b) { return b.color; };
  var cscale = opts.cscale || function(bs) {
    return d3.scale.linear()
      .domain([ 1, d3.max(bs, caccessor) || 1 ])
      .range([ 'white', 'black' ]);
  };
  var raccessor = opts.raccessor || function(b) { return b.length; };
  var rmax = opts.rmax || 0.5;
  var rscale = opts.rscale || function(bs) {
    return d3.scale.log()
      .domain([ 1, d3.max(bs, raccessor) || 1 ])
      .range([ rmax / 2, rmax ]);
  };

  // Hexbins!
  var hexbin = d3.hexbin()
    .radius(rmax);
  var bins = hexbin(data);

  // Get the color & radius scales based on the bins
  cscale = cscale(bins);
  rscale = rscale(bins);

  // Process the bins
  return bins.map(function(bin) {
    // Get the radius
    var rvalue = raccessor(bin);
    var radius = rscale(rvalue);

    // Get the lat / lon points
    var lls = hexagonToCoordinates(hexbin, bin, radius);

    // Get the color
    var cvalue = caccessor(bin);
    var color = cscale(cvalue);

    return {
      center: { lon: bin.x, lat: bin.y },
      color: color,
      coords: lls,
      cvalue: cvalue,
      rvalue: rvalue
    };
  });
}

/**
 * Translate from 'relative' points to actual points
 */

function hexagonToCoordinates(hexbin, bin, radius) {
  var x = bin.x, y = bin.y;
  return hexbin.hexagon(radius)
    .slice(1,-1) // remove leading 'M' & trailing 'z'
    .split('l') // remove 'l's
    .map(function(ll) {
      ll = ll.split(','); // Split lon / lat
      x -= parseFloat(ll[0]);
      y -= parseFloat(ll[1]);
      return {
        lon: x,
        lat: y
      }; // Return the actual x, y coordinates instead of the relative
    })
    .slice(1); // Start / end are duplicates when they aren't relative
}
