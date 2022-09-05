#!/usr/bin/env node
/*******************************************************************************
 * 
 *
 *          FILE:  whocc-downloader.js
 *                 scripts/etc/whocc-downloader.js
 *
 *         USAGE:  node scripts/etc/whocc-downloader.js \
 *                   --who-region 'AFRO' \
 *                   --output 'partials/temp/AFRO.csv
 *
 *  DESCRIPTION:   Download CSVs from https://apps.who.int/whocc/Search.aspx
 *                 and do some clean up
 *
 *  REQUIREMENTS:  - nodejs
 *                     - puppeteer (yarn add i puppeteer)
 *                       (Down: Chromium (~170MB Mac, ~282MB Linux, ~280MB Win))
 *                     - commander (yarn add i commander)
 *          BUGS:  ---
 *         NOTES:  ---
 *        AUTHOR:  Emerson Rocha <rocha[at]ieee.org>
 *       COMPANY:  EticaAI
 *       LICENSE:  Public Domain dedication
 *                 SPDX-License-Identifier: Unlicense
 *       VERSION:  v1.0
 *       CREATED:  2022-09-03 09:21 UTC
 *      REVISION:  ---
*******************************************************************************/

// > TL:DR: do this
// node scripts/etc/whocc-downloader.js --who-region 'AFRO' --output 'partials/temp/AFRO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'AMRO' --output 'partials/temp/AMRO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'EMRO' --output 'partials/temp/EMRO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'EURO' --output 'partials/temp/EURO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'SEARO' --output 'partials/temp/SEARO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'SEARO' --output 'partials/temp/SEARO.csv'
// node scripts/etc/whocc-downloader.js --who-region 'WPRO' --output 'partials/temp/WPRO.csv'

// > To Debug:
// node scripts/etc/whocc-downloader.js --who-region 'WPRO' --output 'partials/temp/WPRO.csv' --show-browser
// > To check if is valid:
// frictionless validate partials/temp/WPRO.csv

// const is_headless = true // Change this to force display chrome (for debug)

// node --trace-warnings scripts/etc/who_cc.js
// yarn add i commander
// yarn add i puppeteer
//    "When you install Puppeteer, it downloads a recent version of
//    Chromium (~170MB Mac, ~282MB Linux, ~280MB Win)
const os = require("os");
const fs = require('fs');
const fsPromises = fs.promises;

const puppeteer = require('puppeteer');
const { program } = require('commander');

program
  .name('whocc')
  .description('Fetch cleaned CSV files from World Health Organization Collaborating Centres')
  .option('--who-region', 'WHO region. Example: "AFRO"')
  .option('--output', 'Path to output. Example: temp/AFRO.csv')
  .option('--show-browser', 'If need show browser (use as last option)', false)
  // .option('--teste', 'Path to output. Defaults to region.csv')
  // .option('--tempdir', 'Path to a temporary dir', null)
  ;

program.parse(process.argv);
const options = program.opts()

// const project_region = options.whoRegion;
const project_region = program.args[0];
// const project_output = options.output ? options.output : project_region + '.csv'
const project_output = program.args[1];
// const project_tempdirdir = options.tempdir
const show_browser = options.showBrowser;

const project_page_start = 'https://apps.who.int/whocc/Search.aspx'
const project_name = 'whocc'

// console.log(program, options, project_region, project_output, program.opts().project_output);
// console.log(program.getOptionValue('output'));
// console.log(project_region, project_output);

// process.exit()

async function clean_csv(project_tempdirdir, project_output) {
  console.log('clean_csv', project_tempdirdir, project_output)
  const created_files = await fsPromises.readdir(project_tempdirdir, (err, files) => {
    if (err)
      throw err;
    return files
  });
  // console.log('todo csvfile', created_files)
  created_files.forEach(file => {
    console.log(file);
    if (file.endsWith('.csv')) {
      // console.log('this is the file', file)
      console.log('this is the file', project_tempdirdir + '/' + file)
      console.log('output will be on ', project_output)
      // fs.copyFile(project_tempdirdir + '/' + file, project_output, (err) => {
      //   if (err)
      //     throw err;
      //   console.log('copied file', project_tempdirdir + '/' + file, project_output);
      // });
      // fs.readFileSync(project_tempdirdir + '/' + file, function (err, data) {
      fs.readFile(project_tempdirdir + '/' + file, function (err, data) {
        if (err)
          throw err;
        console.log('readFileSync now', data)
        // Remove line breanks on the name of WHO CC
        data_v2 = data.toString().replace(/WHO Collaborating Centres\s\sGlobal database/gm, 'WHO Collaborating Centres Global database')

        // People seems to like to add extra newlines after their descriptions
        data_v3 = data_v2.toString().replace(/\.\s*"/gm, '."').replace(/\n*"/gm, '"')

        // TODO: outside here: remove newlines inside the fields
        data_v4 = data_v3

        data_v5 = data_v4.trim()
        // fs.writeFileSync(project_output, data_v3);
        // fs.writeFile(project_output, data_v3);
        fs.writeFile(project_output, data_v5, (err) => {
          if (err)
            console.log(err);
          else {
            console.log("File written successfully\n", project_output);
            // console.log("The written has the following contents:");
            // console.log(fs.readFileSync("books.txt", "utf8"));
          }
        });
        console.log('editef file', project_output)
      });
    } else {
      // console.log('not the .csv file', file)
    }
  });
}

(async () => {
  // console.log('started');

  const project_tempdirdir = await fsPromises.mkdtemp(os.tmpdir() + "/whocc-", (err, folder) => {
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

  // await page.select('select', 'cc_region')
  await Promise.all([
    page.select('select', 'cc_region'),
    page.waitForNavigation(),
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v2.png' });

  await Promise.all([
    page.select('#ctl00_ContentPlaceHolder1_criteriaValue_1', project_region),
    new Promise(r => setTimeout(r, 200))
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v3.png' });

  await Promise.all([
    page.click('input[type=submit'),
    page.waitForNavigation(),
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v4.png' });

  // page.on('response', (response)=>{ console.log(response, response._url)});
  await Promise.all([
    page.click('#ctl00_ContentPlaceHolder1_LinkButtonReports'),
    page.waitForNavigation(),
    new Promise(r => setTimeout(r, 2000))  // Why this is necessary?
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v5.png' });

  await Promise.all([
    page.click('table[title=Export]'),
    // page.waitForNavigation(),
    // page.waitForSelector('a[title="CSV (comma delimited)"]', { visible: true }),
    new Promise(r => setTimeout(r, 1000))
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });

  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v6.png' });

  // // Here we check some events
  // page.on('response', (response) => {
  //   console.log(response, response._url)
  // });

  const [download] = await Promise.all([
    // page.waitForEvent('download'),
    page.click('a[title="CSV (comma delimited)"]'),
    // Note: this is better done by watchin the file downloaded at tempdir
    new Promise(r => setTimeout(r, 5000))
  ]).catch(function (err) {
    console.log(err.message);
    process.exit(1);
  });
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v7.png' });

  clean_csv(project_tempdirdir, project_output)

  console.log('TODO: delete tempdir', project_tempdirdir)
  await browser.close();
})();

