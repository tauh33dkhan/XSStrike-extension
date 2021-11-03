browser.tabs.onUpdated.addListener(processPageAction)

function processPageAction(tabId){
    browser.pageAction.show(tabId)
}

browser.pageAction.onClicked.addListener(sendData)

function sendData(tab){
    browser.tabs.sendMessage(tab.id, {data:'dummyData'})
    browser.notifications.create({
        "type": "basic",
        "title": "XSStrike",
        "message": "Running Scan!"
    })
}
