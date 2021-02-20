
function setCookie(cName, cValue, cDomain, cURL) {

  chrome.cookies.remove({
      'name': cName,
      'url': cURL
  })

  chrome.cookies.set({
      'name': cName,
      'value': cValue,
      'domain': cDomain,
      'url': cURL
  }, function(cookie) {
      console.log(JSON.stringify(cookie));
  });
}

function parseCookie(cookie) {
  setCookie(cookie['name'], cookie['value'], cookie['domain'], cookie['url']);
}

function delCookie(cookie) {
  if (cookie['domain'] == undefined) return;
  else if (cookie['domain'].includes('paypal')) return;

  chrome.cookies.getAll({domain: cookie['domain']}, function(cookies) {
      for (var i=0; i<cookies.length; i++) {
          if (cookies[i].domain.startsWith('.')) {
              url = 'www' + cookies[i].domain;
          } else if (cookies[i].domain.startsWith('www')) {
              url = 'https://' + cookies[i].domain;
          } else {
              url = cookies[i].domain;
          }

          chrome.cookies.remove({url: + cookies[i].path, name: cookies[i].name});
      }
  });
}

function init() {
  chrome.tabs.query({
      'active': true,
      'currentWindow':true
  }, function (tabs) {
      var urlstring = tabs[0].url;
      var url = new URL(urlstring);

      if (urlstring.includes('venetiacli.io/checkout/')) {
          var cookieStr = decodeURIComponent(url.searchParams.get('cookies')).split(' ').join('+');
          var redirect = url.searchParams.get('redirect').toString();

          //  '[{}*{}*{}*{}]'
          var cookieString = atob(cookieStr)

          cookieString = cookieString.split('+++')
          var cookieList = []
          for (var a of cookieString) {
              c = a.split('##')
              cookieList.push({
                  name:c[0],
                  value:c[1],
                  domain:c[2],
                  path:c[3],
                  url:'https://www' + c[2]
              })
          }
          redirect = atob(redirect);

              
          var cookies = cookieList
          // try{
              // cookies = JSON.parse(cookieStr);
          // }catch(e){
              // cookies = JSON.parse(JSON.stringify(cookieStr))
          // }

          for (var i=0; i < cookies.length; i++) {
              delCookie(cookies[i]);
          }

          for (var cookie of cookies) {
              parseCookie(cookie);
          }

          document.getElementById('redirect').innerHTML = 'Redirecting to ' + redirect;

          chrome.tabs.query({
              currentWindow: true,
              active: true
          }, function (tab) {
              chrome.tabs.update(tab.id, {
                  url: redirect
              });
          });
      }
  });
}

window.onload = init;