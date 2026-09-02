import puppeteer from '/home/user/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';
const b = await puppeteer.launch({
  executablePath: '/home/user/.cache/puppeteer/chrome/linux-148.0.7778.97/chrome-linux64/chrome',
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
  headless: 'new',
});
const p = await b.newPage();
await p.setViewport({ width: 414, height: 900, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await p.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
await p.goto('https://eveglyphdesign.github.io/scs-sap-gtm/', { waitUntil: 'networkidle0', timeout: 60000 });
await new Promise(r => setTimeout(r, 1500));
await p.screenshot({ path: '/home/user/workspace/scs-sap-gtm/_review/phone-full.png', fullPage: true });
console.log('ok');
await b.close();
