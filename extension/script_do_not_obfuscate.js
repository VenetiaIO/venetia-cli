function main () {  
    chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true }, function (tabs) {
        var url_string = tabs[0].url;
        var url = new URL(url_string);
        
        if (url_string.toLowerCase().includes('venetiacli.io/checkout/')) {
            var originUrl = atob(url.searchParams.get("origin"));
            var redirectUrl = atob(url.searchParams.get("redirect"));
            var cookies = decodeURIComponent(url.searchParams.get("cookies")).replace(' ', "+");
            cookies = atob(cookies)
            cookies = cookies.replace(/\'/g, '"')
            cookies = '[' + cookies + ']'
  
            if (originUrl != undefined && originUrl != '' && redirect != undefined && redirect != "" && cookies != undefined && cookies != "") {
                
                redirect(originUrl)
  
                cookies = JSON.parse(cookies)
  
  
  
                cookies.forEach(cookie => {
                    deleteCookie(cookie);
                });
  
                cookies.forEach(cookie => {
                    addCookie(cookie);
                });
  
                redirect(redirectUrl)
            }
        }
    });
  }
  
  function redirect(url) {
    chrome.tabs.query({
        currentWindow: true,
        active: true
    }, function (tab) {
        chrome.tabs.update(tab.id, {
            url: url
        });
    });
  }
  
  function addCookie(cookie) {
    try{
        chrome.cookies.remove({
            "name": cookie.name,
            "url": cookie.url
        })
    }catch{}
    
    try{
        chrome.cookies.set({
            "name": cookie.name,
            "domain": cookie.domain,
            "url": cookie.url,
            "value": cookie.value
        }, function (cookie) {
            console.log(JSON.stringify(cookie));
            console.log(chrome.extension.lastError);
            console.log(chrome.runtime.lastError);
        });
    }catch{}
  }
  
  function deleteCookie(cookie) {
  
    try{
        if(cookie.domain.includes("paypal")) {
            return
        };
    
    }catch{}
  
  
    chrome.cookies.getAll({domain: cookie.domain}, function(cookies) {
  
        try{
            for(var i=0; i<cookies.length;i++) {
                chrome.cookies.remove({url: cookie.url, name: cookies[i].name});
            }
        }catch{}
  
    });
  }
  
  main();