/**
 *
 *          FILE:  hxltm-web-utils.js
 *                 assets/js/hxltm-web-utils.js
 *
 *         USAGE:  ---
 *
 *   DESCRIPTION:  hxltm-web-utils
 *
 *  REQUIREMENTS:  - papaparse
 *                 - jQuery (not really essential, but whatever)
 *
 *          BUGS:  ---
 *         NOTES:  ---
 *        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
 *       COMPANY:  EticaAI
 *       LICENSE:  Public Domain dedication
 *                 SPDX-License-Identifier: Unlicense
 *       VERSION:  v1.0
 *       CREATED:  2022-09-11 20:29 UTC
 *      REVISION:  ---
**/


/**
 *
 * @param {string} remove_csv
 * @param {Object} options
 * @param {callback} cb
 */
function hxltm_fetch(remove_csv, options, cb_newline, cb_complete) {
  let total = 0
  Papa.parse(remove_csv, {
    download: true,
    header: true,
    worker: true,
    preview: 0,
    skipEmptyLines: 'greedy',
    escapeFormulae: false,
    columns: options.columns,
    // transform: function (value, header) {
    //   return value
    // },
    step: function (row) {
      cb_newline(row.data)
      total += 1
    },
    complete: function (results, file) {
      // console.log("Parsing complete:", results, file, total);
      options['total'] = total
      cb_complete(options)
    }
  });
  // console.log('hxltm_fetch', remove_csv, callback)
}

/**
 * hxltm_headers_filter
 *
 * @param {array} headers 
 * @returns {array}
 */
function hxltm_headers_filter(headers) {
  let new_headers = []
  headers.forEach(function (item) {
    if (!(item.startsWith('#meta'))) {
      new_headers.push(item)
    }
  })
  return new_headers
}

/**
 * 
 * @param {string} hxlhashtag
 * @param {string} value
 */
function hxltm_html_format_value(hxlhashtag, value) {
  if (!value || value.length == 0) {
    return value
  }

  if (hxlhashtag == "#item+conceptum+codicem") {
    // console.log('codicem', value)
    if (value.indexOf('_') > -1) {
      let deep = (value.split('_').length - 1) * 2
      return `<span class="ms-${deep}">${value}</span>`
    }
    return value
  }

  let values = [value]
  let values_formated = [value]
  if (value.indexOf('|') > -1) {
    values = value.split('|')
    values_formated = values
  } else if (value.startsWith('https://') || value.startsWith('http://')) {
    values_formated = [`<a href="${value}">${value}</a>`]
  }
  // @TODO make proper format checker
  if (hxlhashtag.indexOf('+ix_wikiq') > -1) {
    // console.log('hxlhashtag', hxlhashtag)
    values_formated = []
    values.forEach(item => {
      values_formated.push(`<a href="https://www.wikidata.org/wiki/${item}">${item}</a>`)
    })
  } else if (hxlhashtag.indexOf('+ix_wikip') > -1) {
    // console.log('hxlhashtag', hxlhashtag)
    values_formated = []
    values.forEach(item => {
      values_formated.push(`<a href="https://www.wikidata.org/wiki/Property:${item}">${item}</a>`)
    })
  } else if (hxlhashtag.indexOf('+ix_xywdatap1282') > -1 || hxlhashtag.indexOf('+ix_wdatap1282') > -1) {
    // console.log('hxlhashtag', hxlhashtag)
    values_formated = []
    values.forEach(item => {
      values_formated.push(`<a href="https://wiki.openstreetmap.org/wiki/${item}">${item}</a>`)
    })
  }
  return values_formated.join(' | ')
}

/**
 * Initialize an HTML table with some extra syntax for Bootstrap and
 * tablesorter
 *
 * @param {string} conteiner_id
 * @param {Object} options
 * @param {callback} cb
 */
function hxltm_html_table(conteiner_id, options, cb) {
  let wrapper = $(`#${conteiner_id}`)
  let table_init_str = '<table class="table table-striped table-hover table-sm tablesorter">'
  table_init_str += '<thead>'
  table_init_str += '<tr scole="col">'
  options.columns.forEach(function (item) {
    table_init_str += `<th>${item.split('+').join(' +')}</th>`
  })
  table_init_str += '</tr>'
  table_init_str += '</thead>'
  table_init_str += `<tbody class="table-group-divider"></tbody>`
  table_init_str += '</table>'
  // let table = document.createElement("table")
  // wrapper.append('table')
  // wrapper.append('<table><thead></thead><tbody id="temp"></tbody></table>')
  wrapper.append(table_init_str)
  // console.log('hxltm_html_table_initialize', table)
  options['tbody'] = jQuery(`#${conteiner_id} table tbody`)
  options['tbody_sel'] = `#${conteiner_id} table tbody`
  // console.log('aaaa', options)
  // console.log('table_init_str', table_init_str)
  cb(options)
}

/**
 * Inject a new line on a tbody
 *
 * @param {Element} tbody
 * @param {Object} options
 * @param {Object} line
 */
function hxltm_html_table_new_line(tbody, options, line) {
  let newline = []
  for (const [key, value] of Object.entries(line)) {
    // console.log(`${key}: ${value}`);
    // newline.append('<td>' + item + '</td>')
    newline.push(`<td>${hxltm_html_format_value(key, value)}</td>`)
  }
  // line.forEach(item =>
  //   newline.append('<td>' + item + '</td>')
  // )
  tbody.append('<tr role="row">' + newline.join() + '</tr>')
  // console.log('hxltm_html_table_new_line', line)
}


/**
 * 
 * @param {string} remove_csv
 * @param {Object} options
 * @param {callback} cb
 * @returns {number}
 */
function hxltm_prefetch(remove_csv, _options, cb) {
  Papa.parse(remove_csv, {
    download: true,
    header: true,
    worker: false,
    preview: 1,
    // skipEmptyLines: 'greedy',
    // escapeFormulae: false,
    // transform: function (value, header) {
    //   return value
    // },
    step: function (row) {
      // console.log("Row:", row.data);
      let original_headers = Object.keys(row.data)
      let new_headers = hxltm_headers_filter(original_headers)
      // console.log('headers', original_headers, new_headers)
      cb({ columns: new_headers })
    },
    // complete: function () {
    //   console.log("hxltm_prefetch: All done!");
    // }
    // complete: function(results, file) {
    //   console.log("Parsing complete:", results, file);
    //   cb()
    // }

  });
  // console.log(remove_csv, cb)
}

/**
 * 
 * @param {string} remote_csv
 * @param {string} conteiner_id
 */
function hxltm_ui_loadtable(remote_csv, conteiner_id) {
  if (!(remote_csv.startsWith('/')) && !(remote_csv.startsWith('http'))) {
    remote_csv = window.location.origin + window.location.pathname + remote_csv
  }

  // console.log('@TODO hxltm_ui_loadtable', remote_csv, conteiner_id)
  hxltm_prefetch(remote_csv, null, function (options) {
    // console.log('hxltm_prefetch done', options)
    // hxltm_html_table('n1603_16_1_0__table', options, function(){
    hxltm_html_table(conteiner_id, options, function () {
      hxltm_fetch(remote_csv, options, function (newline) {
        hxltm_html_table_new_line(options.tbody, options, newline)
      }, function (options) {
        console.log('complete', options)
        let table_widgets = []
        if (options.total > 30) {
          table_widgets.push('filter')
          // table_widgets.push('stickyHeaders')
          // table_widgets.push('resizable')
        }
        // table_widgets = [ "zebra", "filter", "pager" ]
        jQuery($(`#${conteiner_id} table`)).tablesorter({
          // widgets: ['zebra', 'filter', 'pager'],
          widgets: table_widgets,
          // debug : "filter columnSelector"
          theme: 'bootstrap',
          debug: true
          // debug: false

        });
      })
    })
  })
}

// let remote_csv = "http://git.workspace.localhost/fititnt/awesome-spatial-reference-data/data/cod_ab.hxl.csv"

// hxltm_fetch('./data/cod_ab.hxl.csv', console.log)
// hxltm_prefetch(remote_csv, null, function (options) {
//   console.log('hxltm_prefetch done', options)
//   hxltm_html_table('n1603_16_1_0__table', options, function () {
//     hxltm_fetch(remote_csv, options, function (newline) {
//       hxltm_html_table_new_line(options.tbody, options, newline)
//     })
//   })
// })

// hxltm_ui_loadtable(remote_csv, 'n1603_16_1_0__table')

// hxltm_prefetch(remote_csv, null, function (options) {
//   console.log('hxltm_prefetch done')
//   // hxltm_fetch(remote_csv, options, function () {
//   //   console.log('hxltm_fetch done')
//   // })
// })
// hxltm_fetch("http://git.workspace.localhost/fititnt/awesome-spatial-reference-data/data/cod_ab.hxl.csv", console.log)

document.querySelectorAll('[data-datapackage-autoload]').forEach(function (el) {
  let remote_csv = el.dataset.datapackagePath
  // console.log('autoloader', el, remote_csv, el.id)
  hxltm_ui_loadtable(remote_csv, el.id)
})

document.querySelectorAll('[data-datapackage-loader-id]').forEach(box =>
  box.addEventListener("click", function (el) {
    let container = document.getElementById(el.target.dataset.datapackageLoaderId)
    let remote_csv = container.dataset.datapackagePath
    hxltm_ui_loadtable(remote_csv, container.id)
    box.parent().remove()
  }, false)
)