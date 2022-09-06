/** This is only used for web version */

// https://gist.github.com/jfreels/6814721
function tabulate(data, columns, container_node) {
  // var table = d3.select('body').append('table')
  var table = d3.select(container_node).append('table')
  var thead = table.append('thead')
  var tbody = table.append('tbody')

  thead.append('tr')
    .selectAll('th')
    .data(columns)
    .enter()
    .append('th')
    .text(function (d) { return d })

  var rows = tbody.selectAll('tr')
    .data(data)
    .enter()
    .append('tr')

  var cells = rows.selectAll('td')
    .data(function (row) {
      return columns.map(function (column) {
        // console.log('line', columns)
        return { column: column, value: row[column] }
      })
    })
    .enter()
    .append('td')
    .text(function (d) { return d.value })

  return table;
}

function autoload_tables() {
  // http://bl.ocks.org/ndarville/7075823
  document.querySelectorAll('[data-datapackage-path]').forEach(function (el) {
    console.log(el)
    console.log(el.id)
    console.log('the path3', el.dataset.datapackagePath)


    // d3.csv(el.dataset.datapackagePath, function(data) {
    //   // console.log(data)
    //   for (var i = 0; i < data.length; i++) {
    //       console.log(data[i].Name);
    //       console.log(data[i].Age);
    //   }
    // });

    d3.csv(el.dataset.datapackagePath, function (data) {
      // const columns = Object.keys(data[0])
      // const columns = Object.keys(data)
      const columns = ['#item+conceptum+codicem']
      console.log('item now...', el.dataset.datapackagePath)

      // var columns = ['variable','aror','asd','maxdd']
      tabulate(data, columns, el)
    })

    // d3.text("data.csv", function(data) {
    d3.text(el.dataset.datapackagePath, function (data) {
      console.log('d3 generating table...', el.dataset.datapackagePath)
      var parsedCSV = d3.csv.parseRows(data);

      // var container = d3.select("body")
      var container = d3.select('#' + el.id)
        .append("table")

      .selectAll("tr")
          .data(parsedCSV).enter()
          .append("tr")

      .selectAll("td")
          .data(function(d) { return d; }).enter()
          .append("td")
          .text(function(d) { return d; });
    });
  })
}

console.log('TODO scripts/html/base.js')

autoload_tables()

// d3.text("http://git.workspace.localhost/fititnt/awesome-spatial-epidemiology/data/biosafety-levels.hxl.tm.hxl.csv", function(data) {
//   var parsedCSV = d3.csv.parseRows(data);

//   console.log('data2', data)
//   var container = d3.select("body")
//       .append("table")

//       .selectAll("tr")
//           .data(parsedCSV).enter()
//           .append("tr")

//       .selectAll("td")
//           .data(function(d) { return d; }).enter()
//           .append("td")
//           .text(function(d) { return d; });
// });

// mydata=
// d3.csv("http://git.workspace.localhost/fititnt/awesome-spatial-epidemiology/data/biosafety-levels.hxl.tm.hxl.csv",function(d){
// return {col1: d.col1, col2: d.col2}}

// ).then(function(data) {
//   return data;
// });


// d3.csv("http://git.workspace.localhost/fititnt/awesome-spatial-epidemiology/data/biosafety-levels.hxl.tm.hxl.csv")
//     .row(function(d) { return {key: d.key, value: +d.value}; })
//     .get(function(error, rows) { console.log(rows); });