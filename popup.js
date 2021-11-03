// save headers to local storage

function saveHeader(){
  customHeader = document.getElementById("customHeader").value;
  localStorage.setItem("header", customHeader);
  var status = document.getElementById('status');
  status.textContent = 'Custom headers saved!';
  setTimeout(function() {
      status.textContent = '';
    }, 5000);
}

// restore headers from local storage

function restoreHeaders() {
  document.getElementById("customHeader").value = localStorage.getItem("header");
}

// checkSkipDom function

function checkSkipDom(){
    var domCheckbox = document.getElementById("skipDom");  // Check if skip option is selected
    if (domCheckbox.checked == true) {
      skipDom = "yes";
    } else {
      skipDom = "no";
    }
    return skipDom
}

// crawl function

function crawl() {
    skipDom = checkSkipDom();
    customHeader = localStorage.getItem("header");
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
      var activeTab = tabs[0];
      if (skipDom == "yes") {
        chrome.tabs.sendMessage(activeTab.id, {"message": "crawl-skipDom", "header": customHeader}); // send skipDom crawl message
      } else {
        chrome.tabs.sendMessage(activeTab.id, {"message": "crawl", "header": customHeader});
      }
    });
}

// scan function

function scan() {
    skipDom = checkSkipDom();
    customHeader = localStorage.getItem("header");
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
      var activeTab = tabs[0];
      if (skipDom == "yes") {
        chrome.tabs.sendMessage(activeTab.id, {"message": "scan-skipDom", "header": customHeader}); // send skipDom scan message
      } else {
        chrome.tabs.sendMessage(activeTab.id, {"message": "scan", "header": customHeader});
      }
    });
}

// Restore checkbox state

function restoreCheckbox(){
  var skipDom = localStorage.getItem("skipDom");
  if (skipDom == "yes") {
    document.getElementById("skipDom").checked =  true;
  } else {
     document.getElementById("skipDom").checked = false;
  }
}

// checkbox evenlistner
document.addEventListener("DOMContentLoaded", function (event) {
  var _selector = document.getElementById('skipDom');
  _selector.addEventListener('change', function (event) {
    if (_selector.checked) {
      localStorage.setItem("skipDom","yes")
    } else {
      localStorage.setItem("skipDom","no")
    }
  });
});

document.addEventListener('DOMContentLoaded', restoreHeaders);
document.addEventListener('DOMContentLoaded', restoreCheckbox);

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("crawl").addEventListener("click", crawl);
  document.getElementById("scan").addEventListener("click", scan);
  document.getElementById("saveHeader").addEventListener('click', saveHeader);

});


