// node scripts/etc/who_cc.js
// yarn add i commander
// yarn add i puppeteer
//    "When you install Puppeteer, it downloads a recent version of
//    Chromium (~170MB Mac, ~282MB Linux, ~280MB Win)



// @TODO maybe https://github.com/marketplace/actions/puppeteer-headful
// @see https://pptr.dev/
const puppeteer = require('puppeteer');
const { program } = require('commander');

program
  .name('whocc')
  .description('Fetch cleaned CSV files from World Health Organization Collaborating Centres')
  .option('--who-region', 'WHO region', 'AFRO')
  .option('--output', 'Path to output. Defaults to region.csv', null);

program.parse(process.argv);
const options = program.opts()

const project_region = options.whoRegion;
const project_output = options.output ? options.output : project_region + '.csv'
const project_page_start = 'https://apps.who.int/whocc/Search.aspx'
const project_name = 'whocc'

console.log(project_region, project_output);
// console.log(program)
// const options = program.opts();
// const limit = options.first ? 1 : undefined;
// console.log(program.args[0].split(options.separator, limit));


(async () => {
  console.log('started');
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(project_page_start);
  await page.screenshot({ path: 'temp/' + project_name + '_v1.png' });


  // await page.select('select', 'cc_region')
  await Promise.all([
    page.select('select', 'cc_region'),
    page.waitForNavigation(),
  ]);
  await page.screenshot({ path: 'temp/' + project_name + '_v2.png' });

  await Promise.all([
    page.click('input[type=submit'),
    page.waitForNavigation(),
  ]);
  await page.screenshot({ path: 'temp/' + project_name + '_v3.png' });

  await Promise.all([
    page.click('#ctl00_ContentPlaceHolder1_LinkButtonReports'),
    page.waitForNavigation(),
  ]);
  await page.screenshot({ path: 'temp/' + project_name + '_v4.png' });

  await Promise.all([
    page.click('table[title=Export]'),
    // page.waitForNavigation(),
    page.waitForSelector('a[title="CSV (comma delimited)"]', {visible: true})
  ]);
  await page.screenshot({ path: 'temp/' + project_name + '_v5.png' });

  const [ download ] = await Promise.all([
    page.waitForEvent('download'),
    page.click('a[title="CSV (comma delimited)"]'),
    // page.waitForNavigation(),
  ]);
  await page.screenshot({ path: 'temp/' + project_name + '_v6.png' });

  await console.log(download)

  // await page.screenshot({ path: 'temp/' + project_name + '_v6.png' });
  // await Promise.all([
  //   page.click('a[title="CSV (comma delimited)"]'),
  //   page.waitForNavigation(),
  // ]);
  await browser.close();
})();

