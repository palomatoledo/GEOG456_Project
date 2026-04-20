// will not work without creating the geometry

var dataset = ee.ImageCollection('USDA/NAIP/DOQQ')
                  .filter(ee.Filter.date('2017-01-01', '2018-12-31'));
var trueColor = dataset.select(['R', 'G', 'B']).median().clip(geometry);
var trueColorVis = {
  min: 0,
  max: 255,
};
Map.setCenter(-76.99606, 38.8749, 15);
Map.addLayer(trueColor, trueColorVis, 'DC 2018');
//print(trueColor)