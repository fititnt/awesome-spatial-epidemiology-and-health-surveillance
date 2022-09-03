// node scripts/etc/whocc.js --who-region 'AFRO' --output 'partials/temp/AFRO.csv


// node --trace-warnings scripts/etc/who_cc.js
// yarn add i commander
// yarn add i puppeteer
//    "When you install Puppeteer, it downloads a recent version of
//    Chromium (~170MB Mac, ~282MB Linux, ~280MB Win)
const os = require("os");
const fs = require('fs');
const fsPromises = fs.promises;
// const tempDir = os.tmpdir(); // /tmp

// @TODO maybe https://github.com/marketplace/actions/puppeteer-headful
// @see https://pptr.dev/
const puppeteer = require('puppeteer');
const { program } = require('commander');
// const { tmpdir } = require('node:os');
// import { tmpdir } from 'node:fs';
// const os = require("os");
// const tempDir = os.tmpdir(); // /tmp
// const mkdtemp = os.mkdtemp // /tmp
// const fsPromises = require("fs").promises;
// const { fs } = require('nodefs');
// import { tmpdir } from 'node:os';
// import { mkdtemp } from 'node:fs';

// console.log('mkdtemp', mkdtemp)
program
  .name('whocc')
  .description('Fetch cleaned CSV files from World Health Organization Collaborating Centres')
  .option('--who-region', 'WHO region. Example: "AFRO"')
  .option('--output', 'Path to output. Example: temp/AFRO.csv')
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
  console.log('todo csvfile', created_files)
  created_files.forEach(file => {
    console.log(file);
    if (file.endsWith('.csv')) {
      console.log('this is the file', file)
      console.log('this is the file', project_tempdirdir + '/' + file)
      fs.copyFile(project_tempdirdir + '/' + file, project_output, (err) => {
        if (err)
          throw err;
        console.log('copied file', project_tempdirdir + '/' + file, project_output);
      });
      // fs.readFileSync(project_tempdirdir + '/' + file, function (err, data) {
      //   if (err)
      //     throw err;
      //   console.log('data', data)
      //   data_v2 = data.toString().replace(/WHO Collaborating Centres\s\sGlobal database/gm, 'WHO Collaborating Centres Global database')
      //   data_v3 = data_v2.toString().replace(/\.\s"/gm, '."')
      //   fs.writeFileSync(project_output + '.edite2', data_v3);
      //   console.log('editef file', project_output)
      // });
    } else {
      console.log('not the .csv file', file)
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
      headless: false, // Here can enable/disable show the browser
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
  ]);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v2.png' });

  await Promise.all([
    page.click('input[type=submit'),
    page.waitForNavigation(),
  ]);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v3.png' });

  // page.on('response', (response)=>{ console.log(response, response._url)});
  await Promise.all([
    page.click('#ctl00_ContentPlaceHolder1_LinkButtonReports'),
    page.waitForNavigation(),
  ]);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v4.png' });

  await Promise.all([
    page.click('table[title=Export]'),
    // page.waitForNavigation(),
    page.waitForSelector('a[title="CSV (comma delimited)"]', { visible: true })
  ]);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v5.png' });

  // Here we check some events
  page.on('response', (response) => {
    console.log(response, response._url)
  });

  const [download] = await Promise.all([
    // page.waitForEvent('download'),
    page.click('a[title="CSV (comma delimited)"]'),
    // Note: this is better done by watchin the file downloaded at tempdir
    new Promise(r => setTimeout(r, 5000))
  ]);
  await page.screenshot({ path: project_tempdirdir + '/' + project_name + '_v6.png' });

  clean_csv(project_tempdirdir, project_output)

  console.log('TODO: delete tempdir', project_tempdirdir)
  await browser.close();
})();

