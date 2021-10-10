var _0x4498 = [
    "tabs",
    "12DILeww",
    "query",
    "domain",
    "name",
    "origin",
    "3eXqAlX",
    "length",
    "lastError",
    "remove",
    "138179HclIzX",
    "log",
    "includes",
    "set",
    "url",
    "update",
    "value",
    "forEach",
    "1230369blSrMd",
    "getAll",
    "paypal",
    "14793HgkGdd",
    "179173BTdQdX",
    "searchParams",
    "352TlFZgm",
    "1224491XPraCb",
    "1NAkUgi",
    "431nXZERz",
    "get",
    "2609WGdNWC",
    "replace",
    "parse",
    "cookies",
    "827sXHaUz",
    "stringify",
    "redirect",
  ];
  (function (_0x3146d, _0x58c813) {
    var _0x551e7b = _0xd323;
    while (!![]) {
      try {
        var _0x458c21 =
          -parseInt(_0x551e7b(0x15c)) * parseInt(_0x551e7b(0x14c)) +
          parseInt(_0x551e7b(0x143)) * parseInt(_0x551e7b(0x157)) +
          parseInt(_0x551e7b(0x148)) * -parseInt(_0x551e7b(0x158)) +
          parseInt(_0x551e7b(0x154)) +
          parseInt(_0x551e7b(0x15a)) * parseInt(_0x551e7b(0x163)) +
          -parseInt(_0x551e7b(0x15d)) * -parseInt(_0x551e7b(0x15f)) +
          -parseInt(_0x551e7b(0x15b));
        if (_0x458c21 === _0x58c813) break;
        else _0x3146d["push"](_0x3146d["shift"]());
      } catch (_0x55987d) {
        _0x3146d["push"](_0x3146d["shift"]());
      }
    }
  })(_0x4498, 0xe168f);
  function main() {
    var _0x26028f = _0xd323;
    chrome[_0x26028f(0x166)][_0x26028f(0x144)](
      { active: !![], lastFocusedWindow: !![] },
      function (_0xc87b62) {
        var _0x2d4e25 = _0x26028f,
          _0x4eebdf = _0xc87b62[0x0][_0x2d4e25(0x150)],
          _0x53d886 = new URL(_0x4eebdf);
        if (
          _0x4eebdf["toLowerCase"]()[_0x2d4e25(0x14e)]("venetiacli.io/checkout/")
        ) {
          var _0x24020b = atob(
              _0x53d886[_0x2d4e25(0x159)][_0x2d4e25(0x15e)](_0x2d4e25(0x147))
            ),
            _0x4be5e2 = atob(
              _0x53d886[_0x2d4e25(0x159)][_0x2d4e25(0x15e)](_0x2d4e25(0x165))
            ),
            _0x214620 = decodeURIComponent(
              _0x53d886[_0x2d4e25(0x159)]["get"](_0x2d4e25(0x162))
            )[_0x2d4e25(0x160)]("\x20", "+");
          (_0x214620 = atob(_0x214620)),
            (_0x214620 = _0x214620[_0x2d4e25(0x160)](/\'/g, "\x22")),
            (_0x214620 = "[" + _0x214620 + "]"),
            _0x24020b != undefined &&
              _0x24020b != "" &&
              redirect != undefined &&
              redirect != "" &&
              _0x214620 != undefined &&
              _0x214620 != "" &&
              (redirect(_0x24020b),
              (_0x214620 = JSON[_0x2d4e25(0x161)](_0x214620)),
              _0x214620[_0x2d4e25(0x153)]((_0x3e764c) => {
                deleteCookie(_0x3e764c);
              }),
              _0x214620[_0x2d4e25(0x153)]((_0xdf1b82) => {
                addCookie(_0xdf1b82);
              }),
              redirect(_0x4be5e2));
        }
      }
    );
  }
  function redirect(_0x3f9287) {
    var _0xe2491b = _0xd323;
    chrome[_0xe2491b(0x166)]["query"](
      { currentWindow: !![], active: !![] },
      function (_0x2477b3) {
        var _0x13aa29 = _0xe2491b;
        chrome[_0x13aa29(0x166)][_0x13aa29(0x151)](_0x2477b3["id"], {
          url: _0x3f9287,
        });
      }
    );
  }
  function addCookie(_0x724ee) {
    var _0x42846f = _0xd323;
    try {
      chrome[_0x42846f(0x162)][_0x42846f(0x14b)]({
        name: _0x724ee[_0x42846f(0x146)],
        url: _0x724ee[_0x42846f(0x150)],
      });
    } catch {}
    try {
      chrome[_0x42846f(0x162)][_0x42846f(0x14f)](
        {
          name: _0x724ee[_0x42846f(0x146)],
          domain: _0x724ee["domain"],
          url: _0x724ee[_0x42846f(0x150)],
          value: _0x724ee[_0x42846f(0x152)],
        },
        function (_0x3f7113) {
          var _0x1b71b2 = _0x42846f;
          console[_0x1b71b2(0x14d)](JSON[_0x1b71b2(0x164)](_0x3f7113)),
            console["log"](chrome["extension"][_0x1b71b2(0x14a)]),
            console[_0x1b71b2(0x14d)](chrome["runtime"][_0x1b71b2(0x14a)]);
        }
      );
    } catch {}
  }
  function deleteCookie(_0x394749) {
    var _0x1ba0ad = _0xd323;
    try {
      if (_0x394749[_0x1ba0ad(0x145)][_0x1ba0ad(0x14e)](_0x1ba0ad(0x156))) return;
    } catch {}
    chrome[_0x1ba0ad(0x162)][_0x1ba0ad(0x155)](
      { domain: _0x394749[_0x1ba0ad(0x145)] },
      function (_0x3d2eb6) {
        var _0x5c3d38 = _0x1ba0ad;
        try {
          for (
            var _0x3c8859 = 0x0;
            _0x3c8859 < _0x3d2eb6[_0x5c3d38(0x149)];
            _0x3c8859++
          ) {
            chrome[_0x5c3d38(0x162)][_0x5c3d38(0x14b)]({
              url: _0x394749[_0x5c3d38(0x150)],
              name: _0x3d2eb6[_0x3c8859][_0x5c3d38(0x146)],
            });
          }
        } catch {}
      }
    );
  }
  function _0xd323(_0x5e093c, _0x25e816) {
    _0x5e093c = _0x5e093c - 0x143;
    var _0x449828 = _0x4498[_0x5e093c];
    return _0x449828;
  }
  main();
  