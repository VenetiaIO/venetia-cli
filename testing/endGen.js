function parseKey(e) {
    for (var t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", r = "", n = 0; e > n; ++n) r += t.substr(Math.floor(Math.random() * t.length), 1);
    return r
}

var n = {};
n.hash = function (e) {
    e = e.utf8Encode();
    var t = [1518500249, 1859775393, 2400959708, 3395469782];
    e += String.fromCharCode(128);
    for (var r = e.length / 4 + 2, i = Math.ceil(r / 16), a = new Array(i), o = 0; i > o; o++) {
        a[o] = new Array(16);
        for (var s = 0; 16 > s; s++) a[o][s] = e.charCodeAt(64 * o + 4 * s) << 24 | e.charCodeAt(64 * o + 4 * s + 1) << 16 | e.charCodeAt(64 * o + 4 * s + 2) << 8 | e.charCodeAt(64 * o + 4 * s + 3)
    }
    a[i - 1][14] = 8 * (e.length - 1) / Math.pow(2, 32), a[i - 1][14] = Math.floor(a[i - 1][14]), a[i - 1][15] = 8 * (e.length - 1) & 4294967295;
    for (var c, d, u, h, g, l = 1732584193, f = 4023233417, p = 2562383102, m = 271733878, v = 3285377520, y = new Array(80), o = 0; i > o; o++) {
        for (var E = 0; 16 > E; E++) y[E] = a[o][E];
        for (var E = 16; 80 > E; E++) y[E] = n.ROTL(y[E - 3] ^ y[E - 8] ^ y[E - 14] ^ y[E - 16], 1);
        c = l, d = f, u = p, h = m, g = v;
        for (var E = 0; 80 > E; E++) {
            var S = Math.floor(E / 20),
                T = n.ROTL(c, 5) + n.f(S, d, u, h) + g + t[S] + y[E] & 4294967295;
            g = h, h = u, u = n.ROTL(d, 30), d = c, c = T
        }
        l = l + c & 4294967295, f = f + d & 4294967295, p = p + u & 4294967295, m = m + h & 4294967295, v = v + g & 4294967295
    }
    return n.toHexStr(l) + n.toHexStr(f) + n.toHexStr(p) + n.toHexStr(m) + n.toHexStr(v)
}, n.f = function (e, t, r, n) {
    switch (e) {
    case 0:
        return t & r ^ ~t & n;
    case 1:
        return t ^ r ^ n;
    case 2:
        return t & r ^ t & n ^ r & n;
    case 3:
        return t ^ r ^ n
    }
}, n.ROTL = function (e, t) {
    return e << t | e >>> 32 - t
}, n.toHexStr = function (e) {
    for (var t, r = "", n = 7; n >= 0; n--) t = e >>> 4 * n & 15, r += t.toString(16);
    return r
}, "undefined" == typeof String.prototype.utf8Encode && (String.prototype.utf8Encode = function () {
    return unescape(encodeURIComponent(this))
}), "undefined" == typeof String.prototype.utf8Decode && (String.prototype.utf8Decode = function () {
    try {
        return decodeURIComponent(escape(this))
    } catch (e) {
        return this
    }
})

var i = function (e) {
    var t = {};
    this.options = this.extend(e, t)
};

function extend(e, t) {
    if (null == e) return t;
    for (var r in e) null != e[r] && t[r] !== e[r] && (t[r] = e[r]);
    return t
}

function mine(e, t, r) {
    for (var i = 0, a = Math.pow(2, 32 - t);;) {
        var o = i.toString(16) + ":" + e;
        i++;
        var s = n.hash(o);
        if (parseInt(s.substr(0, 8), 16) < a) return void r(o)
    }
}


function proof(){
    var nValue = (new Date).getTime() + ":" + parseKey(20);

    var proof = "";
    mine(nValue, 8, function (t) {
        proof = t
    })
    
    return proof
}



// let proof = proof();
