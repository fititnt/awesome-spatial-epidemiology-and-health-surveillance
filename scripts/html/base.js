/** This is only used for web version */

// https://gist.github.com/jfreels/6814721
function tabulate(data, columns, container_node) {
  // var table = d3.select('body').append('table')
  var table = d3.select(container_node).append('table')
  var thead = table.append('thead')
  var tbody = table.append('tbody')

  // Documentation on Boostrap table classes
  // https://getbootstrap.com/docs/5.2/content/tables/#table-borders
  // table.attr('class', 'table table-striped table-hover tablesorter')
  // @TODO add pager
  table.attr('class', 'table table-striped table-hover table-sm tablesorter')
  tbody.attr('class', 'table-group-divider')

  thead.append('tr')
    .selectAll('th')
    .data(columns)
    .enter()
    .append('th').attr('scope', 'col')
    .text(function (d) {
      // This gives change to HTML version break long hashtags
      if (d.startsWith('#')) {
        return d.replace(/(\+)/g, ' +')
      } else {
        return d
      }
    })

  var rows = tbody.selectAll('tr')
    .data(data)
    .enter()
    .append('tr')

  var cells = rows.selectAll('td')
    .data(function (row) {
      return columns.map(function (column) {
        // console.log('line', columns)
        // TODO: maybe implement some extra logic here
        // if (column.endsWith('wikiq')) {
        //   let with_link = '<a href="https://www.wikidata.org/wiki/' + row[column] + '">' + row[column] + '</a>'
        //   // return { column: column, value: row[column] }
        //   return { column: column, value: with_link }
        // }
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
  // document.querySelectorAll('[data-datapackage-path]').forEach(function (el) {

  const loader = function (el) {
    // console.log('loader', el)
    let data_csv = []
    let header_csv = []
    d3.csv(el.dataset.datapackagePath, function (data) {
      data_csv.push(data)
    }).catch(function (e) {
      console.log(e);
    }).then(function () {
      header_csv = Object.keys(data_csv[0]).filter(function (item) {
        return !(item.startsWith('#meta'))
      })
      tabulate(data_csv, header_csv, el)

      let table_widgets = []
      if (data_csv.length > 30) {
        table_widgets.push('filter')
        // table_widgets.push('chart')
        // table_widgets.push('pager')
        // table_widgets.push('columnSelector')
        // table_widgets.push('cssStickyHeaders')
        // table_widgets.push('pager')
      }

      // Examples
      // - https://mottie.github.io/tablesorter/docs/example-widget-chart.html
      // - https://jsfiddle.net/Mottie/rc9b4pkm/
      jQuery(function () {
        jQuery(el.querySelector('table')).tablesorter({
          // widgets: ['zebra', 'filter', 'pager'],
          widgets: table_widgets,
          // Show debugging info only for the filter and columnSelector widgets
          // include "core" to only show the core debugging info
          // debug : "filter columnSelector"
          theme: 'bootstrap',
          // debug: true
          debug: false

        });
      });
    })
  }


  document.querySelectorAll('[data-datapackage-autoload]').forEach(function (el) {
    loader(el)
  })
  document.querySelectorAll('[data-datapackage-loader-id]').forEach(box =>
    box.addEventListener("click", function (el) {
      console.log(el.target)
      loader(document.getElementById(el.target.dataset.datapackageLoaderId))
      // box.target.remove()
      box.remove()
    }, false)
  )
}

// console.log('TODO scripts/html/base.js')

// autoload_tables()

// document.querySelectorAll('table tbody tr').forEach(function (el) {
//   console.log(el)
//   // el.target.addEventListener("hover", function (el2) {
//   el.addEventListener("hover", function (el2) {
//     console.log(el2.target)
//     console.log(el2)
//     // loader(document.getElementById(el.target.dataset.datapackageLoaderId))
//     // // box.target.remove()
//     // box.remove()
//   }, false)
// })