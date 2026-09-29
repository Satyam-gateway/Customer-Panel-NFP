/* A static file server for the prototype, bound to every interface so the
   other machines on this network can open it too — localhost alone is only
   ever this laptop. Node because Python is not installed here.

   node serve.js [port]                                                     */

const http = require('http');
const fs   = require('fs');
const path = require('path');
const os   = require('os');

const PORT = Number(process.argv[2]) || 8756;
const ROOT = __dirname;

const TYPES = {
  '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.css':'text/css; charset=utf-8',   '.json':'application/json; charset=utf-8',
  '.svg':'image/svg+xml',  '.png':'image/png',  '.jpg':'image/jpeg',
  '.jpeg':'image/jpeg',    '.gif':'image/gif',  '.webp':'image/webp',
  '.ico':'image/x-icon',   '.woff':'font/woff', '.woff2':'font/woff2',
};

http.createServer((req, res) => {
  /* strip the cache-buster query, then resolve and check the result is still
     inside ROOT — a request for ../../ must not walk out of the folder */
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel === '/') rel = '/relay-prototype.html';
  const file = path.join(ROOT, path.normalize(rel));
  if (!file.startsWith(ROOT)) { res.writeHead(403).end('Forbidden'); return }

  fs.readFile(file, (err, buf) => {
    if (err) { res.writeHead(404, {'Content-Type':'text/plain'}).end('Not found'); return }
    res.writeHead(200, {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      /* it is a prototype being reloaded constantly — never serve a stale copy */
      'Cache-Control': 'no-store',
    });
    res.end(buf);
  });
}).listen(PORT, '0.0.0.0', () => {
  const ips = Object.values(os.networkInterfaces()).flat()
    .filter(i => i && i.family === 'IPv4' && !i.internal).map(i => i.address);
  console.log('\n  Relay prototype\n');
  console.log('    this machine   http://localhost:' + PORT + '/relay-prototype.html');
  ips.forEach(ip => console.log('    on the network http://' + ip + ':' + PORT + '/relay-prototype.html'));
  console.log('\n  Ctrl-C to stop.\n');
});
