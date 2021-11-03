<div align="center">
  <br>
  <a href="https://github.com/tauh33dkhan/XSStrike-extension"><img src="https://i.ibb.co/XCNfc6P/xsstrike-extension.png" alt="xsstrike-extension" border="0"></a>
  <br>
  <b>A browser extension for XSS Discovery</b><br/>
  <a href="https://opensource.org/licenses/GPL-3.0"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/tauh33dkhan/xsstrike-extension/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
  <img src="https://img.shields.io/badge/version-v1.0-blue.svg?style=flat">
</div><br><br>
<p>A browser extension for finding XSS vulnerabilities. It uses one of the most popular XSS discovering tool XSStrike in the backend to run the scan and then displays its output in the browser. I developed this project because I wanted a browser extension that can quickly scan the websites for XSS vulnerabilities so I decided to bring one of the most popular XSS finding tool XSStrike to the browser. You can use this extension to scan the parameters of current webpage using scan option or use the crawl option to crawl the website for finding XSS.
<div align="center">
<a href="https://github.com/tauh33dkhan/XSStrike-extension"><img src="https://i.ibb.co/F3SXmPR/XSStrike-Extension.png" alt="XSStrike-Extension" border="0"></a></div>
</p>

### Features:

- Supports Crawl, Scan, and DOM scanning features of XSStrike.
- Extracts the user cookie from the browser and then scans with cookie header.
- Allows you to add a custom request header (Ex: ```Authorization: Bearer eyjadf```)
- Provides the option to skip DOM scanning

### Install 

1. Download the repository in your webroot directory or use PHP built-in web server.
```
cd /var/www/html
git clone https://github.com/tauh33dkhan/XSStrike-extension.git

-- or -- 

git clone https://github.com/tauh33dkhan/XSStrike-extension.git
php -S 127.0.0.1:80
```

2. Install the XSStrike dependency.
```
cd ./src/XSStrike
sudo pip install -r requirements.txt
```

3. Install the extension in chrome.

- Go to extension setting chrome://extensions/
- Enable the Developer mode
- Click on load unpacked and navigate to XSStrike-extension directory click on open to load the extension.

### How to use?

- To scan parameters in the current web page URL click on scan, check/uncheck skip DOM option to enable/disable DOM scanning.

  Try on:
  ```
  https://brutelogic.com.br/multi/js-object3.php?p=
  ```
- To crawl the website use the crawl option.

  Try on:
  ```
  https://public-firing-range.appspot.com/reflected/index.html
  ```
- Use the custom header option to supply custom request headers.


## Credits

XSStrike-Extension uses <a href="https://github.com/s0md3v/XSStrike" onclick="_blank">XSStrike</a> in the backend to run the scan, I 
modified it to give web friendly output and limted the number of payload generation to 10.




