const puppeteer = require('puppeteer');
(async () => {
  const b = await puppeteer.launch({args:['--no-sandbox']});
  const p = await b.newPage();
  await p.setViewport({width: 414, height: 900, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await p.goto('https://eveglyphdesign.github.io/scs-sap-gtm/', {waitUntil: 'networkidle0'});
  await p.screenshot({path:'/home/user/workspace/scs-sap-gtm/_review/phone-full.png', fullPage: true});
  await b.close();
  console.log('ok');
})();
