var _0x394c = [
  "join",
  "1652860dYVxFR",
  "get",
  "update",
  "615205OzBmcz",
  "onload",
  "544903VCOsMu",
  "searchParams",
  "includes",
  "remove",
  "https://www",
  "set",
  "81029tKHmnP",
  "https://",
  "path",
  "6tPHJsN",
  "length",
  "93036CWoRfC",
  "push",
  "value",
  "toString",
  "split",
  "name",
  "startsWith",
  "329159LuzOLg",
  "paypal",
  "domain",
  "1465903EVwMwv",
  "cookies",
  "tabs",
  "www",
  "Redirecting\x20to\x20",
  "query",
  "url",
];
var _0xa05c = function (_0x520449, _0xf8e6e0) {
  _0x520449 = _0x520449 - 0x108;
  var _0x394c31 = _0x394c[_0x520449];
  return _0x394c31;
};
var _0x284c82 = _0xa05c;
(function (_0x482ff6, _0x5bdf0b) {
  var _0x3657f8 = _0xa05c;
  while (!![]) {
    try {
      var _0x2016dc =
        parseInt(_0x3657f8(0x127)) +
        -parseInt(_0x3657f8(0x115)) +
        -parseInt(_0x3657f8(0x11f)) +
        parseInt(_0x3657f8(0x11c)) +
        -parseInt(_0x3657f8(0x108)) +
        parseInt(_0x3657f8(0x110)) * parseInt(_0x3657f8(0x113)) +
        parseInt(_0x3657f8(0x10a));
      if (_0x2016dc === _0x5bdf0b) break;
      else _0x482ff6["push"](_0x482ff6["shift"]());
    } catch (_0x546787) {
      _0x482ff6["push"](_0x482ff6["shift"]());
    }
  }
})(_0x394c, 0xccd28);
function setCookie(_0x41a0a1, _0x366527, _0x5d4d63, _0x35acfc) {
  var _0x31cede = _0xa05c;
  chrome[_0x31cede(0x120)][_0x31cede(0x10d)]({
    name: _0x41a0a1,
    url: _0x35acfc,
  }),
    chrome[_0x31cede(0x120)][_0x31cede(0x10f)](
      { name: _0x41a0a1, value: _0x366527, domain: _0x5d4d63, url: _0x35acfc },
      function (_0x44290c) {
        console["log"](JSON["stringify"](_0x44290c));
      }
    );
}
function parseCookie(_0x33495e) {
  var _0x1907aa = _0xa05c;
  setCookie(
    _0x33495e[_0x1907aa(0x11a)],
    _0x33495e[_0x1907aa(0x117)],
    _0x33495e[_0x1907aa(0x11e)],
    _0x33495e[_0x1907aa(0x125)]
  );
}
function delCookie(_0x13c98e) {
  var _0x136add = _0xa05c;
  if (_0x13c98e[_0x136add(0x11e)] == undefined) return;
  else {
    if (_0x13c98e[_0x136add(0x11e)][_0x136add(0x10c)](_0x136add(0x11d))) return;
  }
  chrome[_0x136add(0x120)]["getAll"](
    { domain: _0x13c98e[_0x136add(0x11e)] },
    function (_0x379851) {
      var _0x203c9b = _0x136add;
      for (
        var _0x2fe508 = 0x0;
        _0x2fe508 < _0x379851[_0x203c9b(0x114)];
        _0x2fe508++
      ) {
        if (_0x379851[_0x2fe508][_0x203c9b(0x11e)][_0x203c9b(0x11b)]("."))
          url = _0x203c9b(0x122) + _0x379851[_0x2fe508][_0x203c9b(0x11e)];
        else
          _0x379851[_0x2fe508][_0x203c9b(0x11e)][_0x203c9b(0x11b)](
            _0x203c9b(0x122)
          )
            ? (url = _0x203c9b(0x111) + _0x379851[_0x2fe508][_0x203c9b(0x11e)])
            : (url = _0x379851[_0x2fe508]["domain"]);
        chrome[_0x203c9b(0x120)][_0x203c9b(0x10d)]({
          url: +_0x379851[_0x2fe508][_0x203c9b(0x112)],
          name: _0x379851[_0x2fe508][_0x203c9b(0x11a)],
        });
      }
    }
  );
}
function init() {
  chrome["tabs"]["query"](
    { active: !![], currentWindow: !![] },
    function (_0x350622) {
      var _0x28cae8 = _0xa05c,
        _0x4d085f = _0x350622[0x0][_0x28cae8(0x125)],
        _0x13dd66 = new URL(_0x4d085f);
      if (_0x4d085f[_0x28cae8(0x10c)]("venetiacli.io/api/checkout/")) {
        var _0x32e603 = decodeURIComponent(
            _0x13dd66[_0x28cae8(0x10b)][_0x28cae8(0x128)]("cookies")
          )
            [_0x28cae8(0x119)]("\x20")
            [_0x28cae8(0x126)]("+"),
          _0x5d4dc2 = _0x13dd66[_0x28cae8(0x10b)]
            [_0x28cae8(0x128)]("redirect")
            [_0x28cae8(0x118)](),
          _0x1b263c = atob(_0x32e603);
        _0x1b263c = _0x1b263c[_0x28cae8(0x119)]("+++");
        var _0x1032e6 = [];
        for (var _0x29151f of _0x1b263c) {
          (c = _0x29151f[_0x28cae8(0x119)]("##")),
            _0x1032e6[_0x28cae8(0x116)]({
              name: c[0x0],
              value: c[0x1],
              domain: c[0x2],
              path: c[0x3],
              url: _0x28cae8(0x10e) + c[0x2],
            });
        }
        _0x5d4dc2 = atob(_0x5d4dc2);
        var _0xdb68f2 = _0x1032e6;
        for (
          var _0x5b399c = 0x0;
          _0x5b399c < _0xdb68f2[_0x28cae8(0x114)];
          _0x5b399c++
        ) {
          delCookie(_0xdb68f2[_0x5b399c]);
        }
        for (var _0x48c3a4 of _0xdb68f2) {
          parseCookie(_0x48c3a4);
        }
        (document["getElementById"]("redirect")["innerHTML"] =
          _0x28cae8(0x123) + _0x5d4dc2),
          chrome[_0x28cae8(0x121)][_0x28cae8(0x124)](
            { currentWindow: !![], active: !![] },
            function (_0x16ec51) {
              var _0x260704 = _0x28cae8;
              chrome[_0x260704(0x121)][_0x260704(0x129)](_0x16ec51["id"], {
                url: _0x5d4dc2,
              });
            }
          );
      }
    }
  );
}
window[_0x284c82(0x109)] = init;
