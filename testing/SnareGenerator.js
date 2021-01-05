var navigator = {
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    cookieEnabled: true,
    deviceMemory: 8,
    doNotTrack: null,
    hardwareConcurrency: 4,
    language: "en-US",
    languages: ["en-US", "en"],
    maxTouchPoints: 0,
    onLine: true,
    platform: "Win32",
    product: "Gecko",
    productSub: "20030107",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    vendor: "Google Inc.",
    vendorSub: "",
    plugins:[
        {
            description: "Portable Document Format",
            filename: "internal-pdf-viewer",
            length: 1,
            name: "Chrome PDF Plugin"
        },
        {
            description: "",
            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
            length: 1,
            name: "Chrome PDF Plugin"
        },
        {
            description: "",
            filename: "internal-nacl-plugin",
            length: 2,
            name: "Native Client"
        }

    ]
}

var _i_ac = {
    __if_ay: function (_if_gx) {
      if (_if_gx === null || typeof _if_gx === "undefined") {
        return "";
      }
      var _i_ad = _if_gx + "";
      var _i_ae = "",
        start,
        end,
        stringl = 0;
      start = end = 0;
      stringl = _i_ad.length;
      for (var _i_af = 0; _i_af < stringl; _i_af++) {
        var _i_ag = _i_ad.charCodeAt(_i_af);
        var _i_ah = null;
        if (_i_ag < 128) {
          end++;
        } else if (_i_ag > 127 && _i_ag < 2048) {
          _i_ah =
            String.fromCharCode((_i_ag >> 6) | 192) +
            String.fromCharCode((_i_ag & 63) | 128);
        } else {
          _i_ah =
            String.fromCharCode((_i_ag >> 12) | 224) +
            String.fromCharCode(((_i_ag >> 6) & 63) | 128) +
            String.fromCharCode((_i_ag & 63) | 128);
        }
        if (_i_ah !== null) {
          if (end > start) {
            _i_ae += _i_ad.slice(start, end);
          }
          _i_ae += _i_ah;
          start = end = _i_af + 1;
        }
      }
      if (end > start) {
        _i_ae += _i_ad.slice(start, stringl);
      }
      return _i_ae;
    },
    __if_bi: function (_i_al) {
      var _i_ai = function (_if_gz, _if_gy) {
        var _i_aj = (_if_gz << _if_gy) | (_if_gz >>> (32 - _if_gy));
        return _i_aj;
      };
      var _i_ak = function (_if_ha) {
        var _i_al = "";
        var _i_am;
        var _i_an;
        for (_i_am = 7; _i_am >= 0; _i_am--) {
          _i_an = (_if_ha >>> (_i_am * 4)) & 0x0f;
          _i_al += _i_an.toString(16);
        }
        return _i_al;
      };
      var _i_ao;
      var _i_g, _i_bl;
      var _i_ap = new Array(80);
      var _i_aq = 0x67452301;
      var _i_ar = 0xefcdab89;
      var _i_as = 0x98badcfe;
      var _i_at = 0x10325476;
      var _i_au = 0xc3d2e1f0;
      var _i_av, A2, A3, A4, A5;
      var _i_aw;
      _i_al = this.__if_ay(_i_al);
      var _i_ax = _i_al.length;
      var _i_ay = [];
      for (_i_g = 0; _i_g < _i_ax - 3; _i_g += 4) {
        _i_bl =
          (_i_al.charCodeAt(_i_g) << 24) |
          (_i_al.charCodeAt(_i_g + 1) << 16) |
          (_i_al.charCodeAt(_i_g + 2) << 8) |
          _i_al.charCodeAt(_i_g + 3);
        _i_ay.push(_i_bl);
      }
      switch (_i_ax % 4) {
        case 0:
          _i_g = 0x080000000;
          break;
        case 1:
          _i_g = (_i_al.charCodeAt(_i_ax - 1) << 24) | 0x0800000;
          break;
        case 2:
          _i_g =
            (_i_al.charCodeAt(_i_ax - 2) << 24) |
            (_i_al.charCodeAt(_i_ax - 1) << 16) |
            0x08000;
          break;
        case 3:
          _i_g =
            (_i_al.charCodeAt(_i_ax - 3) << 24) |
            (_i_al.charCodeAt(_i_ax - 2) << 16) |
            (_i_al.charCodeAt(_i_ax - 1) << 8) |
            0x80;
          break;
      }
      _i_ay.push(_i_g);
      while (_i_ay.length % 16 != 14) {
        _i_ay.push(0);
      }
      _i_ay.push(_i_ax >>> 29);
      _i_ay.push((_i_ax << 3) & 0x0ffffffff);
      for (_i_ao = 0; _i_ao < _i_ay.length; _i_ao += 16) {
        for (_i_g = 0; _i_g < 16; _i_g++) {
          _i_ap[_i_g] = _i_ay[_i_ao + _i_g];
        }
        for (_i_g = 16; _i_g <= 79; _i_g++) {
          _i_ap[_i_g] = _i_ai(
            _i_ap[_i_g - 3] ^
              _i_ap[_i_g - 8] ^
              _i_ap[_i_g - 14] ^
              _i_ap[_i_g - 16],
            1
          );
        }
        _i_av = _i_aq;
        A2 = _i_ar;
        A3 = _i_as;
        A4 = _i_at;
        A5 = _i_au;
        for (_i_g = 0; _i_g <= 19; _i_g++) {
          _i_aw =
            (_i_ai(_i_av, 5) +
              ((A2 & A3) | (~A2 & A4)) +
              A5 +
              _i_ap[_i_g] +
              0x5a827999) &
            0x0ffffffff;
          A5 = A4;
          A4 = A3;
          A3 = _i_ai(A2, 30);
          A2 = _i_av;
          _i_av = _i_aw;
        }
        for (_i_g = 20; _i_g <= 39; _i_g++) {
          _i_aw =
            (_i_ai(_i_av, 5) + (A2 ^ A3 ^ A4) + A5 + _i_ap[_i_g] + 0x6ed9eba1) &
            0x0ffffffff;
          A5 = A4;
          A4 = A3;
          A3 = _i_ai(A2, 30);
          A2 = _i_av;
          _i_av = _i_aw;
        }
        for (_i_g = 40; _i_g <= 59; _i_g++) {
          _i_aw =
            (_i_ai(_i_av, 5) +
              ((A2 & A3) | (A2 & A4) | (A3 & A4)) +
              A5 +
              _i_ap[_i_g] +
              0x8f1bbcdc) &
            0x0ffffffff;
          A5 = A4;
          A4 = A3;
          A3 = _i_ai(A2, 30);
          A2 = _i_av;
          _i_av = _i_aw;
        }
        for (_i_g = 60; _i_g <= 79; _i_g++) {
          _i_aw =
            (_i_ai(_i_av, 5) + (A2 ^ A3 ^ A4) + A5 + _i_ap[_i_g] + 0xca62c1d6) &
            0x0ffffffff;
          A5 = A4;
          A4 = A3;
          A3 = _i_ai(A2, 30);
          A2 = _i_av;
          _i_av = _i_aw;
        }
        _i_aq = (_i_aq + _i_av) & 0x0ffffffff;
        _i_ar = (_i_ar + A2) & 0x0ffffffff;
        _i_as = (_i_as + A3) & 0x0ffffffff;
        _i_at = (_i_at + A4) & 0x0ffffffff;
        _i_au = (_i_au + A5) & 0x0ffffffff;
      }
      _i_aw =
        _i_ak(_i_aq) + _i_ak(_i_ar) + _i_ak(_i_as) + _i_ak(_i_at) + _i_ak(_i_au);
      return _i_aw.toLowerCase();
    },
    __if_bv: function (_if_hb, _if_gp) {
      try {
        var _i_az = [
          0x1010400,
          0,
          0x10000,
          0x1010404,
          0x1010004,
          0x10404,
          0x4,
          0x10000,
          0x400,
          0x1010400,
          0x1010404,
          0x400,
          0x1000404,
          0x1010004,
          0x1000000,
          0x4,
          0x404,
          0x1000400,
          0x1000400,
          0x10400,
          0x10400,
          0x1010000,
          0x1010000,
          0x1000404,
          0x10004,
          0x1000004,
          0x1000004,
          0x10004,
          0,
          0x404,
          0x10404,
          0x1000000,
          0x10000,
          0x1010404,
          0x4,
          0x1010000,
          0x1010400,
          0x1000000,
          0x1000000,
          0x400,
          0x1010004,
          0x10000,
          0x10400,
          0x1000004,
          0x400,
          0x4,
          0x1000404,
          0x10404,
          0x1010404,
          0x10004,
          0x1010000,
          0x1000404,
          0x1000004,
          0x404,
          0x10404,
          0x1010400,
          0x404,
          0x1000400,
          0x1000400,
          0,
          0x10004,
          0x10400,
          0,
          0x1010004,
        ];
        var _i_ba = [
          -0x7fef7fe0,
          -0x7fff8000,
          0x8000,
          0x108020,
          0x100000,
          0x20,
          -0x7fefffe0,
          -0x7fff7fe0,
          -0x7fffffe0,
          -0x7fef7fe0,
          -0x7fef8000,
          -0x80000000,
          -0x7fff8000,
          0x100000,
          0x20,
          -0x7fefffe0,
          0x108000,
          0x100020,
          -0x7fff7fe0,
          0,
          -0x80000000,
          0x8000,
          0x108020,
          -0x7ff00000,
          0x100020,
          -0x7fffffe0,
          0,
          0x108000,
          0x8020,
          -0x7fef8000,
          -0x7ff00000,
          0x8020,
          0,
          0x108020,
          -0x7fefffe0,
          0x100000,
          -0x7fff7fe0,
          -0x7ff00000,
          -0x7fef8000,
          0x8000,
          -0x7ff00000,
          -0x7fff8000,
          0x20,
          -0x7fef7fe0,
          0x108020,
          0x20,
          0x8000,
          -0x80000000,
          0x8020,
          -0x7fef8000,
          0x100000,
          -0x7fffffe0,
          0x100020,
          -0x7fff7fe0,
          -0x7fffffe0,
          0x100020,
          0x108000,
          0,
          -0x7fff8000,
          0x8020,
          -0x80000000,
          -0x7fefffe0,
          -0x7fef7fe0,
          0x108000,
        ];
        var _i_bb = [
          0x208,
          0x8020200,
          0,
          0x8020008,
          0x8000200,
          0,
          0x20208,
          0x8000200,
          0x20008,
          0x8000008,
          0x8000008,
          0x20000,
          0x8020208,
          0x20008,
          0x8020000,
          0x208,
          0x8000000,
          0x8,
          0x8020200,
          0x200,
          0x20200,
          0x8020000,
          0x8020008,
          0x20208,
          0x8000208,
          0x20200,
          0x20000,
          0x8000208,
          0x8,
          0x8020208,
          0x200,
          0x8000000,
          0x8020200,
          0x8000000,
          0x20008,
          0x208,
          0x20000,
          0x8020200,
          0x8000200,
          0,
          0x200,
          0x20008,
          0x8020208,
          0x8000200,
          0x8000008,
          0x200,
          0,
          0x8020008,
          0x8000208,
          0x20000,
          0x8000000,
          0x8020208,
          0x8,
          0x20208,
          0x20200,
          0x8000008,
          0x8020000,
          0x8000208,
          0x208,
          0x8020000,
          0x20208,
          0x8,
          0x8020008,
          0x20200,
        ];
        var _i_bc = [
          0x802001,
          0x2081,
          0x2081,
          0x80,
          0x802080,
          0x800081,
          0x800001,
          0x2001,
          0,
          0x802000,
          0x802000,
          0x802081,
          0x81,
          0,
          0x800080,
          0x800001,
          0x1,
          0x2000,
          0x800000,
          0x802001,
          0x80,
          0x800000,
          0x2001,
          0x2080,
          0x800081,
          0x1,
          0x2080,
          0x800080,
          0x2000,
          0x802080,
          0x802081,
          0x81,
          0x800080,
          0x800001,
          0x802000,
          0x802081,
          0x81,
          0,
          0,
          0x802000,
          0x2080,
          0x800080,
          0x800081,
          0x1,
          0x802001,
          0x2081,
          0x2081,
          0x80,
          0x802081,
          0x81,
          0x1,
          0x2000,
          0x800001,
          0x2001,
          0x802080,
          0x800081,
          0x2001,
          0x2080,
          0x800000,
          0x802001,
          0x80,
          0x800000,
          0x2000,
          0x802080,
        ];
        var _i_bd = [
          0x100,
          0x2080100,
          0x2080000,
          0x42000100,
          0x80000,
          0x100,
          0x40000000,
          0x2080000,
          0x40080100,
          0x80000,
          0x2000100,
          0x40080100,
          0x42000100,
          0x42080000,
          0x80100,
          0x40000000,
          0x2000000,
          0x40080000,
          0x40080000,
          0,
          0x40000100,
          0x42080100,
          0x42080100,
          0x2000100,
          0x42080000,
          0x40000100,
          0,
          0x42000000,
          0x2080100,
          0x2000000,
          0x42000000,
          0x80100,
          0x80000,
          0x42000100,
          0x100,
          0x2000000,
          0x40000000,
          0x2080000,
          0x42000100,
          0x40080100,
          0x2000100,
          0x40000000,
          0x42080000,
          0x2080100,
          0x40080100,
          0x100,
          0x2000000,
          0x42080000,
          0x42080100,
          0x80100,
          0x42000000,
          0x42080100,
          0x2080000,
          0,
          0x40080000,
          0x42000000,
          0x80100,
          0x2000100,
          0x40000100,
          0x80000,
          0,
          0x40080000,
          0x2080100,
          0x40000100,
        ];
        var _i_be = [
          0x20000010,
          0x20400000,
          0x4000,
          0x20404010,
          0x20400000,
          0x10,
          0x20404010,
          0x400000,
          0x20004000,
          0x404010,
          0x400000,
          0x20000010,
          0x400010,
          0x20004000,
          0x20000000,
          0x4010,
          0,
          0x400010,
          0x20004010,
          0x4000,
          0x404000,
          0x20004010,
          0x10,
          0x20400010,
          0x20400010,
          0,
          0x404010,
          0x20404000,
          0x4010,
          0x404000,
          0x20404000,
          0x20000000,
          0x20004000,
          0x10,
          0x20400010,
          0x404000,
          0x20404010,
          0x400000,
          0x4010,
          0x20000010,
          0x400000,
          0x20004000,
          0x20000000,
          0x4010,
          0x20000010,
          0x20404010,
          0x404000,
          0x20400000,
          0x404010,
          0x20404000,
          0,
          0x20400010,
          0x10,
          0x4000,
          0x20400000,
          0x404010,
          0x4000,
          0x400010,
          0x20004010,
          0,
          0x20404000,
          0x20000000,
          0x400010,
          0x20004010,
        ];
        var _i_bf = [
          0x200000,
          0x4200002,
          0x4000802,
          0,
          0x800,
          0x4000802,
          0x200802,
          0x4200800,
          0x4200802,
          0x200000,
          0,
          0x4000002,
          0x2,
          0x4000000,
          0x4200002,
          0x802,
          0x4000800,
          0x200802,
          0x200002,
          0x4000800,
          0x4000002,
          0x4200000,
          0x4200800,
          0x200002,
          0x4200000,
          0x800,
          0x802,
          0x4200802,
          0x200800,
          0x2,
          0x4000000,
          0x200800,
          0x4000000,
          0x200800,
          0x200000,
          0x4000802,
          0x4000802,
          0x4200002,
          0x4200002,
          0x2,
          0x200002,
          0x4000000,
          0x4000800,
          0x200000,
          0x4200800,
          0x802,
          0x200802,
          0x4200800,
          0x802,
          0x4000002,
          0x4200802,
          0x4200000,
          0x200800,
          0,
          0x2,
          0x4200802,
          0,
          0x200802,
          0x4200000,
          0x800,
          0x4000002,
          0x4000800,
          0x800,
          0x200002,
        ];
        var _i_bg = [
          0x10001040,
          0x1000,
          0x40000,
          0x10041040,
          0x10000000,
          0x10001040,
          0x40,
          0x10000000,
          0x40040,
          0x10040000,
          0x10041040,
          0x41000,
          0x10041000,
          0x41040,
          0x1000,
          0x40,
          0x10040000,
          0x10000040,
          0x10001000,
          0x1040,
          0x41000,
          0x40040,
          0x10040040,
          0x10041000,
          0x1040,
          0,
          0,
          0x10040040,
          0x10000040,
          0x10001000,
          0x41040,
          0x40000,
          0x41040,
          0x40000,
          0x10041000,
          0x1000,
          0x40,
          0x10040040,
          0x1000,
          0x41040,
          0x10001000,
          0x40,
          0x10000040,
          0x10040000,
          0x10040040,
          0x10000000,
          0x40000,
          0x10001040,
          0,
          0x10041040,
          0x40040,
          0x10000040,
          0x10040000,
          0x10001000,
          0x10001040,
          0,
          0x10041040,
          0x41000,
          0x41000,
          0x1040,
          0x1040,
          0x40040,
          0x10000000,
          0x10041000,
        ];
        var _i_bh = _i_ac.__if_cj(_if_hb);
        var _i_bi = 0;
        var _i_bj = _if_gp.length;
        var _i_bk = 0;
        var _i_g;
        var _i_bl;
        var _i_aw;
        var _i_bm;
        var _i_bn;
        var _i_bo;
        var _i_bp;
        var _i_bq;
        var _i_br = [0, 32, 2];
        var _i_bs;
        var _i_bt;
        var _i_bu;
        var _i_bv;
        var _i_bw;
        var _i_bx;
        var _i_by = 3;
        _if_gp += "\0\0\0\0\0\0\0\0";
        var _i_e = "";
        var _i_bz = "";
        while (_i_bi < _i_bj) {
          _i_bp =
            (_if_gp.charCodeAt(_i_bi++) << 24) ^
            (_if_gp.charCodeAt(_i_bi++) << 16) ^
            (_if_gp.charCodeAt(_i_bi++) << 8) ^
            _if_gp.charCodeAt(_i_bi++);
          _i_bq =
            (_if_gp.charCodeAt(_i_bi++) << 24) ^
            (_if_gp.charCodeAt(_i_bi++) << 16) ^
            (_if_gp.charCodeAt(_i_bi++) << 8) ^
            _if_gp.charCodeAt(_i_bi++);
          _i_aw = ((_i_bp >>> 4) ^ _i_bq) & 0x0f0f0f0f;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 4;
          _i_aw = ((_i_bp >>> 16) ^ _i_bq) & 0x0000ffff;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 16;
          _i_aw = ((_i_bq >>> 2) ^ _i_bp) & 0x33333333;
          _i_bp ^= _i_aw;
          _i_bq ^= _i_aw << 2;
          _i_aw = ((_i_bq >>> 8) ^ _i_bp) & 0x00ff00ff;
          _i_bp ^= _i_aw;
          _i_bq ^= _i_aw << 8;
          _i_aw = ((_i_bp >>> 1) ^ _i_bq) & 0x55555555;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 1;
          _i_bp = (_i_bp << 1) | (_i_bp >>> 31);
          _i_bq = (_i_bq << 1) | (_i_bq >>> 31);
          for (_i_bl = 0; _i_bl < _i_by; _i_bl += 3) {
            _i_bw = _i_br[_i_bl + 1];
            _i_bx = _i_br[_i_bl + 2];
            for (_i_g = _i_br[_i_bl]; _i_g != _i_bw; _i_g += _i_bx) {
              _i_bn = _i_bq ^ _i_bh[_i_g];
              _i_bo = ((_i_bq >>> 4) | (_i_bq << 28)) ^ _i_bh[_i_g + 1];
              _i_aw = _i_bp;
              _i_bp = _i_bq;
              _i_bq =
                _i_aw ^
                (_i_ba[(_i_bn >>> 24) & 0x3f] |
                  _i_bc[(_i_bn >>> 16) & 0x3f] |
                  _i_be[(_i_bn >>> 8) & 0x3f] |
                  _i_bg[_i_bn & 0x3f] |
                  _i_az[(_i_bo >>> 24) & 0x3f] |
                  _i_bb[(_i_bo >>> 16) & 0x3f] |
                  _i_bd[(_i_bo >>> 8) & 0x3f] |
                  _i_bf[_i_bo & 0x3f]);
            }
            _i_aw = _i_bp;
            _i_bp = _i_bq;
            _i_bq = _i_aw;
          }
          _i_bp = (_i_bp >>> 1) | (_i_bp << 31);
          _i_bq = (_i_bq >>> 1) | (_i_bq << 31);
          _i_aw = ((_i_bp >>> 1) ^ _i_bq) & 0x55555555;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 1;
          _i_aw = ((_i_bq >>> 8) ^ _i_bp) & 0x00ff00ff;
          _i_bp ^= _i_aw;
          _i_bq ^= _i_aw << 8;
          _i_aw = ((_i_bq >>> 2) ^ _i_bp) & 0x33333333;
          _i_bp ^= _i_aw;
          _i_bq ^= _i_aw << 2;
          _i_aw = ((_i_bp >>> 16) ^ _i_bq) & 0x0000ffff;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 16;
          _i_aw = ((_i_bp >>> 4) ^ _i_bq) & 0x0f0f0f0f;
          _i_bq ^= _i_aw;
          _i_bp ^= _i_aw << 4;
          _i_bz += String.fromCharCode(
            _i_bp >>> 24,
            (_i_bp >>> 16) & 0xff,
            (_i_bp >>> 8) & 0xff,
            _i_bp & 0xff,
            _i_bq >>> 24,
            (_i_bq >>> 16) & 0xff,
            (_i_bq >>> 8) & 0xff,
            _i_bq & 0xff
          );
          _i_bk += 8;
          if (_i_bk == 512) {
            _i_e += _i_bz;
            _i_bz = "";
            _i_bk = 0;
          }
        }
      } catch (e) {
          console.log(e)
      }
      return _i_e + _i_bz;
    },
    __if_cj: function (_if_hb) {
      var _i_ca = [
        0,
        0x4,
        0x20000000,
        0x20000004,
        0x10000,
        0x10004,
        0x20010000,
        0x20010004,
        0x200,
        0x204,
        0x20000200,
        0x20000204,
        0x10200,
        0x10204,
        0x20010200,
        0x20010204,
      ];
      var _i_cb = [
        0,
        0x1,
        0x100000,
        0x100001,
        0x4000000,
        0x4000001,
        0x4100000,
        0x4100001,
        0x100,
        0x101,
        0x100100,
        0x100101,
        0x4000100,
        0x4000101,
        0x4100100,
        0x4100101,
      ];
      var _i_cc = [
        0,
        0x8,
        0x800,
        0x808,
        0x1000000,
        0x1000008,
        0x1000800,
        0x1000808,
        0,
        0x8,
        0x800,
        0x808,
        0x1000000,
        0x1000008,
        0x1000800,
        0x1000808,
      ];
      var _i_cd = [
        0,
        0x200000,
        0x8000000,
        0x8200000,
        0x2000,
        0x202000,
        0x8002000,
        0x8202000,
        0x20000,
        0x220000,
        0x8020000,
        0x8220000,
        0x22000,
        0x222000,
        0x8022000,
        0x8222000,
      ];
      var _i_ce = [
        0,
        0x40000,
        0x10,
        0x40010,
        0,
        0x40000,
        0x10,
        0x40010,
        0x1000,
        0x41000,
        0x1010,
        0x41010,
        0x1000,
        0x41000,
        0x1010,
        0x41010,
      ];
      var _i_cf = [
        0,
        0x400,
        0x20,
        0x420,
        0,
        0x400,
        0x20,
        0x420,
        0x2000000,
        0x2000400,
        0x2000020,
        0x2000420,
        0x2000000,
        0x2000400,
        0x2000020,
        0x2000420,
      ];
      var _i_cg = [
        0,
        0x10000000,
        0x80000,
        0x10080000,
        0x2,
        0x10000002,
        0x80002,
        0x10080002,
        0,
        0x10000000,
        0x80000,
        0x10080000,
        0x2,
        0x10000002,
        0x80002,
        0x10080002,
      ];
      var _i_ch = [
        0,
        0x10000,
        0x800,
        0x10800,
        0x20000000,
        0x20010000,
        0x20000800,
        0x20010800,
        0x20000,
        0x30000,
        0x20800,
        0x30800,
        0x20020000,
        0x20030000,
        0x20020800,
        0x20030800,
      ];
      var _i_ci = [
        0,
        0x40000,
        0,
        0x40000,
        0x2,
        0x40002,
        0x2,
        0x40002,
        0x2000000,
        0x2040000,
        0x2000000,
        0x2040000,
        0x2000002,
        0x2040002,
        0x2000002,
        0x2040002,
      ];
      var _i_cj = [
        0,
        0x10000000,
        0x8,
        0x10000008,
        0,
        0x10000000,
        0x8,
        0x10000008,
        0x400,
        0x10000400,
        0x408,
        0x10000408,
        0x400,
        0x10000400,
        0x408,
        0x10000408,
      ];
      var _i_ck = [
        0,
        0x20,
        0,
        0x20,
        0x100000,
        0x100020,
        0x100000,
        0x100020,
        0x2000,
        0x2020,
        0x2000,
        0x2020,
        0x102000,
        0x102020,
        0x102000,
        0x102020,
      ];
      var _i_cl = [
        0,
        0x1000000,
        0x200,
        0x1000200,
        0x200000,
        0x1200000,
        0x200200,
        0x1200200,
        0x4000000,
        0x5000000,
        0x4000200,
        0x5000200,
        0x4200000,
        0x5200000,
        0x4200200,
        0x5200200,
      ];
      var _i_cm = [
        0,
        0x1000,
        0x8000000,
        0x8001000,
        0x80000,
        0x81000,
        0x8080000,
        0x8081000,
        0x10,
        0x1010,
        0x8000010,
        0x8001010,
        0x80010,
        0x81010,
        0x8080010,
        0x8081010,
      ];
      var _i_cn = [
        0,
        0x4,
        0x100,
        0x104,
        0,
        0x4,
        0x100,
        0x104,
        0x1,
        0x5,
        0x101,
        0x105,
        0x1,
        0x5,
        0x101,
        0x105,
      ];
      var _i_bh = [32];
      var _i_co = [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0];
      var _i_cp;
      var _i_cq;
      var _i_aw;
      var _i_bi = 0;
      var _i_af = 0;
      var _i_bp =
        (_if_hb.charCodeAt(_i_bi++) << 24) |
        (_if_hb.charCodeAt(_i_bi++) << 16) |
        (_if_hb.charCodeAt(_i_bi++) << 8) |
        _if_hb.charCodeAt(_i_bi++);
      var _i_bq =
        (_if_hb.charCodeAt(_i_bi++) << 24) |
        (_if_hb.charCodeAt(_i_bi++) << 16) |
        (_if_hb.charCodeAt(_i_bi++) << 8) |
        _if_hb.charCodeAt(_i_bi++);
      _i_aw = ((_i_bp >>> 4) ^ _i_bq) & 0x0f0f0f0f;
      _i_bq ^= _i_aw;
      _i_bp ^= _i_aw << 4;
      _i_aw = ((_i_bq >>> -16) ^ _i_bp) & 0x0000ffff;
      _i_bp ^= _i_aw;
      _i_bq ^= _i_aw << -16;
      _i_aw = ((_i_bp >>> 2) ^ _i_bq) & 0x33333333;
      _i_bq ^= _i_aw;
      _i_bp ^= _i_aw << 2;
      _i_aw = ((_i_bq >>> -16) ^ _i_bp) & 0x0000ffff;
      _i_bp ^= _i_aw;
      _i_bq ^= _i_aw << -16;
      _i_aw = ((_i_bp >>> 1) ^ _i_bq) & 0x55555555;
      _i_bq ^= _i_aw;
      _i_bp ^= _i_aw << 1;
      _i_aw = ((_i_bq >>> 8) ^ _i_bp) & 0x00ff00ff;
      _i_bp ^= _i_aw;
      _i_bq ^= _i_aw << 8;
      _i_aw = ((_i_bp >>> 1) ^ _i_bq) & 0x55555555;
      _i_bq ^= _i_aw;
      _i_bp ^= _i_aw << 1;
      _i_aw = (_i_bp << 8) | ((_i_bq >>> 20) & 0x000000f0);
      _i_bp =
        (_i_bq << 24) |
        ((_i_bq << 8) & 0xff0000) |
        ((_i_bq >>> 8) & 0xff00) |
        ((_i_bq >>> 24) & 0xf0);
      _i_bq = _i_aw;
      for (var _i_g = 0; _i_g < _i_co.length; _i_g++) {
        if (_i_co[_i_g]) {
          _i_bp = (_i_bp << 2) | (_i_bp >>> 26);
          _i_bq = (_i_bq << 2) | (_i_bq >>> 26);
        } else {
          _i_bp = (_i_bp << 1) | (_i_bp >>> 27);
          _i_bq = (_i_bq << 1) | (_i_bq >>> 27);
        }
        _i_bp &= -0xf;
        _i_bq &= -0xf;
        _i_cp =
          _i_ca[_i_bp >>> 28] |
          _i_cb[(_i_bp >>> 24) & 0xf] |
          _i_cc[(_i_bp >>> 20) & 0xf] |
          _i_cd[(_i_bp >>> 16) & 0xf] |
          _i_ce[(_i_bp >>> 12) & 0xf] |
          _i_cf[(_i_bp >>> 8) & 0xf] |
          _i_cg[(_i_bp >>> 4) & 0xf];
        _i_cq =
          _i_ch[_i_bq >>> 28] |
          _i_ci[(_i_bq >>> 24) & 0xf] |
          _i_cj[(_i_bq >>> 20) & 0xf] |
          _i_ck[(_i_bq >>> 16) & 0xf] |
          _i_cl[(_i_bq >>> 12) & 0xf] |
          _i_cm[(_i_bq >>> 8) & 0xf] |
          _i_cn[(_i_bq >>> 4) & 0xf];
        _i_aw = ((_i_cq >>> 16) ^ _i_cp) & 0x0000ffff;
        _i_bh[_i_af++] = _i_cp ^ _i_aw;
        _i_bh[_i_af++] = _i_cq ^ (_i_aw << 16);
      }
      return _i_bh;
    },
};

var _i_d = {
    __if_o: function (_if_gs) {
      return (
        _if_gs.getUTCFullYear() +
        "/" +
        this.__if_ac((_if_gs.getUTCMonth() + 1).toString(), 2) +
        "/" +
        this.__if_ac(_if_gs.getUTCDate().toString(), 2) +
        " " +
        this.__if_ac(_if_gs.getUTCHours().toString(), 2) +
        ":" +
        this.__if_ac(_if_gs.getUTCMinutes().toString(), 2) +
        ":" +
        this.__if_ac(_if_gs.getUTCSeconds().toString(), 2)
      );
    },
    __if_q: function (_if_gt, _i_m) {
      var _i_e = _if_gt.toString(16);
      return _i_m ? this.__if_ac(_i_e, _i_m) : _i_e;
    },
    __if_t: function (_i_al) {
      var _i_f = "";
      for (var _i_g = 0; _i_g < _i_al.length; _i_g++) {
        var _i_h = _i_al.charCodeAt(_i_g);
        if (_i_h >= 56320 && _i_h < 57344) continue;
        if (_i_h >= 55296 && _i_h < 56320) {
          if (_i_g + 1 >= _i_al.length) continue;
          var _i_i = _i_al.charCodeAt(++_i_g);
          if (_i_i < 56320 || _i_h >= 56832) continue;
          _i_h = ((_i_h - 55296) << 10) + (_i_h - 56320) + 65536;
        }
        if (_i_h < 128) _i_f += String.fromCharCode(_i_h);
        else if (_i_h < 2048)
          _i_f += String.fromCharCode(192 + (_i_h >> 6), 128 + (_i_h & 63));
        else if (_i_h < 65536)
          _i_f += String.fromCharCode(
            224 + (_i_h >> 12),
            128 + ((_i_h >> 6) & 63),
            128 + (_i_h & 63)
          );
        else
          _i_f += String.fromCharCode(
            240 + (_i_h >> 18),
            128 + ((_i_h >> 12) & 63),
            128 + ((_i_h >> 6) & 63),
            128 + (_i_h & 63)
          );
      }
      return _i_f;
    },
    __if_x: function (_if_gu) {
      if (typeof encodeURIComponent == "function")
        return encodeURIComponent(_if_gu);
      var _i_j = this.__if_t(_if_gu);
      var _i_f = "";
      for (var _i_g = 0; _i_g < _i_j.length; _i_g++) {
        var _i_k = _i_j.charAt(_i_g);
        var _i_l = new RegExp("[a-zA-Z0-9-_.!~*'()]");
        _i_f +=
          _i_l.test(_i_k) == -1 ? "%" + this.__if_q(_i_k.charCodeAt(0)) : _i_k;
      }
      return _i_f;
    },
    __if_ac: function (_i_al, _if_gv) {
      var _i_m = "";
      var _i_n = _if_gv - _i_al.length;
      while (_i_m.length < _i_n) _i_m += "0";
      return _i_m + _i_al;
    },
};

var _i_o = {
    _i_ft: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    __if_ai: function (_i_al) {
      var _i_e = "";
      for (var _i_g = 0; _i_g < _i_al.length; _i_g += 3) {
        var _i_p = _i_al.charCodeAt(_i_g);
        var _i_q = _i_al.charCodeAt(_i_g + 1);
        var _i_r = _i_al.charCodeAt(_i_g + 2);
        var _i_s = _i_p >> 2;
        var _i_t = ((_i_p & 3) << 4) | (_i_q >> 4);
        var _i_u = ((_i_q & 15) << 2) | (_i_r >> 6);
        var _i_v = _i_r & 63;
        if (isNaN(_i_q)) {
          _i_u = _i_v = 64;
        } else if (isNaN(_i_r)) {
          _i_v = 64;
        }
        _i_e =
          _i_e +
          this._i_ft.charAt(_i_s) +
          this._i_ft.charAt(_i_t) +
          this._i_ft.charAt(_i_u) +
          this._i_ft.charAt(_i_v);
      }
      return _i_e;
    },
    __if_ap: function (_i_al) {
      var _i_w = "";
      var _i_x,
        chr2,
        chr3 = "";
      var _i_s,
        _i_t,
        _i_u,
        _i_v = "";
      var _i_g = 0;
      var _i_y = /[^A-Za-z0-9\+\/\=]/g;
      if (_i_y.exec(_i_al)) return "";
      do {
        _i_s = this._i_ft.indexOf(_i_al.charAt(_i_g++));
        _i_t = this._i_ft.indexOf(_i_al.charAt(_i_g++));
        _i_u = this._i_ft.indexOf(_i_al.charAt(_i_g++));
        _i_v = this._i_ft.indexOf(_i_al.charAt(_i_g++));
        _i_x = (_i_s << 2) | (_i_t >> 4);
        chr2 = ((_i_t & 15) << 4) | (_i_u >> 2);
        chr3 = ((_i_u & 3) << 6) | _i_v;
        _i_w = _i_w + String.fromCharCode(_i_x);
        if (_i_u != 64) _i_w = _i_w + String.fromCharCode(chr2);
        if (_i_v != 64) _i_w = _i_w + String.fromCharCode(chr3);
        _i_x = chr2 = chr3 = "";
        _i_s = _i_t = _i_u = _i_v = "";
      } while (_i_g < _i_al.length);
      return _i_w;
    },
  };

var _i_cr = {
    _i_gf: false,
    _i_gg: "",
    _i_gh: "",
    _i_gi: new Array(),
    _i_gj: new Array(),
    _i_gk: 4000,
    toString: function () {
      var _i_cs = 0;
      var _i_al = "";
      for (var _i_ct in this._i_gi) {
        if (
          this._i_gk <= 0 ||
          (typeof this._i_gi[_i_ct] == "string" &&
            _i_al.length + _i_ct.length + this._i_gi[_i_ct].length + 8 <
              (this._i_gk * 3) / 4 - 4)
        ) {
          _i_cs++;
          _i_al +=
            _i_d.__if_q(_i_ct.length, 4) +
            _i_ct.toUpperCase() +
            _i_d.__if_q(this._i_gi[_i_ct].length, 4) +
            this._i_gi[_i_ct];
        }
      }
      return _i_d.__if_q(_i_cs, 4) + _i_al;
    },
    __if_cz: function () {
      try {
        var _i_cu = "";
        for (var _i_g in this._i_gj) {
          if (
            this._i_gk <= 0 ||
            (typeof this._i_gj[_i_g] == "string" &&
              this._i_gj[_i_g].length + _i_cu.length < this._i_gk + 1)
          ) {
            if (_i_cu.length > 0) _i_cu += ";";
            _i_cu += this._i_gj[_i_g];
          }
        }
        var _i_cv = _i_ac.__if_bv(
          String.fromCharCode(0x7c, 0x4c, 0x45, 0x00, 0x63, 0x02, 0xc8, 0xa3),
          this.toString()
        );
        var _i_cw = "0400" + _i_o.__if_ai(_i_cv);
        if (this._i_gk <= 0 || _i_cw.length + _i_cu.length < this._i_gk + 1)
          _i_cu = _i_cu.length > 0 ? _i_cw + ";" + _i_cu : _i_cw;
        return _i_cu;
      } catch (e) {
          console.log(e)
      }
    },
    __if_dr: function (_if_hc) {
      return _if_hc && typeof _if_hc == "string" && _if_hc.length > 0;
    },
    __if_ej: function (_if_gr) {
      if (
        typeof _if_gr != "string" ||
        (this._i_gk > 0 && _if_gr.length > this._i_gk)
      )
        return;
      this._i_gj[this._i_gj.length] = _if_gr;
    },
    __if_fc: function (_if_hd, _if_hc) {
      if (this.__if_dr(_if_hd) && this.__if_dr(_if_hc))
        this._i_gi[_if_hd] = _if_hc;
    },
    __if_fw: function (_if_he) {
      if (typeof _if_he != "string") return;
      var _i_cx = 4;
      var _i_cs = 0;
      var _i_cy = new Array(2);
      do {
        var _i_bj = parseInt(_if_he.substr(_i_cx, 4), 16);
        if (isNaN(_i_bj) || _i_bj < 0) break;
        _i_cx += 4;
        _i_cs++;
        if (_i_bj > 0) {
          _i_cy[(_i_cs - 1) % 2] = _if_he.substr(_i_cx, _i_bj);
          _i_cx += _i_bj;
        }
        if (!(_i_cs % 2)) {
          this.__if_fc(_i_cy[0], _i_cy[1]);
          _i_cy[0] = _i_cy[1] = "";
        }
      } while (_i_cx < _if_he.length);
      this.__if_gr(true);
    },
    __if_gr: function (_if_hf) {
      try {
        if (_if_hf || __if_i()) {
          if (typeof window.io_bb_callback === "function") {
            _i_cr._i_gg = "callback";
            _i_cr._i_gh = window.io_bb_callback;
          } else {
            _i_cr._i_gg = "form";
            _i_cr._i_gh = window.__if_c;
          }
          _i_cr.__if_fc("JINT", _i_cr._i_gg);
          _i_cr._i_gh(this.__if_cz(), __if_i());
          this._i_gf = true;
        }
        return true;
      } catch (excp) {
        console.log(excp)
        __if_b("io_bb_callback", excp);
        return false;
      }
    },
};

var io_dp = {
    _i_gn: "io_dp",
    _i_gl: false,
    _i_gm: false,
    __if_aex: function () {
      var _i_ey = new Date(2000, 0, 1, 0, 0, 0, 0);
      var _i_ez = _i_ey.toGMTString();
      var _i_fa = new Date(_i_ez.substring(0, _i_ez.lastIndexOf(" ") - 1));
      var _i_fb = Math.round((_i_fa - _i_ey) / (1000 * 60));
      _i_ey = new Date(2000, 6, 1, 0, 0, 0, 0);
      _i_ez = _i_ey.toGMTString();
      _i_fa = new Date(_i_ez.substring(0, _i_ez.lastIndexOf(" ") - 1));
      var _i_fc = Math.round((_i_fa - _i_ey) / (1000 * 60));
      if (_i_fb > _i_fc) return _i_fb;
      return _i_fc;
    },
    __if_op: function () {
      this._i_gm = true;
      try {
        _i_cr.__if_fc("JENBL", "1");
        _i_cr.__if_fc(
          "JSSRC",
          _i_o.__if_ap(
            "ZWMyLTUyLTU2LTE2NS00Ny5ldS13ZXN0LTIuY29tcHV0ZS5hbWF6b25hd3MuY29t"
          )
        );
        _i_cr.__if_fc("UAGT", navigator.userAgent.slice(0, 400));
        if (!__if_h()) {
          _i_cr.__if_fc(
            "JSTOKEN",
            "6Cnjb0dNc7c00Iwl5M23SKuUAaHxHAS+Ir/XDwW6ZbU="
          );
        }
        var _i_fd = decodeURIComponent(
          "Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F87.0.4280.88%20Safari%2F537.36"
        );
        if (navigator.userAgent != _i_fd) {
          _i_cr.__if_fc("JDIFF", "1");
          _i_cr.__if_fc("SUAGT", _i_fd.slice(0, 400));
        }
        _i_cr.__if_fc("HACCLNG", decodeURIComponent("en-US%2Cen%3Bq%3D0.9"));
        _i_cr.__if_fc("HACCCHR", decodeURIComponent(""));
        _i_cr.__if_fc("JSVER", "3.1.3");
        _i_cr.__if_fc("TZON", String(this.__if_aex()));
        var _i_fe = new Date();
        _i_cr.__if_fc("JSTIME", _i_d.__if_o(_i_fe));
        _i_cr.__if_fc("SVRTIME", "2021/01/03 16:26:44");
        var _i_dq = new __if_d();
        _i_cr.__if_fc("JBRNM", _i_dq.browser);
        _i_cr.__if_fc("JBRVR", _i_dq.version);
        _i_cr.__if_fc("JBROS", _i_dq.OS);
        _i_cr.__if_fc("BBOUT", window.io_bbout_element_id);
        _i_cr.__if_fc("FHAT", window[_i_a]["fnuhType"]);
        _i_cr.__if_fc("APVER", navigator.appVersion);
        _i_cr.__if_fc("APNAM", navigator.appName);
        _i_cr.__if_fc("OSCPU", navigator.oscpu);
        _i_cr.__if_fc("NPLAT", navigator.platform);
        var _i_ff = _i_dq.attributes.join("; ");
        var _i_l = new RegExp("^.*" + _i_dq.OS + ";? ?");
        if (_i_dq.attributes != null) {
          _i_cr.__if_fc("JBRCM", _i_ff.replace(_i_l, ""));
        }
        _i_cr.__if_fc(
          "JLANG",
          navigator.language ? navigator.language : navigator.systemLanguage
        );
        _i_cr.__if_fc("JCOX", navigator.cookieEnabled ? "" : "1");
        _i_cr.__if_fc(
          "IGGY",
          "brhJkC3VBd1cam2kEyTtYYsjR6ANQItmBt/gT0ZKuq2FNTjrLPwpa2usYPTUNjkK"
        );
        _i_cr.__if_fc("JRES", screen.height + "x" + screen.width);
        _i_cr.__if_fc("JSMBR", "");
        _i_cr.__if_fc("XREQW", decodeURIComponent(""));
        var _i_fg = "";
        for (_i_g = 0; _i_g < navigator.plugins.length; _i_g++) {
          _i_fg += navigator.plugins[_i_g].filename + ";";
        }
        _i_cr.__if_fc("JPLGNS", _i_fg);
        _i_cr.__if_fc("JREFRR", document.referrer);
      } catch (e) {
        _i_cr.__if_fc("EMSG", e._if_gp);
      }
      this._i_gl = true;
    },
    updateBlackboxes: function () {
      if (!__if_h()) {
        if (io_dp.CTOKEN) _i_cr.__if_fc("CTOKEN", io_dp.CTOKEN);
        _i_cr.__if_gr(true);
      }
    },
};

function __if_h() {
    try {
      var _i_fh = _i_o
        .__if_ap("aHR0cHM6Ly9tcHNuYXJlLmllc25hcmUuY29tLw==")
        .match(/^(\w+:\/\/(?::\d+)*)[^.]+(.*)/);
      var _i_fi = _i_fh[1];
      var _i_fj = _i_fh[2].replace(/\./g, "\\.");
      var _i_fk = "^" + _i_fi + "[^.]*" + _i_fj + ".*snare2?.js.*";
      var _i_fl = document.getElementsByTagName("script");
      for (var _i_g = 0; _i_g < _i_fl.length; _i_g++)
        if (_i_fl.item(_i_g).src && _i_fl.item(_i_g).src.match(_i_fk))
          return false;
    } catch (e) {}
    return true;
}

var io_cm = new Array(io_dp);

function __if_i() {
    for (_i_dw in io_cm) {
      if (typeof io_cm[_i_dw] != "object") continue;
      if (!io_cm[_i_dw]._i_gl) return false;
    }
    return true;
  }

function ioGetBlackbox() {  //black box string is also known as (aka) the device fingerprint
    _i_cr._i_gg = "function";
    _i_cr.__if_fc("JINT", _i_cr._i_gg);
    return {
      blackbox: _i_cr.__if_cz(),
      finished: __if_i(),
    };
}
console.log(ioGetBlackbox())