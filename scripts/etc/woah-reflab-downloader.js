#!/usr/bin/env node
/*******************************************************************************
 * 
 *
 *          FILE:  woah-reflab-downloader.js
 *                 scripts/etc/woah-reflab-downloader.js
 *
 *         USAGE:  node scripts/etc/woah-reflab-downloader.js \
 *                   --woah-language 'AFRO' \
 *                   --output 'partials/temp/AFRO.csv
 *
 *  DESCRIPTION:   Download CSVs from https://apps.who.int/whocc/Search.aspx
 *                 and do some clean up
 *
 *  REQUIREMENTS:  - nodejs
 *                     - puppeteer (yarn add i puppeteer)
 *                       (Down: Chromium (~170MB Mac, ~282MB Linux, ~280MB Win))
 *                     - commander (yarn add i commander)
 *                     - csv (yarn add i csv)
 *          BUGS:  ---
 *         NOTES:  ---
 *        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
 *       COMPANY:  EticaAI
 *       LICENSE:  Public Domain dedication
 *                 SPDX-License-Identifier: Unlicense
 *       VERSION:  v1.0
 *       CREATED:  2022-09-03 12:42 UTC started. based on whocc-downloader.js
 *      REVISION:  ---
*******************************************************************************/

// > TL:DR: do this
// node scripts/etc/woah-reflab-downloader.js --woah-language 'EN' --output 'partials/temp/woah-reflab-en.csv'
// node scripts/etc/woah-reflab-downloader.js --woah-language 'FR' --output 'partials/temp/woah-reflab-fr.csv'
// node scripts/etc/woah-reflab-downloader.js --woah-language 'ES' --output 'partials/temp/woah-reflab-es.csv'

// > To Debug:
// node scripts/etc/woah-reflab-downloader.js --woah-language 'es' --output 'partials/temp/woah-reflab-es.csv' --show-browser
// > To check if is valid:
// frictionless validate partials/temp/woah-reflab-es.csv

// node --trace-warnings scripts/etc/who_cc.js
// yarn add i commander
// yarn add i puppeteer
//    "When you install Puppeteer, it downloads a recent version of
//    Chromium (~170MB Mac, ~282MB Linux, ~280MB Win)
const os = require("os");
const fs = require('fs');
const csv = require('csv');
const fsPromises = fs.promises;
const iso6393a2toa3 = {
  'EN': 'eng',
  'FR': 'fra',
  'ES': 'spa',
}

const puppeteer = require('puppeteer');
const { program } = require('commander');

program
  .name('woah')
  .description('Data mine World Organisation for Animal Health reference laboratories')
  .option('--woah-language', 'Language. Example: "EN", "FR", "ES"')
  .option('--output', 'Path to output. Example: temp/AFRO.csv')
  .option('--show-browser', 'If need show browser (use as last option)', false)
  // .option('--teste', 'Path to output. Defaults to region.csv')
  // .option('--tempdir', 'Path to a temporary dir', null)
  ;

program.parse(process.argv);
const options = program.opts();

// const project_woahlang = options.whoRegion;
const project_woahlang = program.args[0].toLocaleUpperCase();
const project_woahlang_a3 = iso6393a2toa3[project_woahlang];
// const project_output = options.output ? options.output : project_woahlang + '.csv'
const project_output = program.args[1];
// const project_tempdirdir = options.tempdir
const show_browser = options.showBrowser;

console.log(project_woahlang, project_woahlang_a3, project_output, program.args, program.args[0]);

// https://crm.oie.int/interconnexion/laboratoires.php?LANG=EN
// https://crm.oie.int/interconnexion/laboratoires.php?LANG=FR
// https://crm.oie.int/interconnexion/laboratoires.php?LANG=ES
const project_page_start = `https://crm.oie.int/interconnexion/laboratoires.php?LANG=` + project_woahlang;
const project_name = 'woah';

(async () => {
  // console.log('started');

  const project_tempdirdir = await fsPromises.mkdtemp(os.tmpdir() + "/woah-", (err, folder) => {
    if (err)
      console.log(err);
    else {
      console.log("The temporary folder path is:", folder);
    }
    return folder + '/';
  });
  console.log('Started. Tempdir at: ', project_tempdirdir)

  const browser = await puppeteer.launch(
    {
      // headless: is_headless, // Here can enable/disable show the browser
      headless: !show_browser, // Here can enable/disable show the browser
    }
  );

  const page = await browser.newPage();
  const client = await page.target().createCDPSession();
  await client.send('Page.setDownloadBehavior', {
    behavior: 'allow', downloadPath: project_tempdirdir
  });

  await page.goto(project_page_start);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v1.png' });

  await page.waitForSelector('#shortcutstable')

  // let titles = await(await page.$$('h3')).evaluate(node => node.innerText);

  all_titles = []
  let titles = await page.$$('h3');
  for (const title of titles) {
    // videoLinks.push(await link.evaluate( node => node.getAttribute('href')));
    all_titles.push(await title.evaluate(node => node.innerText));
  };

  // console.log(titles)
  // console.log(all_titles)

  let data = []
  data.push('#item+rem+i_' + project_woahlang_a3 + '+is_latn')
  data = data.concat(all_titles)

  let dataToWrite = ''

  // Poor's man matrix to CSV string.
  data.forEach((line) => {
    line_items = []
    if (!Array.isArray(line)) {
      line = [line]
    }
    line.forEach((item) => {
      item = item.trim()
      if (item.indexOf(",") > -1){
        line_items.push('"' + item + '"')
      } else {
        line_items.push(item)
      }
    });
    dataToWrite += line_items.join(",") + "\n"
  });

  fs.writeFile(project_output, dataToWrite, 'utf8', function (err) {
    if (err) {
      console.log('Some error occured', project_output);
    } else {
      console.log('It\'s saved!', project_output);
    }
  });

  // await Promise.all([
  //   new Promise(r => setTimeout(r, 60000))
  // ]).catch(function (err) {
  //   console.log(err.message);
  //   process.exit(1);
  // });


  console.log('TODO: delete tempdir', project_tempdirdir)
  await browser.close();
})();

