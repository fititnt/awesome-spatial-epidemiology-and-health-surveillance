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
    let data_csv = []
    let header_csv = []
    d3.csv(el.dataset.datapackagePath, function (data) {
      data_csv.push(data)
    }).catch(function (e) {
      console.log(e); // "Ah, não!"
    }).then(function () {
      header_csv = Object.keys(data_csv[0])
      tabulate(data_csv, header_csv, el)
    })
    
  })
}

// console.log('TODO scripts/html/base.js')

autoload_tables()
