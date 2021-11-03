var cookie = encodeURIComponent(document.cookie);
var skipDom = 'no';

function scan(cookie, skipDom, customHeader) {
  a=document.URL;
  b=encodeURIComponent(a);
  c='target=' + b + '&op=scan&skipDom=' + skipDom;
  d='http://127.0.0.1/XSStrike-extension/src/xss.php?' + c + '&cookie=Cookie: ' + cookie + '\\n' + customHeader;
  window.open(d);
}

function crawl(cookie, skipDom, customHeader) {
  e=document.URL;
  f=encodeURIComponent(e);
  g='target=' + f + '&op=crawl&skipDom=' + skipDom;
  h='http://127.0.0.1/XSStrike-extension/src/xss.php?' + g + '&cookie=Cookie: ' + cookie + '\\n' + customHeader;
  window.open(h);
}
chrome.runtime.onMessage.addListener(
      function(request, sender, sendResponse) {
        customHeader = request.header
        if( request.message == "crawl" ) {
          crawl(cookie, skipDom, customHeader);
        }
        else if(request.message == "crawl-skipDom") {
          skipDom = "yes";
          crawl(cookie, skipDom, customHeader);
        }
        else if(request.message == "scan-skipDom") {
          skipDom = "yes"
          scan(cookie, skipDom, customHeader);
        }
        else {
          skipDom = "no";
          scan(cookie, skipDom, customHeader);
        }

      }
);

