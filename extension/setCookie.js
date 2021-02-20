var _0x2f8b = [
  "tabs",
  "value",
  "get",
  "656377BgsvPe",
  "5impaOK",
  "url",
  "+++",
  "redirect",
  "remove",
  "getAll",
  "domain",
  "startsWith",
  "venetiacli.io/checkout/",
  "push",
  "86290YEmnXR",
  "https://",
  "www",
  "length",
  "330770gYFYjW",
  "https://www",
  "206273nEuZAE",
  "toString",
  "name",
  "query",
  "log",
  "join",
  "split",
  "752387xJjAsh",
  "761882BmbSGo",
  "cookies",
  "382iNuJmI",
  "path",
  "set",
  "getElementById",
  "searchParams",
  "includes",
  "3791EDExwi",
  "paypal",
  "stringify",
];
var _0x4a80 = function (_0x399bba, _0x5036c8) {
  _0x399bba = _0x399bba - 0x10a;
  var _0x2f8bcf = _0x2f8b[_0x399bba];
  return _0x2f8bcf;
};
(function (_0xd34963, _0x7c056d) {
  var _0x54053c = _0x4a80;
  while (!![]) {
    try {
      var _0x2e2e3a =
        -parseInt(_0x54053c(0x10a)) +
        parseInt(_0x54053c(0x123)) +
        -parseInt(_0x54053c(0x115)) * parseInt(_0x54053c(0x10b)) +
        parseInt(_0x54053c(0x11b)) +
        -parseInt(_0x54053c(0x122)) +
        parseInt(_0x54053c(0x119)) +
        parseInt(_0x54053c(0x125)) * parseInt(_0x54053c(0x12b));
      if (_0x2e2e3a === _0x7c056d) break;
      else _0xd34963["push"](_0xd34963["shift"]());
    } catch (_0x28bfd8) {
      _0xd34963["push"](_0xd34963["shift"]());
    }
  }
})(_0x2f8b, 0xdd679);
function setCookie(_0x42338d, _0x384e6b, _0x44bfb9, _0x3ae207) {
  var _0x2cf0f1 = _0x4a80;
  chrome[_0x2cf0f1(0x124)][_0x2cf0f1(0x10f)]({
    name: _0x42338d,
    url: _0x3ae207,
  }),
    chrome["cookies"][_0x2cf0f1(0x127)](
      { name: _0x42338d, value: _0x384e6b, domain: _0x44bfb9, url: _0x3ae207 },
      function (_0x2b6145) {
        var _0x1cefbe = _0x2cf0f1;
        console[_0x1cefbe(0x11f)](JSON[_0x1cefbe(0x12d)](_0x2b6145));
      }
    );
}
function parseCookie(_0x4d1260) {
  var _0x189ac7 = _0x4a80;
  setCookie(
    _0x4d1260[_0x189ac7(0x11d)],
    _0x4d1260[_0x189ac7(0x12f)],
    _0x4d1260[_0x189ac7(0x111)],
    _0x4d1260["url"]
  );
}
function delCookie(_0x37a245) {
  var _0x4e064e = _0x4a80;
  if (_0x37a245[_0x4e064e(0x111)] == undefined) return;
  else {
    if (_0x37a245[_0x4e064e(0x111)][_0x4e064e(0x12a)](_0x4e064e(0x12c))) return;
  }
  chrome["cookies"][_0x4e064e(0x110)](
    { domain: _0x37a245["domain"] },
    function (_0xa3f7d8) {
      var _0x4f54fa = _0x4e064e;
      for (
        var _0x181550 = 0x0;
        _0x181550 < _0xa3f7d8[_0x4f54fa(0x118)];
        _0x181550++
      ) {
        if (_0xa3f7d8[_0x181550][_0x4f54fa(0x111)][_0x4f54fa(0x112)]("."))
          url = _0x4f54fa(0x117) + _0xa3f7d8[_0x181550]["domain"];
        else
          _0xa3f7d8[_0x181550][_0x4f54fa(0x111)][_0x4f54fa(0x112)](
            _0x4f54fa(0x117)
          )
            ? (url = _0x4f54fa(0x116) + _0xa3f7d8[_0x181550]["domain"])
            : (url = _0xa3f7d8[_0x181550][_0x4f54fa(0x111)]);
        chrome[_0x4f54fa(0x124)][_0x4f54fa(0x10f)]({
          url: +_0xa3f7d8[_0x181550][_0x4f54fa(0x126)],
          name: _0xa3f7d8[_0x181550]["name"],
        });
      }
    }
  );
}
function init() {
  var _0x2b6a85 = _0x4a80;
  chrome[_0x2b6a85(0x12e)][_0x2b6a85(0x11e)](
    { active: !![], currentWindow: !![] },
    function (_0x4c1d6c) {
      var _0x34f1d9 = _0x2b6a85,
        _0x3eec05 = _0x4c1d6c[0x0][_0x34f1d9(0x10c)],
        _0xb0daa4 = new URL(_0x3eec05);
      if (_0x3eec05[_0x34f1d9(0x12a)](_0x34f1d9(0x113))) {
        var _0x3ce8a6 = decodeURIComponent(
            _0xb0daa4[_0x34f1d9(0x129)][_0x34f1d9(0x130)]("cookies")
          )
            [_0x34f1d9(0x121)]("\x20")
            [_0x34f1d9(0x120)]("+"),
          _0xfa6c6d = _0xb0daa4[_0x34f1d9(0x129)]
            [_0x34f1d9(0x130)](_0x34f1d9(0x10e))
            [_0x34f1d9(0x11c)](),
          _0x1a0ea6 = atob(_0x3ce8a6);
        _0x1a0ea6 = _0x1a0ea6[_0x34f1d9(0x121)](_0x34f1d9(0x10d));
        var _0x3082c0 = [];
        for (var _0x13e327 of _0x1a0ea6) {
          (c = _0x13e327[_0x34f1d9(0x121)]("##")),
            _0x3082c0[_0x34f1d9(0x114)]({
              name: c[0x0],
              value: c[0x1],
              domain: c[0x2],
              path: c[0x3],
              url: _0x34f1d9(0x11a) + c[0x2],
            });
        }
        _0xfa6c6d = atob(_0xfa6c6d);
        var _0x4302e9 = _0x3082c0;
        for (
          var _0x8ae8b5 = 0x0;
          _0x8ae8b5 < _0x4302e9["length"];
          _0x8ae8b5++
        ) {
          delCookie(_0x4302e9[_0x8ae8b5]);
        }
        for (var _0x1b0ded of _0x4302e9) {
          parseCookie(_0x1b0ded);
        }
        (document[_0x34f1d9(0x128)](_0x34f1d9(0x10e))["innerHTML"] =
          "Redirecting\x20to\x20" + _0xfa6c6d),
          chrome["tabs"][_0x34f1d9(0x11e)](
            { currentWindow: !![], active: !![] },
            function (_0x51b855) {
              var _0x54c3f7 = _0x34f1d9;
              chrome[_0x54c3f7(0x12e)]["update"](_0x51b855["id"], {
                url: _0xfa6c6d,
              });
            }
          );
      }
    }
  );
}
window["onload"] = init;
