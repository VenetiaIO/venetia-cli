!(function (e) {
  function t(r) {
    if (n[r]) return n[r].exports;
    var o = (n[r] = { i: r, l: !1, exports: {} });
    return e[r].call(o.exports, o, o.exports, t), (o.l = !0), o.exports;
  }
  var n = {};
  (t.m = e),
    (t.c = n),
    (t.d = function (e, n, r) {
      t.o(e, n) ||
        Object.defineProperty(e, n, {
          configurable: !1,
          enumerable: !0,
          get: r,
        });
    }),
    (t.n = function (e) {
      var n =
        e && e.__esModule
          ? function () {
              return e.default;
            }
          : function () {
              return e;
            };
      return t.d(n, "a", n), n;
    }),
    (t.o = function (e, t) {
      return Object.prototype.hasOwnProperty.call(e, t);
    }),
    (t.p = ""),
    t((t.s = 0));
})([
  function (e, t, n) {
    e.exports = n(1);
  },
  function (e, t, n) {
    "use strict";
    function r(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function o(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function i(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function a(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function c(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function s(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function u(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function l(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function p(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function f(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function d(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function _(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function h(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function m(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function y(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function v(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function b(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function g(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function E(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function w(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function S(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function P(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function O(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function k(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function A(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function T(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function R(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function I(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function N(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function M(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function C(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function j(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function L(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function x(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function q(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function D(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function B(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function F(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function U(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function H(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function G(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function W(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function Y(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function z(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function K(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function V(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function J(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function X(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function Q(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function $(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function Z(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function ee(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function te(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function ne(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function re(e, t) {
      if (!e)
        throw new ReferenceError(
          "this hasn't been initialised - super() hasn't been called"
        );
      return !t || ("object" != typeof t && "function" != typeof t) ? e : t;
    }
    function oe(e, t) {
      if ("function" != typeof t && null !== t)
        throw new TypeError(
          "Super expression must either be null or a function, not " + typeof t
        );
      (e.prototype = Object.create(t && t.prototype, {
        constructor: {
          value: e,
          enumerable: !1,
          writable: !0,
          configurable: !0,
        },
      })),
        t &&
          (Object.setPrototypeOf
            ? Object.setPrototypeOf(e, t)
            : (e.__proto__ = t));
    }
    function ie(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function ae(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function ce(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function se(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0,
            })
          : (e[t] = n),
        e
      );
    }
    function ue(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function le(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function pe(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function fe(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function de(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function _e(e) {
      return e;
    }
    function he(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function me(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function ye(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    function ve(e, t) {
      var n = {};
      for (var r in e)
        t.indexOf(r) >= 0 ||
          (Object.prototype.hasOwnProperty.call(e, r) && (n[r] = e[r]));
      return n;
    }
    function be(e, t) {
      if (!(e instanceof t))
        throw new TypeError("Cannot call a class as a function");
    }
    function ge(e) {
      if (Array.isArray(e)) {
        for (var t = 0, n = Array(e.length); t < e.length; t++) n[t] = e[t];
        return n;
      }
      return Array.from(e);
    }
    Object.defineProperty(t, "__esModule", { value: !0 });
    var Ee,
      we,
      Se,
      Pe,
      Oe,
      ke,
      Ae,
      Te,
      Re = (function (e) {
        function t(e) {
          r(this, t);
          var n = o(
            this,
            (t.__proto__ || Object.getPrototypeOf(t)).call(this, e)
          );
          return (
            window.__stripeElementsController &&
              window.__stripeElementsController.reportIntegrationError(e),
            (n.name = "IntegrationError"),
            Object.defineProperty(n, "message", {
              value: n.message,
              enumerable: !0,
            }),
            n
          );
        }
        return i(t, e), t;
      })(Error),
      Ie = Re,
      Ne = function (e) {
        var t =
          arguments.length > 1 && void 0 !== arguments[1]
            ? arguments[1]
            : "absurd";
        throw new Error(t);
      },
      Me = n(2),
      Ce = n.n(Me),
      je = window.Promise ? Promise : Ce.a,
      Le = je,
      xe = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      qe = Date.now
        ? function () {
            return Date.now();
          }
        : function () {
            return new Date().getTime();
          },
      De = qe(),
      Be =
        window.performance && window.performance.now
          ? function () {
              return window.performance.now();
            }
          : function () {
              return qe() - De;
            },
      Fe = (function () {
        function e(t) {
          a(this, e), (this.timestampValue = null != t ? t : Be());
        }
        return (
          xe(
            e,
            [
              {
                key: "getAsPosixTime",
                value: function () {
                  return qe() - this.getElapsedTime();
                },
              },
              {
                key: "getElapsedTime",
                value: function (e) {
                  return Math.round(
                    (e ? e.timestampValue : Be()) - this.timestampValue
                  );
                },
              },
              {
                key: "valueOf",
                value: function () {
                  return Math.round(this.timestampValue);
                },
              },
            ],
            [
              {
                key: "fromPosixTime",
                value: function (t) {
                  return new e(t - qe() + Be());
                },
              },
            ]
          ),
          e
        );
      })(),
      Ue =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      He = function (e, t) {
        for (var n = 0; n < e.length; n++) if (t(e[n])) return e[n];
      },
      Ge = function (e, t) {
        for (var n = 0; n < e.length; n++) if (t(e[n])) return n;
        return -1;
      },
      We = function e(t, n) {
        if (
          "object" !== (void 0 === t ? "undefined" : Ue(t)) ||
          "object" !== (void 0 === n ? "undefined" : Ue(n))
        )
          return t === n;
        if (null === t || null === n) return t === n;
        var r = Array.isArray(t);
        if (r !== Array.isArray(n)) return !1;
        var o = "[object Object]" === Object.prototype.toString.call(t);
        if (o !== ("[object Object]" === Object.prototype.toString.call(n)))
          return !1;
        if (!o && !r) return !1;
        var i = Object.keys(t),
          a = Object.keys(n);
        if (i.length !== a.length) return !1;
        for (var c = {}, s = 0; s < i.length; s++) c[i[s]] = !0;
        for (var u = 0; u < a.length; u++) c[a[u]] = !0;
        var l = Object.keys(c);
        if (l.length !== i.length) return !1;
        var p = t,
          f = n,
          d = function (t) {
            return e(p[t], f[t]);
          };
        return l.every(d);
      },
      Ye = function (e, t) {
        for (var n = {}, r = 0; r < t.length; r++) n[t[r]] = !0;
        for (var o = [], i = 0; i < e.length; i++) n[e[i]] && o.push(e[i]);
        return o;
      },
      ze = function (e, t) {
        var n = 0,
          r = function r(o) {
            for (var i = new Fe(); n < e.length && i.getElapsedTime() < 50; )
              t(e[n]), n++;
            n === e.length
              ? o()
              : setTimeout(function () {
                  return r(o);
                });
          };
        return new Le(function (e) {
          return r(e);
        });
      },
      Ke = [
        "aed",
        "afn",
        "all",
        "amd",
        "ang",
        "aoa",
        "ars",
        "aud",
        "awg",
        "azn",
        "bam",
        "bbd",
        "bdt",
        "bgn",
        "bhd",
        "bif",
        "bmd",
        "bnd",
        "bob",
        "brl",
        "bsd",
        "btn",
        "bwp",
        "byr",
        "bzd",
        "cad",
        "cdf",
        "chf",
        "clf",
        "clp",
        "cny",
        "cop",
        "crc",
        "cuc",
        "cup",
        "cve",
        "czk",
        "djf",
        "dkk",
        "dop",
        "dzd",
        "egp",
        "ern",
        "etb",
        "eur",
        "fjd",
        "fkp",
        "gbp",
        "gel",
        "ghs",
        "gip",
        "gmd",
        "gnf",
        "gtq",
        "gyd",
        "hkd",
        "hnl",
        "hrk",
        "htg",
        "huf",
        "idr",
        "ils",
        "inr",
        "iqd",
        "irr",
        "isk",
        "jmd",
        "jod",
        "jpy",
        "kes",
        "kgs",
        "khr",
        "kmf",
        "kpw",
        "krw",
        "kwd",
        "kyd",
        "kzt",
        "lak",
        "lbp",
        "lkr",
        "lrd",
        "lsl",
        "ltl",
        "lvl",
        "lyd",
        "mad",
        "mdl",
        "mga",
        "mkd",
        "mmk",
        "mnt",
        "mop",
        "mro",
        "mur",
        "mvr",
        "mwk",
        "mxn",
        "myr",
        "mzn",
        "nad",
        "ngn",
        "nio",
        "nok",
        "npr",
        "nzd",
        "omr",
        "pab",
        "pen",
        "pgk",
        "php",
        "pkr",
        "pln",
        "pyg",
        "qar",
        "ron",
        "rsd",
        "rub",
        "rwf",
        "sar",
        "sbd",
        "scr",
        "sdg",
        "sek",
        "sgd",
        "shp",
        "skk",
        "sll",
        "sos",
        "srd",
        "ssp",
        "std",
        "svc",
        "syp",
        "szl",
        "thb",
        "tjs",
        "tmt",
        "tnd",
        "top",
        "try",
        "ttd",
        "twd",
        "tzs",
        "uah",
        "ugx",
        "usd",
        "uyu",
        "uzs",
        "vef",
        "vnd",
        "vuv",
        "wst",
        "xaf",
        "xag",
        "xau",
        "xcd",
        "xdr",
        "xof",
        "xpf",
        "yer",
        "zar",
        "zmk",
        "zmw",
        "btc",
        "jep",
        "eek",
        "ghc",
        "mtl",
        "tmm",
        "yen",
        "zwd",
        "zwl",
        "zwn",
        "zwr",
      ],
      Ve = Ke,
      Je = {
        AE: "AE",
        AT: "AT",
        AU: "AU",
        BE: "BE",
        BG: "BG",
        BR: "BR",
        CA: "CA",
        CH: "CH",
        CI: "CI",
        CR: "CR",
        CY: "CY",
        CZ: "CZ",
        DE: "DE",
        DK: "DK",
        DO: "DO",
        EE: "EE",
        ES: "ES",
        FI: "FI",
        FR: "FR",
        GB: "GB",
        GR: "GR",
        GT: "GT",
        HK: "HK",
        HU: "HU",
        ID: "ID",
        IE: "IE",
        IN: "IN",
        IT: "IT",
        JP: "JP",
        LT: "LT",
        LU: "LU",
        LV: "LV",
        MT: "MT",
        MX: "MX",
        MY: "MY",
        NL: "NL",
        NO: "NO",
        NZ: "NZ",
        PE: "PE",
        PH: "PH",
        PL: "PL",
        PT: "PT",
        RO: "RO",
        SE: "SE",
        SG: "SG",
        SI: "SI",
        SK: "SK",
        SN: "SN",
        TH: "TH",
        TT: "TT",
        US: "US",
        UY: "UY",
      },
      Xe = Object.keys(Je),
      Qe = { live: "live", test: "test", unknown: "unknown" },
      $e = function (e) {
        return /^pk_test_/.test(e)
          ? Qe.test
          : /^pk_live_/.test(e)
          ? Qe.live
          : Qe.unknown;
      },
      Ze = function (e) {
        if (e === Qe.unknown)
          throw new Ie(
            "It looks like you're using an older Stripe key. In order to use this API, you'll need to use a modern API key, which is prefixed with 'pk_live_' or 'pk_test_'.\n    You can roll your publishable key here: https://dashboard.stripe.com/account/apikeys"
          );
      },
      et = /^(http(s)?):\/\//,
      tt = function (e) {
        return et.test(e);
      },
      nt = function (e) {
        if (!tt(e)) return null;
        var t = document.createElement("a");
        t.href = e;
        var n = t.protocol,
          r = t.host,
          o = t.pathname,
          i = /:80$/,
          a = /:443$/;
        return (
          "http:" === n && i.test(r)
            ? (r = r.replace(i, ""))
            : "https:" === n && a.test(r) && (r = r.replace(a, "")),
          { host: r, protocol: n, origin: n + "//" + r, path: o }
        );
      },
      rt = function (e, t) {
        if ("/" === t[0]) {
          var n = nt(e);
          return n ? "" + n.origin + t : t;
        }
        return "" + e.replace(/\/[^\/]*$/, "/") + t;
      },
      ot =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      it =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      at = function (e, t, n) {
        return (
          "Invalid value for " +
          n.label +
          ": " +
          (n.path.join(".") || "value") +
          " should be " +
          e +
          ". You specified: " +
          t +
          "."
        );
      },
      ct = function (e) {
        return {
          type: "valid",
          value: e,
          warnings:
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : [],
        };
      },
      st = function (e) {
        return { error: e, errorType: "full", type: "error" };
      },
      ut = function (e, t, n) {
        var r = new Ie(at(e, t, n));
        return st(r);
      },
      lt = function (e, t, n) {
        return {
          expected: e,
          actual: String(t),
          options: n,
          errorType: "mismatch",
          type: "error",
        };
      },
      pt = function (e) {
        return function (t, n) {
          return void 0 === t ? ct(t) : e(t, n);
        };
      },
      ft = function (e, t) {
        return function (n, r) {
          var o = function (e) {
              var t = e.options.path.join(".") || "value";
              return {
                error: t + " should be " + e.expected,
                actual: t + " as " + e.actual,
              };
            },
            i = function (e, t, n) {
              return st(
                new Ie(
                  "Invalid value for " +
                    e +
                    ": " +
                    t +
                    ". You specified " +
                    n +
                    "."
                )
              );
            },
            a = e(n, r),
            c = t(n, r);
          if ("error" === a.type && "error" === c.type) {
            if ("mismatch" === a.errorType && "mismatch" === c.errorType) {
              var s = o(a),
                u = s.error,
                l = s.actual,
                p = o(c),
                f = p.error,
                d = p.actual;
              return i(
                r.label,
                u === f ? u : u + " or " + f,
                l === d ? l : l + " and " + d
              );
            }
            if ("mismatch" === a.errorType) {
              var _ = o(a),
                h = _.error,
                m = _.actual;
              return i(r.label, h, m);
            }
            if ("mismatch" === c.errorType) {
              var y = o(c),
                v = y.error,
                b = y.actual;
              return i(r.label, v, b);
            }
            return st(a.error);
          }
          return "valid" === a.type ? a : c;
        };
      },
      dt = function (e, t) {
        return function (n, r) {
          var o = He(e, function (e) {
            return e === n;
          });
          if (void 0 === o) {
            var i = t
              ? "a recognized string."
              : "one of the following strings: " + e.join(", ");
            return lt(i, n, r);
          }
          return ct(o);
        };
      },
      _t = function (e) {
        return function (t, n) {
          return "string" == typeof t && 0 === t.indexOf(e)
            ? ct(t)
            : lt("a string starting with " + e, t, n);
        };
      },
      ht = function () {
        for (var e = arguments.length, t = Array(e), n = 0; n < e; n++)
          t[n] = arguments[n];
        return dt(t, !1);
      },
      mt = function () {
        for (var e = arguments.length, t = Array(e), n = 0; n < e; n++)
          t[n] = arguments[n];
        return dt(t, !0);
      },
      yt = ht.apply(void 0, s(Xe)),
      vt = ht.apply(void 0, s(Ve)),
      bt =
        (ht.apply(void 0, s(Object.keys(Qe))),
        function (e, t) {
          return "string" == typeof e ? ct(e) : lt("a string", e, t);
        }),
      gt = function (e, t) {
        return function (n, r) {
          return void 0 === n ? ct(t()) : e(n, r);
        };
      },
      Et = function (e, t) {
        return "boolean" == typeof e ? ct(e) : lt("a boolean", e, t);
      },
      wt = function (e, t) {
        return "number" == typeof e ? ct(e) : lt("a number", e, t);
      },
      St = function (e) {
        return function (t, n) {
          return "number" == typeof t && t > e
            ? ct(t)
            : lt("a number greater than " + e, t, n);
        };
      },
      Pt = function (e) {
        return function (t, n) {
          return "number" == typeof t && t === parseInt(t, 10) && (!e || t >= 0)
            ? ct(t)
            : lt(
                e
                  ? "a positive amount in the currency's subunit"
                  : "an amount in the currency's subunit",
                t,
                n
              );
        };
      },
      Ot = function (e, t) {
        return Pt(!1)(e, t);
      },
      kt = function (e, t) {
        return Pt(!0)(e, t);
      },
      At = function (e, t) {
        return e && "object" === (void 0 === e ? "undefined" : it(e))
          ? ct(e)
          : lt("an object", e, t);
      },
      Tt = function (e) {
        return function (t, n) {
          if (Array.isArray(t)) {
            return t
              .map(function (t, r) {
                return e(
                  t,
                  ot({}, n, { path: [].concat(s(n.path), [String(r)]) })
                );
              })
              .reduce(function (e, t) {
                return "error" === e.type
                  ? e
                  : "error" === t.type
                  ? t
                  : ct(
                      [].concat(s(e.value), [t.value]),
                      [].concat(s(e.warnings), s(t.warnings))
                    );
              }, ct([]));
          }
          return lt("array", t, n);
        };
      },
      Rt = function (e) {
        return function (t) {
          return function (n, r) {
            if (Array.isArray(n)) {
              var o = t(n, r);
              if ("valid" === o.type)
                for (var i = {}, a = 0; a < o.value.length; a += 1) {
                  var c = o.value[a];
                  if (
                    "object" === (void 0 === c ? "undefined" : it(c)) &&
                    c &&
                    "string" == typeof c[e]
                  ) {
                    var s = c[e],
                      u = "_" + s;
                    if (i[u])
                      return st(
                        new Ie(
                          "Duplicate value for " +
                            e +
                            ": " +
                            s +
                            ". The property '" +
                            e +
                            "' of '" +
                            r.path.join(".") +
                            "' has to be unique."
                        )
                      );
                    i[u] = !0;
                  }
                }
              return o;
            }
            return lt("array", n, r);
          };
        };
      },
      It = function (e) {
        return function (t, n) {
          return void 0 === t
            ? ct(void 0)
            : lt("used in " + e + " instead", t, n);
        };
      },
      Nt = function (e) {
        return function (t) {
          return function (n, r) {
            if (
              n &&
              "object" === (void 0 === n ? "undefined" : it(n)) &&
              !Array.isArray(n)
            ) {
              var o = n,
                i = He(Object.keys(o), function (e) {
                  return !t[e];
                });
              if (i && e)
                return st(
                  new Ie(
                    "Invalid " +
                      r.label +
                      " parameter: " +
                      [].concat(s(r.path), [i]).join(".") +
                      " is not an accepted parameter."
                  )
                );
              var a = Object.keys(o),
                u = ct({});
              return (
                i &&
                  (u = a.reduce(function (e, n) {
                    return t[n]
                      ? e
                      : ct(
                          e.value,
                          [].concat(s(e.warnings), [
                            "Unrecognized " +
                              r.label +
                              " parameter: " +
                              [].concat(s(r.path), [n]).join(".") +
                              " is not a recognized parameter. This may cause issues with your integration in the future.",
                          ])
                        );
                  }, u)),
                Object.keys(t).reduce(function (e, n) {
                  if ("error" === e.type) return e;
                  var i = t[n],
                    a = i(o[n], ot({}, r, { path: [].concat(s(r.path), [n]) }));
                  return "valid" === a.type && void 0 !== a.value
                    ? ct(
                        ot({}, e.value, c({}, n, a.value)),
                        [].concat(s(e.warnings), s(a.warnings))
                      )
                    : "valid" === a.type
                    ? ct(e.value, [].concat(s(e.warnings), s(a.warnings)))
                    : a;
                }, u)
              );
            }
            return lt("an object", n, r);
          };
        };
      },
      Mt = Nt(!0),
      Ct = Nt(!1),
      jt = function (e, t) {
        return ot({}, e, { path: [].concat(s(e.path), [t]) });
      },
      Lt = function (e, t, n, r) {
        var o = r || {},
          i = e(t, {
            origin: o.origin || "",
            element: o.element || "",
            label: n,
            path: o.path || [],
          });
        return "valid" === i.type
          ? i
          : "full" === i.errorType
          ? i
          : {
              type: "error",
              errorType: "full",
              error: new Ie(at(i.expected, i.actual, i.options)),
            };
      },
      xt = function (e, t, n, r) {
        var o = Lt(e, t, n, r);
        switch (o.type) {
          case "valid":
            return { value: o.value, warnings: o.warnings };
          case "error":
            throw o.error;
          default:
            return Ne(o);
        }
      },
      qt = {
        ADDRESS_AUTOCOMPLETE: "ADDRESS_AUTOCOMPLETE",
        CARD_ELEMENT: "CARD_ELEMENT",
        CONTROLLER: "CONTROLLER",
        METRICS_CONTROLLER: "METRICS_CONTROLLER",
        PAYMENT_REQUEST_ELEMENT: "PAYMENT_REQUEST_ELEMENT",
        PAYMENT_REQUEST_BROWSER: "PAYMENT_REQUEST_BROWSER",
        PAYMENT_REQUEST_GOOGLE_PAY: "PAYMENT_REQUEST_GOOGLE_PAY",
        IBAN_ELEMENT: "IBAN_ELEMENT",
        IDEAL_BANK_ELEMENT: "IDEAL_BANK_ELEMENT",
        AUTHORIZE_WITH_URL: "AUTHORIZE_WITH_URL",
        STRIPE_3DS2_CHALLENGE: "STRIPE_3DS2_CHALLENGE",
        STRIPE_3DS2_FINGERPRINT: "STRIPE_3DS2_FINGERPRINT",
        AU_BANK_ACCOUNT_ELEMENT: "AU_BANK_ACCOUNT_ELEMENT",
        FPX_BANK_ELEMENT: "FPX_BANK_ELEMENT",
        LIGHTBOX_APP: "LIGHTBOX_APP",
      },
      Dt = qt,
      Bt = Object({
        NODE_ENV: "production",
        TEST_ENV: !1,
        SELENIUM_TEST_ENV: !1,
        PUBLIC_URL: "",
        RELEASE_VERSION: "7183167e",
        STRIPE_JS_API_URL: "https://api.stripe.com/v1/",
        STRIPE_JS_HOOKS_URL: "https://hooks.stripe.com/",
        STRIPE_HIP_URL: "https://invoice.stripe.com",
        STRIPE_PAYMENTS_URL: "https://payments.stripe.com",
        STRIPE_HIP_DATA_URL: "https://invoicedata.stripe.com/",
        STRIPE_OLD_HIP_URL: "https://pay.stripe.com",
        STRIPE_JS_ALLOW_MUTABLE_API_URL: !1,
        STRIPE_JS_Q_URL: "https://q.stripe.com",
        STRIPE_JS_M_NETWORK_URL: "https://m.stripe.network",
        STRIPE_JS_PAYMENTS_URL_REWRITES: !1,
        STRIPE_JS_ROOT_URL: "https://js.stripe.com/v3/",
        STRIPE_CHECKOUT_URL: "https://checkout.stripe.com/",
        STRIPE_FLINKS_API_URL: "",
        STRIPE_JS_SOURCEMAPS: !1,
        STRIPE_JS_DEBUG_POSTMESSAGE: !1,
        STRIPE_JS_DEBUG_LOGGER: !0,
        ELEMENTS_INNER_CARD_HTML_NAME:
          "elements-inner-card-7c709165b923b57686ef7bd156668047.html",
        ELEMENTS_INNER_IBAN_HTML_NAME:
          "elements-inner-iban-2f5fb7dccca0cb4312133993f4c35de7.html",
        ELEMENTS_INNER_IDEAL_BANK_HTML_NAME:
          "elements-inner-ideal-bank-c2688f53679f1cc003ee4f5941d8e9a3.html",
        ELEMENTS_INNER_PAYMENT_REQUEST_HTML_NAME:
          "elements-inner-payment-request-38139b90900baea9545e50fe4f7a3e7c.html",
        ELEMENTS_INNER_AU_BANK_ACCOUNT_HTML_NAME:
          "elements-inner-au-bank-account-f5f75454405a34e58f03860d25b6d8b3.html",
        ELEMENTS_INNER_FPX_BANK_HTML_NAME:
          "elements-inner-fpx-bank-39497c2da5d3ed07a97e15d10e87defa.html",
        RECAPTCHA_HTML_NAME: "recaptcha.html",
        CHECKOUT_INNER_ADDRESS_AUTOCOMPLETE_HTML_NAME:
          "checkout-inner-address-autocomplete-cf04c314168c3949dfe91491f142000d.html",
        CONTROLLER_HTML_NAME:
          "controller-3a7bf1d6a025a77682c5d50829c5af2d.html",
        PAYMENT_REQUEST_INNER_BROWSER_HTML_NAME:
          "payment-request-inner-browser-4e2a15d9ba2e9bd5168f2fc95194557a.html",
        PAYMENT_REQUEST_INNER_GOOGLE_PAY_HTML_NAME:
          "payment-request-inner-google-pay-0d2b5a5aee752c8d7d047d9a0f9415df.html",
        AUTHORIZE_WITH_URL_INNER_HTML_NAME:
          "authorize-with-url-inner-2e1b686ba76fc87a44e63d7808da6129.html",
        THREE_DS_2_CHALLENGE_HTML_NAME:
          "three-ds-2-challenge-47fab86f335ea73d4202e1a15b3fb82c.html",
        THREE_DS_2_FINGERPRINT_HTML_NAME:
          "three-ds-2-fingerprint-cb76e42d76deb5a59efe231496c40951.html",
        M_OUTER_HTML_NAME: "m-outer-090169779cdf49fad5ab0e59c999f664.html",
        LIGHTBOX_INNER_HTML_NAME:
          "lightbox-inner-d76966c870e572e8bee0156c0ce20b6b.html",
        STRIPE_JS_NO_DEMOS: !0,
        STRIPE_JS_NO_REPORTS: !0,
      }),
      Ft = function (e) {
        return "" + (Bt.STRIPE_JS_ROOT_URL || "") + (e || "");
      },
      Ut = function (e) {
        switch (e) {
          case "ADDRESS_AUTOCOMPLETE":
            return Ft(Bt.CHECKOUT_INNER_ADDRESS_AUTOCOMPLETE_HTML_NAME);
          case "CARD_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_CARD_HTML_NAME);
          case "CONTROLLER":
            return Ft(Bt.CONTROLLER_HTML_NAME);
          case "METRICS_CONTROLLER":
            return Ft(Bt.M_OUTER_HTML_NAME);
          case "PAYMENT_REQUEST_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_PAYMENT_REQUEST_HTML_NAME);
          case "PAYMENT_REQUEST_BROWSER":
            return Ft(Bt.PAYMENT_REQUEST_INNER_BROWSER_HTML_NAME);
          case "PAYMENT_REQUEST_GOOGLE_PAY":
            return Ft(Bt.PAYMENT_REQUEST_INNER_GOOGLE_PAY_HTML_NAME);
          case "IBAN_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_IBAN_HTML_NAME);
          case "IDEAL_BANK_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_IDEAL_BANK_HTML_NAME);
          case "AUTHORIZE_WITH_URL":
            return Ft(Bt.AUTHORIZE_WITH_URL_INNER_HTML_NAME);
          case "STRIPE_3DS2_CHALLENGE":
            return Ft(Bt.THREE_DS_2_CHALLENGE_HTML_NAME);
          case "STRIPE_3DS2_FINGERPRINT":
            return Ft(Bt.THREE_DS_2_FINGERPRINT_HTML_NAME);
          case "AU_BANK_ACCOUNT_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_AU_BANK_ACCOUNT_HTML_NAME);
          case "FPX_BANK_ELEMENT":
            return Ft(Bt.ELEMENTS_INNER_FPX_BANK_HTML_NAME);
          case "LIGHTBOX_APP":
            return Ft(Bt.LIGHTBOX_INNER_HTML_NAME);
          default:
            return Ne(e);
        }
      },
      Ht = Ut,
      Gt = {
        card: "card",
        cardNumber: "cardNumber",
        cardExpiry: "cardExpiry",
        cardCvc: "cardCvc",
        postalCode: "postalCode",
        iban: "iban",
        idealBank: "idealBank",
        paymentRequestButton: "paymentRequestButton",
        auBankAccount: "auBankAccount",
        fpxBank: "fpxBank",
        idealBankSecondary: "idealBankSecondary",
        auBankAccountNumber: "auBankAccountNumber",
        auBsb: "auBsb",
        fpxBankSecondary: "fpxBankSecondary",
      },
      Wt = Gt,
      Yt = { PAYMENT_INTENT: "PAYMENT_INTENT", SETUP_INTENT: "SETUP_INTENT" },
      zt = Yt,
      Kt = [Wt.card, Wt.cardNumber, Wt.cardExpiry, Wt.cardCvc, Wt.postalCode],
      Vt = Kt,
      Jt = "https://js.stripe.com/v3/",
      Xt = nt(Jt),
      Qt = Xt ? Xt.origin : "",
      $t = {
        family: "font-family",
        src: "src",
        unicodeRange: "unicode-range",
        style: "font-style",
        variant: "font-variant",
        stretch: "font-stretch",
        weight: "font-weight",
        display: "font-display",
      },
      Zt = Object.keys($t).reduce(function (e, t) {
        return (e[$t[t]] = t), e;
      }, {}),
      en = [
        Wt.idealBank,
        Wt.idealBankSecondary,
        Wt.fpxBank,
        Wt.fpxBankSecondary,
      ],
      tn = 0,
      nn = function (e) {
        return "" + e + tn++;
      },
      rn = function e() {
        var t =
          arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "";
        return t
          ? (
              parseInt(t, 10) ^
              ((16 * Math.random()) >> (parseInt(t, 10) / 4))
            ).toString(16)
          : "00000000-0000-4000-8000-000000000000".replace(/[08]/g, e);
      },
      on =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      an = function e(t, n) {
        var r = [];
        return (
          Object.keys(t).forEach(function (o) {
            var i = t[o],
              a = n ? n + "[" + o + "]" : o;
            if (i && "object" === (void 0 === i ? "undefined" : on(i))) {
              var c = e(i, a);
              "" !== c && (r = [].concat(u(r), [c]));
            } else void 0 !== i && null !== i && (r = [].concat(u(r), [a + "=" + encodeURIComponent(String(i))]));
          }),
          r.join("&").replace(/%20/g, "+")
        );
      },
      cn = an,
      sn = n(6),
      un = n.n(sn),
      ln = (function () {
        function e(e, t) {
          var n = [],
            r = !0,
            o = !1,
            i = void 0;
          try {
            for (
              var a, c = e[Symbol.iterator]();
              !(r = (a = c.next()).done) &&
              (n.push(a.value), !t || n.length !== t);
              r = !0
            );
          } catch (e) {
            (o = !0), (i = e);
          } finally {
            try {
              !r && c.return && c.return();
            } finally {
              if (o) throw i;
            }
          }
          return n;
        }
        return function (t, n) {
          if (Array.isArray(t)) return t;
          if (Symbol.iterator in Object(t)) return e(t, n);
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance"
          );
        };
      })(),
      pn = function (e, t) {
        var n = {};
        t.forEach(function (e) {
          var t = ln(e, 2),
            r = t[0],
            o = t[1];
          r.split(/\s+/).forEach(function (e) {
            e && (n[e] = n[e] || o);
          });
        }),
          (e.className = un()(e.className, n));
      },
      fn = function (e, t) {
        e.style.cssText = Object.keys(t)
          .map(function (e) {
            return e + ": " + t[e] + " !important;";
          })
          .join(" ");
      },
      dn = {
        border: "none",
        margin: "0",
        padding: "0",
        width: "1px",
        "min-width": "100%",
        overflow: "hidden",
        display: "block",
        visibility: "hidden",
        position: "fixed",
        height: "1px",
        "pointer-events": "none",
        "user-select": "none",
      },
      _n = function (e) {
        fn(e, dn);
      },
      hn = function (e) {
        try {
          return window.parent.frames[e];
        } catch (e) {
          return null;
        }
      },
      mn = function (e) {
        if (!document.body)
          throw new Ie(
            "Stripe.js requires that your page has a <body> element."
          );
        return e(document.body);
      },
      yn =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      vn = function (e) {
        var t = e.controllerId,
          n = e.frameId,
          r = e.targetOrigin,
          o = e.type,
          i = r,
          a = void 0;
        "controller" === o
          ? (a = hn(n))
          : "group" === o
          ? (a = hn(t))
          : "outer" === o
          ? (a = window.frames[n])
          : "hosted" === o
          ? (a = window.frames[n])
          : "inner" === o && ((i = i || "*"), (a = window.parent)),
          (i = i || Qt),
          a &&
            a.postMessage(JSON.stringify(yn({}, e, { __stripeJsV3: !0 })), i);
      },
      bn = function (e) {
        try {
          var t = "string" == typeof e ? JSON.parse(e) : e;
          return t.__stripeJsV3 ? t : null;
        } catch (e) {
          return null;
        }
      },
      gn =
        (n(7),
        function (e, t) {
          var n = e._isUserError || "IntegrationError" === e.name;
          throw (
            (t &&
              !n &&
              t.report("fatal.uncaught_error", {
                iframe: !1,
                name: e.name,
                element: "outer",
                message: e.message || e.description,
                fileName: e.fileName,
                lineNumber: e.lineNumber,
                columnNumber: e.columnNumber,
                stack: e.stack && e.stack.substring(0, 1e3),
              }),
            e)
          );
        }),
      En = function (e, t) {
        return function () {
          try {
            return e.call(this);
          } catch (e) {
            return gn(e, t || (this && this._controller));
          }
        };
      },
      wn = function (e, t) {
        return function (n) {
          try {
            return e.call(this, n);
          } catch (e) {
            return gn(e, t || (this && this._controller));
          }
        };
      },
      Sn = function (e, t) {
        return function (n, r) {
          try {
            return e.call(this, n, r);
          } catch (e) {
            return gn(e, t || (this && this._controller));
          }
        };
      },
      Pn = function (e, t) {
        return function (n, r, o) {
          try {
            return e.call(this, n, r, o);
          } catch (e) {
            return gn(e, t || (this && this._controller));
          }
        };
      },
      On = function (e, t) {
        return function () {
          try {
            for (var n = arguments.length, r = Array(n), o = 0; o < n; o++)
              r[o] = arguments[o];
            return e.call.apply(e, [this].concat(r));
          } catch (e) {
            return gn(e, t || (this && this._controller));
          }
        };
      },
      kn = function e() {
        var t = this;
        l(this, e),
          (this._emit = function (e) {
            for (
              var n = arguments.length, r = Array(n > 1 ? n - 1 : 0), o = 1;
              o < n;
              o++
            )
              r[o - 1] = arguments[o];
            return (
              (t._callbacks[e] || []).forEach(function (e) {
                var t = e.fn;
                if (t._isUserCallback)
                  try {
                    t.apply(void 0, r);
                  } catch (e) {
                    throw ((e._isUserError = !0), e);
                  }
                else t.apply(void 0, r);
              }),
              t
            );
          }),
          (this._once = function (e, n) {
            var r = function r() {
              t._off(e, r), n.apply(void 0, arguments);
            };
            return t._on(e, r, n);
          }),
          (this._removeAllListeners = function () {
            return (t._callbacks = {}), t;
          }),
          (this._on = function (e, n, r) {
            return (
              (t._callbacks[e] = t._callbacks[e] || []),
              t._callbacks[e].push({ original: r, fn: n }),
              t
            );
          }),
          (this._validateUserOn = function (e, t) {}),
          (this._userOn = function (e, n) {
            if ("string" != typeof e)
              throw new Ie(
                "When adding an event listener, the first argument should be a string event name."
              );
            if ("function" != typeof n)
              throw new Ie(
                "When adding an event listener, the second argument should be a function callback."
              );
            return (
              t._validateUserOn(e, n), (n._isUserCallback = !0), t._on(e, n)
            );
          }),
          (this._hasRegisteredListener = function (e) {
            return t._callbacks[e] && t._callbacks[e].length > 0;
          }),
          (this._off = function (e, n) {
            if (n) {
              for (
                var r = t._callbacks[e], o = void 0, i = 0;
                i < r.length;
                i++
              )
                if (((o = r[i]), o.fn === n || o.original === n)) {
                  r.splice(i, 1);
                  break;
                }
            } else delete t._callbacks[e];
            return t;
          }),
          (this._callbacks = {});
        var n = Sn(this._userOn),
          r = Sn(this._off),
          o = Sn(this._once),
          i = wn(this._hasRegisteredListener),
          a = wn(this._removeAllListeners),
          c = On(this._emit);
        (this.on = this.addListener = this.addEventListener = n),
          (this.off = this.removeListener = this.removeEventListener = r),
          (this.once = o),
          (this.hasRegisteredListener = i),
          (this.removeAllListeners = a),
          (this.emit = c);
      },
      An = kn,
      Tn =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Rn = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      In = (function (e) {
        function t(e, n, r, o) {
          f(this, t);
          var i = d(this, (t.__proto__ || Object.getPrototypeOf(t)).call(this));
          return (
            (i._sendFAReq = function (e) {
              var t = nn(e.tag);
              return new Le(function (n, r) {
                (i._requests[t] = { resolve: n, reject: r }),
                  i._send({
                    message: {
                      action: "stripe-frame-action",
                      payload: { nonce: t, faReq: e },
                    },
                    type: "outer",
                    frameId: i.id,
                    controllerId: i._controllerId,
                  });
              });
            }),
            (i.action = {
              perform3DS2Challenge: function (e) {
                return i._sendFAReq({
                  tag: "PERFORM_3DS2_CHALLENGE",
                  value: e,
                });
              },
              perform3DS2Fingerprint: function (e) {
                return i._sendFAReq({
                  tag: "PERFORM_3DS2_FINGERPRINT",
                  value: e,
                });
              },
              show3DS2Spinner: function (e) {
                return i._sendFAReq({ tag: "SHOW_3DS2_SPINNER", value: e });
              },
              checkCanMakePayment: function (e) {
                return i._sendFAReq({
                  tag: "CHECK_CAN_MAKE_PAYMENT",
                  value: e,
                });
              },
              closeLightboxFrame: function (e) {
                return i._sendFAReq({ tag: "CLOSE_LIGHTBOX_FRAME", value: e });
              },
              openLightboxFrame: function (e) {
                return i._sendFAReq({ tag: "OPEN_LIGHTBOX_FRAME", value: e });
              },
            }),
            (i.type = e),
            (i.loaded = !1),
            (i._controllerId = n),
            (i._persistentMessages = []),
            (i._queuedMessages = []),
            (i._requests = {}),
            (i._listenerRegistry = r),
            (i.id = i._generateId()),
            (i._iframe = i._createIFrame(o)),
            i._on("load", function () {
              (i.loaded = !0),
                i._ensureMounted(),
                i.loaded &&
                  (i._persistentMessages.forEach(function (e) {
                    return i._send(e);
                  }),
                  i._queuedMessages.forEach(function (e) {
                    return i._send(e);
                  }),
                  (i._queuedMessages = []));
            }),
            i._on("title", function (e) {
              var t = e.title;
              i._iframe.setAttribute("title", t);
            }),
            i
          );
        }
        return (
          _(t, e),
          Rn(t, [
            {
              key: "_generateId",
              value: function () {
                return nn("__privateStripeFrame");
              },
            },
            {
              key: "send",
              value: function (e) {
                this._send({
                  message: e,
                  type: "outer",
                  frameId: this.id,
                  controllerId: this._controllerId,
                });
              },
            },
            {
              key: "sendPersistent",
              value: function (e) {
                this._ensureMounted();
                var t = {
                  message: e,
                  type: "outer",
                  frameId: this.id,
                  controllerId: this._controllerId,
                };
                (this._persistentMessages = [].concat(
                  p(this._persistentMessages),
                  [t]
                )),
                  this.loaded && vn(t);
              },
            },
            {
              key: "resolve",
              value: function (e, t) {
                this._requests[e] && this._requests[e].resolve(t);
              },
            },
            {
              key: "reject",
              value: function (e, t) {
                this._requests[e] && this._requests[e].reject(t);
              },
            },
            {
              key: "_send",
              value: function (e) {
                this._ensureMounted(),
                  this.loaded
                    ? vn(e)
                    : (this._queuedMessages = [].concat(
                        p(this._queuedMessages),
                        [e]
                      ));
              },
            },
            {
              key: "appendTo",
              value: function (e) {
                e.appendChild(this._iframe);
              },
            },
            {
              key: "unmount",
              value: function () {
                (this.loaded = !1), this._emit("unload");
              },
            },
            {
              key: "destroy",
              value: function () {
                this.unmount();
                var e = this._iframe.parentElement;
                e && e.removeChild(this._iframe), this._emit("destroy");
              },
            },
            {
              key: "_ensureMounted",
              value: function () {
                this._isMounted() || this.unmount();
              },
            },
            {
              key: "_isMounted",
              value: function () {
                return !!document.body && document.body.contains(this._iframe);
              },
            },
            {
              key: "_createIFrame",
              value: function (e) {
                var t = window.location.href.toString(),
                  n = nt(t),
                  r = n ? n.origin : "",
                  o =
                    e.queryString && "string" == typeof e.queryString
                      ? e.queryString
                      : cn(
                          Tn({}, e, {
                            origin: r,
                            referrer: t,
                            controllerId: this._controllerId,
                          })
                        ),
                  i = document.createElement("iframe");
                return (
                  i.setAttribute("frameborder", "0"),
                  i.setAttribute("allowTransparency", "true"),
                  i.setAttribute("scrolling", "no"),
                  i.setAttribute("name", this.id),
                  i.setAttribute("allowpaymentrequest", "true"),
                  (i.src = Ht(this.type) + "#" + o),
                  i
                );
              },
            },
          ]),
          t
        );
      })(An),
      Nn = In,
      Mn = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Cn = function e(t, n, r) {
        null === t && (t = Function.prototype);
        var o = Object.getOwnPropertyDescriptor(t, n);
        if (void 0 === o) {
          var i = Object.getPrototypeOf(t);
          return null === i ? void 0 : e(i, n, r);
        }
        if ("value" in o) return o.value;
        var a = o.get;
        if (void 0 !== a) return a.call(r);
      },
      jn = (function (e) {
        function t(e, n, r, o) {
          h(this, t);
          var i = m(
            this,
            (t.__proto__ || Object.getPrototypeOf(t)).call(this, e, n, r, o)
          );
          if (
            ((i.autoload = o.autoload || !1),
            "complete" === document.readyState)
          )
            i._ensureMounted();
          else {
            var a = i._ensureMounted.bind(i);
            i._listenerRegistry.addEventListener(
              document,
              "DOMContentLoaded",
              a
            ),
              i._listenerRegistry.addEventListener(window, "load", a),
              setTimeout(a, 5e3);
          }
          return i;
        }
        return (
          y(t, e),
          Mn(t, [
            {
              key: "_ensureMounted",
              value: function () {
                Cn(
                  t.prototype.__proto__ || Object.getPrototypeOf(t.prototype),
                  "_ensureMounted",
                  this
                ).call(this),
                  this._isMounted() || this._autoMount();
              },
            },
            {
              key: "_autoMount",
              value: function () {
                if (document.body) this.appendTo(document.body);
                else if (
                  "complete" === document.readyState ||
                  "interactive" === document.readyState
                )
                  throw new Ie(
                    "Stripe.js requires that your page has a <body> element."
                  );
                this.autoload && (this.loaded = !0);
              },
            },
            {
              key: "_createIFrame",
              value: function (e) {
                var n = Cn(
                  t.prototype.__proto__ || Object.getPrototypeOf(t.prototype),
                  "_createIFrame",
                  this
                ).call(this, e);
                return (
                  n.setAttribute("aria-hidden", "true"),
                  n.setAttribute("allowpaymentrequest", "true"),
                  n.setAttribute("tabIndex", "-1"),
                  _n(n),
                  n
                );
              },
            },
          ]),
          t
        );
      })(Nn),
      Ln = jn,
      xn = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      qn = (function (e) {
        function t() {
          return (
            v(this, t),
            b(
              this,
              (t.__proto__ || Object.getPrototypeOf(t)).apply(this, arguments)
            )
          );
        }
        return (
          g(t, e),
          xn(t, [
            {
              key: "_generateId",
              value: function () {
                return this._controllerId;
              },
            },
          ]),
          t
        );
      })(Ln),
      Dn = qn,
      Bn = function (e) {
        return /Edge\//i.test(e);
      },
      Fn = function (e) {
        return /(MSIE ([0-9]{1,}[.0-9]{0,})|Trident\/)/i.test(e);
      },
      Un = function (e) {
        return /SamsungBrowser/.test(e);
      },
      Hn = function (e) {
        return /iPad|iPhone/i.test(e) && !Fn(e);
      },
      Gn = function (e) {
        return /Android/i.test(e) && !Fn(e);
      },
      Wn = window.navigator.userAgent,
      Yn = Bn(Wn),
      zn =
        ((function (e) {
          /Edge\/((1[0-6]\.)|0\.)/i.test(e);
        })(Wn),
        Fn(Wn)),
      Kn =
        ((function (e) {
          /MSIE ([0-9]{1,}[.0-9]{0,})/i.test(e);
        })(Wn),
        Hn(Wn)),
      Vn =
        ((function (e) {
          Hn(e) || Gn(e);
        })(Wn),
        Gn(Wn),
        (function (e) {
          /Android 4\./i.test(e) && !/Chrome/i.test(e) && Gn(e);
        })(Wn),
        (function (e) {
          return /^((?!chrome|android).)*safari/i.test(e) && !Un(e);
        })(Wn)),
      Jn =
        ((function (e) {
          /Firefox\//i.test(e);
        })(Wn),
        (function (e) {
          /Firefox\/(50|51|[0-4]?\d)([^\d]|$)/i.test(e);
        })(Wn),
        Un(Wn)),
      Xn =
        ((function (e) {
          /Chrome\/(6[6-9]|[7-9]\d+|[1-9]\d{2,})/i.test(e);
        })(Wn),
        (function (e) {
          return (
            /AppleWebKit/i.test(e) && !/Chrome/i.test(e) && !Bn(e) && !Fn(e)
          );
        })(Wn)),
      Qn = (function (e) {
        return /Chrome/i.test(e) && !Bn(e);
      })(Wn),
      $n = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Zn = function e(t, n, r) {
        null === t && (t = Function.prototype);
        var o = Object.getOwnPropertyDescriptor(t, n);
        if (void 0 === o) {
          var i = Object.getPrototypeOf(t);
          return null === i ? void 0 : e(i, n, r);
        }
        if ("value" in o) return o.value;
        var a = o.get;
        if (void 0 !== a) return a.call(r);
      },
      er = {
        border: "none",
        margin: "0",
        padding: "0",
        width: "1px",
        "min-width": "100%",
        overflow: "hidden",
        display: "block",
        "user-select": "none",
      },
      tr = (function (e) {
        function t() {
          return (
            E(this, t),
            w(
              this,
              (t.__proto__ || Object.getPrototypeOf(t)).apply(this, arguments)
            )
          );
        }
        return (
          S(t, e),
          $n(t, [
            {
              key: "update",
              value: function (e) {
                this.send({ action: "stripe-user-update", payload: e });
              },
            },
            {
              key: "updateStyle",
              value: function (e) {
                var t = this;
                Object.keys(e).forEach(function (n) {
                  t._iframe.style[n] = e[n];
                });
              },
            },
            {
              key: "focus",
              value: function (e) {
                this.loaded &&
                  (Vn && e
                    ? this._iframe.focus()
                    : this.send({ action: "stripe-user-focus", payload: {} }));
              },
            },
            {
              key: "blur",
              value: function () {
                this.loaded &&
                  (this._iframe.contentWindow.blur(), this._iframe.blur());
              },
            },
            {
              key: "clear",
              value: function () {
                this.send({ action: "stripe-user-clear", payload: {} });
              },
            },
            {
              key: "_createIFrame",
              value: function (e) {
                var n = Zn(
                  t.prototype.__proto__ || Object.getPrototypeOf(t.prototype),
                  "_createIFrame",
                  this
                ).call(this, e);
                return (
                  n.setAttribute("title", "Secure payment input frame"),
                  fn(n, er),
                  n
                );
              },
            },
          ]),
          t
        );
      })(Nn),
      nr = tr,
      rr = function (e, t) {
        var n = !1;
        return function () {
          if (n) throw new Ie(t);
          n = !0;
          try {
            return e.apply(void 0, arguments).then(
              function (e) {
                return (n = !1), e;
              },
              function (e) {
                throw ((n = !1), e);
              }
            );
          } catch (e) {
            throw ((n = !1), e);
          }
        };
      },
      or = function (e) {
        var t = e;
        return function () {
          t && (t.apply(void 0, arguments), (t = null));
        };
      },
      ir = function () {
        return mn(function (e) {
          var t = e.style,
            n = t.position,
            r = t.top,
            o = t.left,
            i = t.bottom,
            a = t.right,
            c = t.overflow,
            s = document.documentElement
              ? document.documentElement.style
              : { overflow: "", scrollBehavior: "" },
            u = s.overflow,
            l = s.scrollBehavior,
            p = window,
            f = p.pageXOffset,
            d = p.pageYOffset,
            _ = document.documentElement
              ? window.innerWidth - document.documentElement.offsetWidth
              : 0,
            h = document.documentElement
              ? window.innerHeight - document.documentElement.offsetHeight
              : 0;
          return (
            (e.style.position = "fixed"),
            (e.style.overflow = "hidden"),
            document.documentElement &&
              ((document.documentElement.style.overflow = "visible"),
              (document.documentElement.style.scrollBehavior = "auto")),
            (e.style.top = -d + "px"),
            (e.style.left = -f + "px"),
            (e.style.right = _ + "px"),
            (e.style.bottom = h + "px"),
            or(function () {
              (e.style.position = n),
                (e.style.top = r),
                (e.style.left = o),
                (e.style.bottom = i),
                (e.style.right = a),
                (e.style.overflow = c),
                document.documentElement &&
                  (document.documentElement.style.overflow = u),
                window.scrollTo(f, d),
                document.documentElement &&
                  (document.documentElement.style.scrollBehavior = l);
            })
          );
        });
      },
      ar = function (e, t) {
        return e ? window.getComputedStyle(e, t) : null;
      },
      cr = ar,
      sr = function (e, t) {
        var n = Array.prototype.slice
          .call(
            document.querySelectorAll(
              "a[href], area[href], input:not([disabled]),\n  select:not([disabled]), textarea:not([disabled]), button:not([disabled]),\n  object, embed, *[tabindex], *[contenteditable]"
            )
          )
          .filter(function (e) {
            var t = e.getAttribute("tabindex"),
              n = !t || parseInt(t, 10) >= 0,
              r = e.getBoundingClientRect(),
              o = cr(e),
              i =
                r.width > 0 &&
                r.height > 0 &&
                o &&
                "hidden" !== o.getPropertyValue("visibility");
            return n && i;
          });
        return n[
          Ge(n, function (t) {
            return t === e || e.contains(t);
          }) + ("previous" === t ? -1 : 1)
        ];
      },
      ur = function (e) {
        var t = [],
          n = ze(document.querySelectorAll("*"), function (n) {
            var r = n.getAttribute("tabindex") || "";
            e !== n && (n.tabIndex = -1), t.push({ element: n, tabIndex: r });
          });
        return or(function () {
          n.then(function () {
            return ze(t, function (e) {
              var t = e.element,
                n = e.tabIndex;
              "" === n
                ? t.removeAttribute("tabindex")
                : t.setAttribute("tabindex", n);
            });
          });
        });
      },
      lr =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      pr = {
        display: "block",
        position: "fixed",
        "z-index": "2147483647",
        background: "rgba(40,40,40,0)",
        transition: "background 400ms ease",
        "will-change": "background",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
      },
      fr = lr({}, pr, { background: "rgba(40,40,40,0.75)" }),
      dr = function e(t) {
        var n = this,
          r = t.lockScrolling,
          o = t.lockFocus,
          i = t.lockFocusOn,
          a = t.listenerRegistry;
        P(this, e),
          (this.domElement = document.createElement("div")),
          (this._runOnHide = []),
          (this.mount = function () {
            mn(function (e) {
              (n.domElement.style.display = "none"),
                e.contains(n.domElement) ||
                  e.insertBefore(n.domElement, e.firstChild);
            });
          }),
          (this.show = function () {
            if ((fn(n.domElement, pr), n._lockScrolling)) {
              var e = ir();
              n._runOnHide.push(e);
            }
            if (n._lockFocus) {
              var t = ur(n._lockFocusOn);
              n._runOnHide.push(t);
            }
          }),
          (this.fadeIn = function () {
            setTimeout(function () {
              fn(n.domElement, fr);
            });
          }),
          (this.fadeOut = function () {
            return new Le(function (e) {
              fn(n.domElement, pr),
                setTimeout(e, 500),
                n._listenerRegistry.addEventListener(
                  n.domElement,
                  "transitionend",
                  e
                );
            }).then(function () {
              for (n.domElement.style.display = "none"; n._runOnHide.length; )
                n._runOnHide.pop()();
            });
          }),
          (this.unmount = function () {
            mn(function (e) {
              e.removeChild(n.domElement);
            });
          }),
          (this._lockScrolling = !!r),
          (this._lockFocus = !!o),
          (this._lockFocusOn = i || null),
          (this._listenerRegistry = a);
      },
      _r = dr,
      hr =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      mr = function e(t, n, r) {
        null === t && (t = Function.prototype);
        var o = Object.getOwnPropertyDescriptor(t, n);
        if (void 0 === o) {
          var i = Object.getPrototypeOf(t);
          return null === i ? void 0 : e(i, n, r);
        }
        if ("value" in o) return o.value;
        var a = o.get;
        if (void 0 !== a) return a.call(r);
      },
      yr = {
        position: "absolute",
        left: "0",
        top: "0",
        height: "100%",
        width: "100%",
      },
      vr = (function (e) {
        function t(e) {
          var n = e.type,
            r = e.controllerId,
            o = e.listenerRegistry,
            i = e.options;
          O(this, t);
          var a = k(
            this,
            (t.__proto__ || Object.getPrototypeOf(t)).call(
              this,
              n,
              r,
              o,
              hr({}, i)
            )
          );
          return (
            (a._autoMount = function () {
              a.appendTo(a._backdrop.domElement), a._backdrop.mount();
            }),
            (a.show = function () {
              a._backdrop.show(), fn(a._iframe, yr);
            }),
            (a.fadeInBackdrop = function () {
              a._backdrop.fadeIn();
            }),
            (a._backdropFadeoutPromise = null),
            (a.fadeOutBackdrop = function () {
              return (
                a._backdropFadeoutPromise ||
                  (a._backdropFadeoutPromise = a._backdrop.fadeOut()),
                a._backdropFadeoutPromise
              );
            }),
            (a.destroy = function () {
              return a.fadeOutBackdrop().then(function () {
                a._backdrop.unmount(),
                  mr(
                    t.prototype.__proto__ || Object.getPrototypeOf(t.prototype),
                    "destroy",
                    a
                  ).call(a);
              });
            }),
            (a._backdrop = new _r({
              lockScrolling: !0,
              lockFocus: !0,
              lockFocusOn: a._iframe,
              listenerRegistry: o,
            })),
            a._autoMount(),
            a
          );
        }
        return A(t, e), t;
      })(Nn),
      br = vr,
      gr =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Er = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      wr = function e(t, n, r) {
        null === t && (t = Function.prototype);
        var o = Object.getOwnPropertyDescriptor(t, n);
        if (void 0 === o) {
          var i = Object.getPrototypeOf(t);
          return null === i ? void 0 : e(i, n, r);
        }
        if ("value" in o) return o.value;
        var a = o.get;
        if (void 0 !== a) return a.call(r);
      },
      Sr = {
        display: "block",
        position: "absolute",
        "z-index": "1000",
        width: "1px",
        "min-width": "100%",
        margin: "2px 0 0 0",
        padding: "0",
        border: "none",
        overflow: "hidden",
      },
      Pr = (function (e) {
        function t() {
          return (
            T(this, t),
            R(
              this,
              (t.__proto__ || Object.getPrototypeOf(t)).apply(this, arguments)
            )
          );
        }
        return (
          I(t, e),
          Er(t, [
            {
              key: "updateStyle",
              value: function (e) {
                var t = this;
                Object.keys(e).forEach(function (n) {
                  t._iframe.style[n] = e[n];
                });
              },
            },
            {
              key: "update",
              value: function (e) {
                this.send({ action: "stripe-user-update", payload: e });
              },
            },
            {
              key: "_createIFrame",
              value: function (e) {
                var n = wr(
                  t.prototype.__proto__ || Object.getPrototypeOf(t.prototype),
                  "_createIFrame",
                  this
                ).call(this, gr({}, e, { isSecondaryFrame: !0 }));
                return fn(n, Sr), (n.style.height = "0"), n;
              },
            },
          ]),
          t
        );
      })(Nn),
      Or = Pr,
      kr = function (e) {
        var t = nt(e),
          n = t ? t.host : "";
        return "stripe.com" === n || !!n.match(/\.stripe\.(com|me)$/);
      },
      Ar = function (e, t) {
        var n = nt(e),
          r = nt(t);
        return !(!n || !r) && n.origin === r.origin;
      },
      Tr = function (e) {
        return Ar(e, "https://js.stripe.com/v3/");
      },
      Rr = function (e) {
        return Tr(e) || kr(e);
      },
      Ir = [
        "button",
        "checkbox",
        "file",
        "hidden",
        "image",
        "submit",
        "radio",
        "reset",
      ],
      Nr = function (e) {
        var t = e.tagName;
        if (e.isContentEditable || "TEXTAREA" === t) return !0;
        if ("INPUT" !== t) return !1;
        var n = e.getAttribute("type");
        return -1 === Ir.indexOf(n);
      },
      Mr = Nr,
      Cr = function (e) {
        var t = e.name,
          n = e.value,
          r = e.expiresIn,
          o = e.path,
          i = e.domain,
          a = new Date(),
          c = r || 31536e6;
        a.setTime(a.getTime() + c);
        var s = o || "/",
          u = (n || "").replace(/[^!#-+\--:<-[\]-~]/g, encodeURIComponent),
          l =
            encodeURIComponent(t) +
            "=" +
            u +
            ";expires=" +
            a.toGMTString() +
            ";path=" +
            s +
            ";SameSite=Lax";
        return i && (l += ";domain=" + i), (document.cookie = l), l;
      },
      jr = function (e) {
        var t = He(document.cookie.split("; "), function (t) {
          var n = t.indexOf("=");
          return decodeURIComponent(t.substr(0, n)) === e;
        });
        if (t) {
          var n = t.indexOf("=");
          return decodeURIComponent(t.substr(n + 1));
        }
        return null;
      },
      Lr = function (e) {
        var t = {};
        return (
          e
            .replace(/\+/g, " ")
            .split("&")
            .forEach(function (e, n) {
              var r = e.split("="),
                o = decodeURIComponent(r[0]),
                i = void 0,
                a = t,
                c = 0,
                s = o.split("]["),
                u = s.length - 1;
              if (
                (/\[/.test(s[0]) && /\]$/.test(s[u])
                  ? ((s[u] = s[u].replace(/\]$/, "")),
                    (s = s.shift().split("[").concat(s)),
                    (u = s.length - 1))
                  : (u = 0),
                2 === r.length)
              )
                if (((i = decodeURIComponent(r[1])), u))
                  for (; c <= u; c++)
                    (o = "" === s[c] ? a.length : s[c]),
                      (a[o] =
                        c < u
                          ? a[o] || (s[c + 1] && isNaN(s[c + 1]) ? {} : [])
                          : i),
                      (a = a[o]);
                else
                  Array.isArray(t[o])
                    ? t[o].push(i)
                    : void 0 !== t[o]
                    ? (t[o] = [t[o], i])
                    : (t[o] = i);
              else o && (t[o] = "");
            }),
          t
        );
      },
      xr = Lr,
      qr = n(8),
      Dr = n.n(qr),
      Br =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Fr =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      Ur = function (e) {
        return (
          e &&
          "object" === (void 0 === e ? "undefined" : Fr(e)) &&
          (e.constructor === Array || e.constructor === Object)
        );
      },
      Hr = function (e) {
        return Ur(e)
          ? Array.isArray(e)
            ? e.slice(0, e.length)
            : Br({}, e)
          : e;
      },
      Gr = function e(t) {
        return function () {
          for (var n = arguments.length, r = Array(n), o = 0; o < n; o++)
            r[o] = arguments[o];
          if (Array.isArray(r[0]) && t) return Hr(r[0]);
          var i = Array.isArray(r[0]) ? [] : {};
          return (
            r.forEach(function (n) {
              n &&
                Object.keys(n).forEach(function (r) {
                  var o = i[r],
                    a = n[r],
                    c = Ur(o) && !(t && Array.isArray(o));
                  "object" === (void 0 === a ? "undefined" : Fr(a)) && c
                    ? (i[r] = e(t)(o, Hr(a)))
                    : void 0 !== a
                    ? (i[r] = Ur(a) ? e(t)(a) : Hr(a))
                    : void 0 !== o && (i[r] = o);
                });
            }),
            i
          );
        };
      },
      Wr = (Gr(!1), Gr(!0)),
      Yr = Jt.replace(/\/$/, ""),
      zr = (function (e) {
        var t = N({}, "_1776170249", !0);
        try {
          var n = xr(e.slice(e.indexOf("?") + 1));
          Object.keys(n).forEach(function (e) {
            var r = Dr()(e),
              o = n[e];
            switch (r) {
              case "_1776170249":
                "false" === o && (t[r] = !1);
            }
          });
        } catch (e) {}
        return t;
      })(
        (function (e) {
          try {
            if (e.currentScript) return e.currentScript.src;
            var t = e.querySelectorAll('script[src^="' + Yr + '"]'),
              n = He(t, function (e) {
                var t = e.getAttribute("src") || "",
                  n = t.split("?")[0];
                return new RegExp("^" + Yr + "/?$").test(n);
              });
            return (n && n.getAttribute("src")) || "";
          } catch (e) {
            return "";
          }
        })(document)
      ),
      Kr = zr._1776170249,
      Vr = (function () {
        function e(e, t) {
          var n = [],
            r = !0,
            o = !1,
            i = void 0;
          try {
            for (
              var a, c = e[Symbol.iterator]();
              !(r = (a = c.next()).done) &&
              (n.push(a.value), !t || n.length !== t);
              r = !0
            );
          } catch (e) {
            (o = !0), (i = e);
          } finally {
            try {
              !r && c.return && c.return();
            } finally {
              if (o) throw i;
            }
          }
          return n;
        }
        return function (t, n) {
          if (Array.isArray(t)) return t;
          if (Symbol.iterator in Object(t)) return e(t, n);
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance"
          );
        };
      })(),
      Jr = function () {
        var e = [];
        return {
          addEventListener: function (t, n, r) {
            t.addEventListener(n, r), e.push([t, n, r]);
          },
          removeEventListener: function (t, n, r) {
            t.removeEventListener(n, r),
              (e = e.filter(function (e) {
                var o = Vr(e, 3),
                  i = o[0],
                  a = o[1],
                  c = o[2];
                return i !== t || a !== n || c !== r;
              }));
          },
        };
      },
      Xr = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Qr = "__privateStripeMetricsController",
      $r = { MERCHANT: "merchant", SESSION: "session" },
      Zr = "NA",
      eo = function (e) {
        return 42 === e.length;
      },
      to = function (e, t, n) {
        return n ? (!e || (!eo(e) && eo(t)) ? t : e) : rn();
      },
      no = (function () {
        function e() {
          var t = this,
            n =
              arguments.length > 0 && void 0 !== arguments[0]
                ? arguments[0]
                : {};
          if (
            (M(this, e),
            (this._controllerFrame = null),
            (this._latencies = []),
            (this._handleMessage = function (e) {
              return function (n) {
                var r = n.data,
                  o = n.origin;
                if (Rr(o) && "string" == typeof r)
                  try {
                    var i = JSON.parse(r),
                      a = i.originatingScript,
                      c = i.payload;
                    if ("m2" === a) {
                      var s = c.guid,
                        u = c.muid,
                        l = c.sid;
                      (t._guid = s),
                        (t._muid = t._getID($r.MERCHANT, u)),
                        (t._sid = t._getID($r.SESSION, l)),
                        e();
                    }
                  } catch (e) {}
              };
            }),
            n.checkoutIds)
          ) {
            var r = n.checkoutIds,
              o = r.muid,
              i = r.sid;
            (this._guid = Zr),
              (this._muid = o),
              (this._sid = i),
              (this._doNotPersist = !0);
          } else
            (this._guid = Zr),
              (this._muid = this._getID($r.MERCHANT)),
              (this._sid = this._getID($r.SESSION)),
              (this._doNotPersist = !1);
          (this._listenerRegistry = Jr()),
            (this._idsPromise = new Le(function (e) {
              t._establishMessageChannel(e);
            })),
            (this._id = nn(Qr)),
            Kr &&
              ((this._controllerFrame = new Dn(
                Dt.METRICS_CONTROLLER,
                this._id,
                this._listenerRegistry,
                { autoload: !0, queryString: this._buildFrameQueryString() }
              )),
              this._startIntervalCheck(),
              setTimeout(
                this._testLatency.bind(this),
                2e3 + 500 * Math.random()
              ));
        }
        return (
          Xr(e, [
            {
              key: "ids",
              value: function () {
                return { guid: this._guid, muid: this._muid, sid: this._sid };
              },
            },
            {
              key: "idsPromise",
              value: function () {
                var e = this;
                return this._idsPromise.then(function () {
                  return e.ids();
                });
              },
            },
            {
              key: "_establishMessageChannel",
              value: function (e) {
                if (!Kr) return (this._guid = rn()), void e();
                this._listenerRegistry.addEventListener(
                  window,
                  "message",
                  this._handleMessage(e)
                );
              },
            },
            {
              key: "_startIntervalCheck",
              value: function () {
                var e = this,
                  t = window.location.href;
                setInterval(function () {
                  var n = window.location.href;
                  n !== t &&
                    (e.send(function (e) {
                      return {
                        action: "ping",
                        payload: {
                          sid: e.sid,
                          muid: e.muid,
                          title: document.title,
                          referrer: document.referrer,
                          url: document.location.href,
                          version: 6,
                        },
                      };
                    }),
                    (t = n));
                }, 5e3);
              },
            },
            {
              key: "report",
              value: function (e, t) {
                this.send(function (n) {
                  return {
                    action: "track",
                    payload: {
                      sid: n.sid,
                      muid: n.muid,
                      url: document.location.href,
                      source: e,
                      data: t,
                      version: 6,
                    },
                  };
                });
              },
            },
            {
              key: "send",
              value: function (e) {
                var t = this;
                this._idsPromise.then(function () {
                  try {
                    t._controllerFrame && t._controllerFrame.send(e(t.ids()));
                  } catch (e) {}
                });
              },
            },
            {
              key: "_testLatency",
              value: function () {
                var e = this,
                  t = new Date(),
                  n = function n() {
                    try {
                      var r = new Date();
                      e._latencies.push(r - t),
                        e._latencies.length >= 10 &&
                          (e.report("mouse-timings-10", e._latencies),
                          e._listenerRegistry.removeEventListener(
                            document,
                            "mousemove",
                            n
                          )),
                        (t = r);
                    } catch (e) {}
                  };
                this._listenerRegistry.addEventListener(
                  document,
                  "mousemove",
                  n
                );
              },
            },
            {
              key: "_extractMetaReferrerPolicy",
              value: function () {
                var e = document.querySelector("meta[name=referrer]");
                return null != e && e instanceof HTMLMetaElement
                  ? e.content.toLowerCase()
                  : null;
              },
            },
            {
              key: "_extractUrl",
              value: function (e) {
                var t = document.location.href;
                switch (e) {
                  case "origin":
                  case "strict-origin":
                  case "origin-when-cross-origin":
                  case "strict-origin-when-cross-origin":
                    return document.location.origin;
                  case "unsafe-url":
                    return t.split("#")[0];
                  default:
                    return t;
                }
              },
            },
            {
              key: "_buildFrameQueryString",
              value: function () {
                var e = this._extractMetaReferrerPolicy(),
                  t = this._extractUrl(e),
                  n = {
                    url: t,
                    title: document.title,
                    referrer: document.referrer,
                    muid: this._muid,
                    sid: this._sid,
                    version: 6,
                    preview: Rr(t),
                  };
                return (
                  null != e && (n.metaReferrerPolicy = e),
                  Object.keys(n)
                    .map(function (e) {
                      return null != n[e]
                        ? e + "=" + encodeURIComponent(n[e].toString())
                        : null;
                    })
                    .join("&")
                );
              },
            },
            {
              key: "_getID",
              value: function (e) {
                var t =
                  arguments.length > 1 && void 0 !== arguments[1]
                    ? arguments[1]
                    : Zr;
                switch (e) {
                  case $r.MERCHANT:
                    if (this._doNotPersist) return to(this._muid, t, Kr);
                    try {
                      var n = to(jr("__stripe_mid"), t, Kr);
                      return (
                        eo(n) &&
                          Cr({
                            name: "__stripe_mid",
                            value: n,
                            domain: "." + document.location.hostname,
                          }),
                        n
                      );
                    } catch (e) {
                      return Zr;
                    }
                  case $r.SESSION:
                    if (this._doNotPersist) return to(this._sid, t, Kr);
                    try {
                      var r = to(jr("__stripe_sid"), t, Kr);
                      return (
                        eo(r) &&
                          Cr({
                            name: "__stripe_sid",
                            value: r,
                            domain: "." + document.location.hostname,
                            expiresIn: 18e5,
                          }),
                        r
                      );
                    } catch (e) {
                      return Zr;
                    }
                  default:
                    throw new Error("Invalid ID type specified: " + e);
                }
              },
            },
          ]),
          e
        );
      })(),
      ro = null,
      oo = function () {
        return ro;
      },
      io = function () {
        var e =
          arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
        return (ro = new no(e));
      },
      ao = !1,
      co = function () {
        var e = oo();
        e &&
          (ao ||
            ((ao = !0),
            e.send(function (e) {
              return {
                action: "ping",
                payload: {
                  v2: 2,
                  sid: e.sid,
                  muid: e.muid,
                  title: document.title,
                  referrer: document.referrer,
                  url: document.location.href,
                  version: 6,
                },
              };
            }),
            e.send(function (t) {
              return {
                action: "track",
                payload: {
                  sid: t.sid,
                  muid: t.muid,
                  url: document.location.href,
                  source: "mouse-timings-10-v2",
                  data: e._latencies,
                  version: 6,
                },
              };
            })));
      },
      so = co,
      uo =
        ((Ee = {}),
        C(Ee, Wt.card, {
          unique: !0,
          conflict: [Wt.cardNumber, Wt.cardExpiry, Wt.cardCvc, Wt.postalCode],
          beta: !1,
        }),
        C(Ee, Wt.cardNumber, { unique: !0, conflict: [Wt.card], beta: !1 }),
        C(Ee, Wt.cardExpiry, { unique: !0, conflict: [Wt.card], beta: !1 }),
        C(Ee, Wt.cardCvc, { unique: !0, conflict: [Wt.card], beta: !1 }),
        C(Ee, Wt.postalCode, { unique: !0, conflict: [Wt.card], beta: !1 }),
        C(Ee, Wt.paymentRequestButton, { unique: !0, conflict: [], beta: !1 }),
        C(Ee, Wt.iban, { unique: !0, conflict: [], beta: !1 }),
        C(Ee, Wt.idealBank, { unique: !0, conflict: [], beta: !1 }),
        C(Ee, Wt.auBankAccount, { unique: !0, beta: !1, conflict: [] }),
        C(Ee, Wt.fpxBank, { unique: !0, beta: !1, conflict: [] }),
        Ee),
      lo = uo,
      po =
        ((we = {}),
        j(we, Wt.card, Dt.CARD_ELEMENT),
        j(we, Wt.cardNumber, Dt.CARD_ELEMENT),
        j(we, Wt.cardExpiry, Dt.CARD_ELEMENT),
        j(we, Wt.cardCvc, Dt.CARD_ELEMENT),
        j(we, Wt.postalCode, Dt.CARD_ELEMENT),
        j(we, Wt.paymentRequestButton, Dt.PAYMENT_REQUEST_ELEMENT),
        j(we, Wt.iban, Dt.IBAN_ELEMENT),
        j(we, Wt.idealBank, Dt.IDEAL_BANK_ELEMENT),
        j(we, Wt.auBankAccount, Dt.AU_BANK_ACCOUNT_ELEMENT),
        j(we, Wt.fpxBank, Dt.FPX_BANK_ELEMENT),
        we),
      fo = po,
      _o = ["brand"],
      ho = ["country", "bankName"],
      mo = ["bankName", "branchName"],
      yo =
        ((Se = {}),
        L(Se, Wt.card, _o),
        L(Se, Wt.cardNumber, _o),
        L(Se, Wt.iban, ho),
        L(Se, Wt.auBankAccount, mo),
        Se),
      vo =
        ((Pe = {}),
        L(Pe, Wt.idealBank, { secondary: Wt.idealBankSecondary }),
        L(Pe, Wt.fpxBank, { secondary: Wt.fpxBankSecondary }),
        Pe),
      bo =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      go = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Eo =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      wo = "__privateStripeController",
      So = !1,
      Po = function (e, t) {
        return (
          document.activeElement === e._iframe ||
          (e._iframe.parentElement && document.activeElement === t)
        );
      },
      Oo = function (e) {
        return "object" === (void 0 === e ? "undefined" : Eo(e)) &&
          null !== e &&
          "IntegrationError" === e.name
          ? new Ie("string" == typeof e.message ? e.message : "")
          : e;
      },
      ko = (function () {
        function e(t) {
          q(this, e), Ao.call(this);
          var n = t.listenerRegistry,
            r = t.startTimestamp,
            o = x(t, ["listenerRegistry", "startTimestamp"]),
            i = o.apiKey,
            a = o.stripeAccount,
            c = o.stripeJsId,
            s = o.locale;
          (this._id = nn(wo)),
            (this._stripeJsId = c),
            (this._apiKey = i),
            (this._stripeAccount = a),
            (this._listenerRegistry = n),
            (this._flags = []),
            Math.random() >= 0.5 && this._flags.push("a"),
            (this._controllerFrame = new Dn(
              Dt.CONTROLLER,
              this._id,
              this._listenerRegistry,
              bo({}, o, { startTime: r.getAsPosixTime(), flags: this._flags })
            )),
            (this._frames = {}),
            (this._requests = {}),
            this._setupPostMessage(),
            (this._handleMessage = wn(this._handleMessage, this)),
            this.action.fetchLocale({ locale: s || "auto" });
        }
        return (
          go(e, [
            {
              key: "registerWrapper",
              value: function (e) {
                this._controllerFrame.send({
                  action: "stripe-wrapper-register",
                  payload: { wrapperLibrary: e },
                });
              },
            },
          ]),
          e
        );
      })(),
      Ao = function () {
        var e = this;
        (this._sendCAReq = function (t) {
          var n = nn(t.tag);
          return new Le(function (r, o) {
            (e._requests[n] = { resolve: r, reject: o }),
              e._controllerFrame.send({
                action: "stripe-safe-controller-action-request",
                payload: { nonce: n, caReq: t },
              });
          });
        }),
          (this.livemode = function () {
            var t = e._apiKey;
            return /^pk_test_/.test(t)
              ? "testmode"
              : /^pk_live_/.test(t)
              ? "livemode"
              : "unknown";
          }),
          (this.action = {
            retrievePaymentIntent: function (t) {
              return e._sendCAReq({ tag: "RETRIEVE_PAYMENT_INTENT", value: t });
            },
            confirmPaymentIntent: function (t) {
              return e._sendCAReq({ tag: "CONFIRM_PAYMENT_INTENT", value: t });
            },
            cancelPaymentIntentSource: function (t) {
              return e._sendCAReq({
                tag: "CANCEL_PAYMENT_INTENT_SOURCE",
                value: t,
              });
            },
            confirmSetupIntent: function (t) {
              return e._sendCAReq({ tag: "CONFIRM_SETUP_INTENT", value: t });
            },
            retrieveSetupIntent: function (t) {
              return e._sendCAReq({ tag: "RETRIEVE_SETUP_INTENT", value: t });
            },
            cancelSetupIntentSource: function (t) {
              return e._sendCAReq({
                tag: "CANCEL_SETUP_INTENT_SOURCE",
                value: t,
              });
            },
            fetchLocale: function (t) {
              return e._sendCAReq({ tag: "FETCH_LOCALE", value: t });
            },
            updateCSSFonts: function (t) {
              return e._sendCAReq({ tag: "UPDATE_CSS_FONTS", value: t });
            },
            createApplePaySession: function (t) {
              return e._sendCAReq({
                tag: "CREATE_APPLE_PAY_SESSION",
                value: t,
              });
            },
            retrieveSource: function (t) {
              return e._sendCAReq({ tag: "RETRIEVE_SOURCE", value: t });
            },
            tokenizeWithElement: function (t) {
              return e._sendCAReq({ tag: "TOKENIZE_WITH_ELEMENT", value: t });
            },
            tokenizeCvcUpdate: function (t) {
              return e._sendCAReq({ tag: "TOKENIZE_CVC_UPDATE", value: t });
            },
            tokenizeWithData: function (t) {
              return e._sendCAReq({ tag: "TOKENIZE_WITH_DATA", value: t });
            },
            createSourceWithElement: function (t) {
              return e._sendCAReq({
                tag: "CREATE_SOURCE_WITH_ELEMENT",
                value: t,
              });
            },
            createSourceWithData: function (t) {
              return e._sendCAReq({ tag: "CREATE_SOURCE_WITH_DATA", value: t });
            },
            createPaymentMethodWithElement: function (t) {
              return e._sendCAReq({
                tag: "CREATE_PAYMENT_METHOD_WITH_ELEMENT",
                value: t,
              });
            },
            createPaymentMethodWithData: function (t) {
              return e._sendCAReq({
                tag: "CREATE_PAYMENT_METHOD_WITH_DATA",
                value: t,
              });
            },
            createPaymentPage: function (t) {
              return e._sendCAReq({ tag: "CREATE_PAYMENT_PAGE", value: t });
            },
            createPaymentPageWithSession: function (t) {
              return e._sendCAReq({
                tag: "CREATE_PAYMENT_PAGE_WITH_SESSION",
                value: t,
              });
            },
            createRadarSession: function (t) {
              return e._sendCAReq({ tag: "CREATE_RADAR_SESSION", value: t });
            },
            authenticate3DS2: function (t) {
              return e._sendCAReq({ tag: "AUTHENTICATE_3DS2", value: t });
            },
            verifyMicrodepositsForPayment: function (t) {
              return e._sendCAReq({
                tag: "VERIFY_MICRODEPOSITS_FOR_PAYMENT",
                value: t,
              });
            },
            verifyMicrodepositsForSetup: function (t) {
              return e._sendCAReq({
                tag: "VERIFY_MICRODEPOSITS_FOR_SETUP",
                value: t,
              });
            },
          }),
          (this.createElementFrame = function (t, n) {
            var r = n.groupId,
              o = x(n, ["groupId"]),
              i = new nr(
                t,
                e._id,
                e._listenerRegistry,
                bo({}, o, {
                  keyMode: $e(e._apiKey),
                  apiKey: e._apiKey,
                  flags: e._flags,
                })
              );
            return e._setupFrame(i, t, r);
          }),
          (this.createSecondaryElementFrame = function (t, n) {
            var r = n.groupId,
              o = x(n, ["groupId"]),
              i = new Or(
                t,
                e._id,
                e._listenerRegistry,
                bo({}, o, { keyMode: $e(e._apiKey) })
              );
            return e._setupFrame(i, t, r);
          }),
          (this.createHiddenFrame = function (t, n) {
            var r = new Ln(t, e._id, e._listenerRegistry, n);
            return e._setupFrame(r, t);
          }),
          (this.createLightboxFrame = function (t) {
            var n = t.type,
              r = t.options,
              o = new br({
                type: n,
                controllerId: e._id,
                listenerRegistry: e._listenerRegistry,
                options: r,
              });
            return e._setupFrame(o, n);
          }),
          (this._setupFrame = function (t, n, r) {
            return (
              (e._frames[t.id] = t),
              e._controllerFrame.sendPersistent({
                action: "stripe-user-createframe",
                payload: { newFrameId: t.id, frameType: n, groupId: r },
              }),
              t._on("unload", function () {
                e._controllerFrame.sendPersistent({
                  action: "stripe-frame-unload",
                  payload: { unloadedFrameId: t.id },
                });
              }),
              t._on("destroy", function () {
                delete e._frames[t.id],
                  e._controllerFrame.sendPersistent({
                    action: "stripe-frame-destroy",
                    payload: { destroyedFrameId: t.id },
                  });
              }),
              t._on("load", function () {
                e._controllerFrame.sendPersistent({
                  action: "stripe-frame-load",
                  payload: { loadedFrameId: t.id },
                }),
                  e._controllerFrame.loaded &&
                    t.send({ action: "stripe-controller-load", payload: {} });
              }),
              t
            );
          }),
          (this.report = function (t) {
            var n =
              arguments.length > 1 && void 0 !== arguments[1]
                ? arguments[1]
                : {};
            e._controllerFrame.send({
              action: "stripe-controller-report",
              payload: { event: t, data: n },
            });
          }),
          (this.warn = function () {
            for (var t = arguments.length, n = Array(t), r = 0; r < t; r++)
              n[r] = arguments[r];
            e._controllerFrame.send({
              action: "stripe-controller-warn",
              payload: { args: n },
            });
          }),
          (this.controllerFor = function () {
            return "outer";
          }),
          (this._setupPostMessage = function () {
            e._listenerRegistry.addEventListener(window, "message", function (
              t
            ) {
              var n = t.data,
                r = t.origin,
                o = bn(n);
              o && Ar(Qt, r) && e._handleMessage(o);
            });
          }),
          (this._handleMessage = function (t) {
            var n = t.controllerId,
              r = t.frameId,
              o = t.message,
              i = e._frames[r];
            if (n === e._id)
              switch (o.action) {
                case "stripe-frame-event":
                  var a = o.payload,
                    c = a.event,
                    s = a.data;
                  if (i) {
                    if (Kn) {
                      var u = i._iframe.parentElement,
                        l =
                          u && u.querySelector(".__PrivateStripeElement-input");
                      if ("focus" === c && !So && !Po(i, l)) {
                        l && l.focus(), (So = !0);
                        break;
                      }
                      if ("blur" === c && So) {
                        So = !1;
                        break;
                      }
                      "blur" === c &&
                        setTimeout(function () {
                          var e = document.activeElement;
                          if (e && !Po(i, l) && !Mr(e)) {
                            var t =
                              u &&
                              u.querySelector(
                                ".__PrivateStripeElement-safariInput"
                              );
                            if (t) {
                              var n = t;
                              (n.disabled = !1),
                                n.focus(),
                                n.blur(),
                                (n.disabled = !0);
                            }
                            e.focus();
                          }
                        }, 400);
                    }
                    i._emit(c, s);
                  }
                  break;
                case "stripe-frame-action-response":
                  i && i.resolve(o.payload.nonce, o.payload.faRes);
                  break;
                case "stripe-frame-action-error":
                  i && i.reject(o.payload.nonce, Oo(o.payload.faErr));
                  break;
                case "stripe-frame-error":
                  throw new Ie(o.payload.message);
                case "stripe-integration-error":
                  i &&
                    i._emit("__privateIntegrationError", {
                      message: o.payload.message,
                    });
                  break;
                case "stripe-controller-load":
                  e._controllerFrame._emit("load"),
                    Object.keys(e._frames).forEach(function (t) {
                      return e._frames[t].send({
                        action: "stripe-controller-load",
                        payload: {},
                      });
                    });
                  break;
                case "stripe-safe-controller-action-response":
                  e._requests[o.payload.nonce] &&
                    e._requests[o.payload.nonce].resolve(o.payload.caRes);
                  break;
                case "stripe-safe-controller-action-error":
                  e._requests[o.payload.nonce] &&
                    e._requests[o.payload.nonce].reject(Oo(o.payload.caErr));
                  break;
                case "stripe-api-call":
                  so();
              }
          });
      },
      To = ko,
      Ro = function () {
        var e = document.querySelectorAll("meta[name=viewport][content]"),
          t = e[e.length - 1];
        return t && t instanceof HTMLMetaElement ? t.content : "";
      },
      Io = function (e) {
        Ro().match(/width=device-width/) ||
          e(
            'Elements requires "width=device-width" be set in your page\'s viewport meta tag.\n       For more information: https://stripe.com/docs/js/appendix/viewport_meta_requirements'
          );
      },
      No = {
        checkout_beta_2: "checkout_beta_2",
        checkout_beta_3: "checkout_beta_3",
        checkout_beta_4: "checkout_beta_4",
        checkout_beta_testcards: "checkout_beta_testcards",
        payment_intent_beta_1: "payment_intent_beta_1",
        payment_intent_beta_2: "payment_intent_beta_2",
        payment_intent_beta_3: "payment_intent_beta_3",
        card_payment_method_beta_1: "card_payment_method_beta_1",
        acknowledge_ie9_deprecation: "acknowledge_ie9_deprecation",
        cvc_update_beta_1: "cvc_update_beta_1",
        google_pay_beta_1: "google_pay_beta_1",
        acss_debit_beta_1: "acss_debit_beta_1",
        afterpay_clearpay_pm_beta_1: "afterpay_clearpay_pm_beta_1",
        alipay_pm_beta_1: "alipay_pm_beta_1",
        au_bank_account_beta_1: "au_bank_account_beta_1",
        au_bank_account_beta_2: "au_bank_account_beta_2",
        bacs_debit_beta: "bacs_debit_beta",
        bancontact_pm_beta_1: "bancontact_pm_beta_1",
        boleto_pilot_pm_beta_1: "boleto_pilot_pm_beta_1",
        eps_pm_beta_1: "eps_pm_beta_1",
        fpx_bank_beta_1: "fpx_bank_beta_1",
        giropay_pm_beta_1: "giropay_pm_beta_1",
        grabpay_pm_beta_1: "grabpay_pm_beta_1",
        ideal_pm_beta_1: "ideal_pm_beta_1",
        oxxo_pm_beta_1: "oxxo_pm_beta_1",
        p24_pm_beta_1: "p24_pm_beta_1",
        sepa_pm_beta_1: "sepa_pm_beta_1",
        sofort_pm_beta_1: "sofort_pm_beta_1",
        wechat_pay_pm_beta_1: "wechat_pay_pm_beta_1",
        checkout_beta_locales: "checkout_beta_locales",
        stripe_js_beta_locales: "stripe_js_beta_locales",
        ideal_sepa_beta_1: "ideal_sepa_beta_1",
        sofort_sepa_beta_1: "sofort_sepa_beta_1",
        bancontact_sepa_beta_1: "bancontact_sepa_beta_1",
        upi_beta_1: "upi_beta_1",
      },
      Mo = Object.keys(No),
      Co = function (e, t) {
        return e.indexOf(t) >= 0;
      },
      jo = (function (e) {
        function t() {
          D(this, t);
          var e = B(this, (t.__proto__ || Object.getPrototypeOf(t)).call(this));
          return (e.name = "NetworkError"), (e.type = "network_error"), e;
        }
        return F(t, e), t;
      })(Error),
      Lo = jo,
      xo =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      qo = (function () {
        function e(e, t) {
          var n = [],
            r = !0,
            o = !1,
            i = void 0;
          try {
            for (
              var a, c = e[Symbol.iterator]();
              !(r = (a = c.next()).done) &&
              (n.push(a.value), !t || n.length !== t);
              r = !0
            );
          } catch (e) {
            (o = !0), (i = e);
          } finally {
            try {
              !r && c.return && c.return();
            } finally {
              if (o) throw i;
            }
          }
          return n;
        }
        return function (t, n) {
          if (Array.isArray(t)) return t;
          if (Symbol.iterator in Object(t)) return e(t, n);
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance"
          );
        };
      })(),
      Do = function e(t) {
        return new Le(function (n, r) {
          var o = t.method,
            i = t.url,
            a = t.data,
            c = t.headers,
            s = t.withCredentials,
            u = t.contentType,
            l = void 0 === u ? "application/x-www-form-urlencoded" : u,
            p = "";
          a && "application/x-www-form-urlencoded" === l
            ? (p = cn(a))
            : a && "application/json" === l && (p = JSON.stringify(a));
          var f = "GET" === o && p ? i + "?" + p : i,
            d = "GET" === o ? "" : p,
            _ = new XMLHttpRequest();
          s && (_.withCredentials = s),
            _.open(o, f, !0),
            _.setRequestHeader("Accept", "application/json"),
            _.setRequestHeader("Content-Type", l),
            c &&
              Object.entries(c).forEach(function (e) {
                var t = qo(e, 2),
                  n = t[0],
                  r = t[1];
                "string" == typeof r && _.setRequestHeader(n, r);
              }),
            (_.onreadystatechange = function () {
              4 === _.readyState &&
                ((_.onreadystatechange = function () {}),
                0 === _.status
                  ? s
                    ? r(new Lo())
                    : e(xo({}, t, { withCredentials: !0 })).then(n, r)
                  : n(_));
            });
          try {
            _.send(d);
          } catch (e) {
            r(e);
          }
        });
      },
      Bo = Do,
      Fo =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Uo = function (e, t) {
        var n = /@font-face[ ]?{[^}]*}/g,
          r = e.match(n);
        if (!r) throw new Ie("No @font-face rules found in file from " + t);
        return r;
      },
      Ho = function (e) {
        var t = e.match(/@font-face[ ]?{([^}]*)}/);
        return t ? t[1] : "";
      },
      Go = function (e, t) {
        var n = e.replace(/\/\*.*\*\//g, "").trim(),
          r = n.length && /;$/.test(n) ? n : n + ";",
          o = r.match(/((([^;(]*\([^()]*\)[^;)]*)|[^;]+)+)(?=;)/g);
        if (!o)
          throw new Ie(
            "Found @font-face rule containing no valid font-properties in file from " +
              t
          );
        return o;
      },
      Wo = function (e, t) {
        var n = e.indexOf(":");
        if (-1 === n)
          throw new Ie(
            "Invalid css declaration in file from " + t + ': "' + e + '"'
          );
        var r = e.slice(0, n).trim(),
          o = Zt[r];
        if (!o)
          throw new Ie(
            "Unsupported css property in file from " + t + ': "' + r + '"'
          );
        return { property: o, value: e.slice(n + 1).trim() };
      },
      Yo = function (e, t) {
        var n = e.reduce(function (e, n) {
          var r = Wo(n, t),
            o = r.property,
            i = r.value;
          return Fo({}, e, U({}, o, i));
        }, {});
        return (
          ["family", "src"].forEach(function (e) {
            if (!n[e])
              throw new Ie(
                "Missing css property in file from " + t + ': "' + $t[e] + '"'
              );
          }),
          n
        );
      },
      zo = function (e) {
        return Bo({ url: e, method: "GET" })
          .then(function (e) {
            return e.responseText;
          })
          .then(function (t) {
            return Uo(t, e).map(function (t) {
              var n = Ho(t),
                r = Go(n, e);
              return Yo(r, e);
            });
          });
      },
      Ko = zo,
      Vo = function (e, t) {
        return e.reduce(function (e, n) {
          return e.then(function (e) {
            return "SATISFIED" === e.type
              ? e
              : n().then(function (e) {
                  return t(e)
                    ? { type: "SATISFIED", value: e }
                    : { type: "UNSATISFIED" };
                });
          });
        }, Le.resolve({ type: "UNSATISFIED" }));
      },
      Jo = Vo,
      Xo =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Qo = {
        success: "success",
        fail: "fail",
        invalid_shipping_address: "invalid_shipping_address",
      },
      $o = {
        fail: "fail",
        invalid_payer_name: "invalid_payer_name",
        invalid_payer_email: "invalid_payer_email",
        invalid_payer_phone: "invalid_payer_phone",
        invalid_shipping_address: "invalid_shipping_address",
      },
      Zo = { shipping: "shipping", delivery: "delivery", pickup: "pickup" },
      ei = Xo({ success: "success" }, $o),
      ti = { merchantCapabilities: ["supports3DS"], displayItems: [] },
      ni = Ct({ amount: kt, label: bt, pending: pt(Et) }),
      ri = Ct({ amount: Ot, label: bt, pending: pt(Et) }),
      oi = Ct({
        amount: Ot,
        label: bt,
        pending: pt(Et),
        id: gt(bt, function () {
          return nn("shippingOption");
        }),
        detail: gt(bt, function () {
          return "";
        }),
      }),
      ii = ht.apply(void 0, H(Object.keys(Zo))),
      ai = Ct({ origin: bt, name: bt }),
      ci = Ct({
        displayItems: pt(Tt(ri)),
        shippingOptions: pt(Rt("id")(Tt(oi))),
        total: ni,
        requestShipping: pt(Et),
        requestPayerName: pt(Et),
        requestPayerEmail: pt(Et),
        requestPayerPhone: pt(Et),
        shippingType: pt(ii),
        currency: vt,
        country: yt,
        jcbEnabled: pt(Et),
        __billingDetailsEmailOverride: pt(bt),
        __minApplePayVersion: pt(wt),
        __merchantDetails: pt(ai),
        __skipGooglePayInPaymentRequest: pt(Et),
        __isCheckout: pt(Et),
      }),
      si = Mt({
        currency: pt(vt),
        displayItems: pt(Tt(ri)),
        shippingOptions: pt(Rt("id")(Tt(oi))),
        total: pt(ni),
      }),
      ui = function (e, t) {
        var n = [
          "invalid_payer_name",
          "invalid_payer_email",
          "invalid_payer_phone",
        ];
        return ht.apply(void 0, H(Object.keys(Qo)))(
          -1 !== n.indexOf(e) ? "fail" : e,
          t
        );
      },
      li = Ct({
        displayItems: pt(Tt(ri)),
        shippingOptions: pt(Rt("id")(Tt(oi))),
        total: pt(ni),
        status: ui,
      }),
      pi = ht.apply(void 0, H(Object.keys(ei))),
      fi = function (e) {
        var t = Co(e, No.google_pay_beta_1);
        return Vn
          ? t
            ? ["APPLE_PAY", "GOOGLE_PAY"]
            : ["APPLE_PAY"]
          : t
          ? ["GOOGLE_PAY", "BROWSER"]
          : ["BROWSER"];
      },
      di = fi,
      _i = function () {
        try {
          return window.location.origin === window.top.location.origin;
        } catch (e) {
          return !1;
        }
      },
      hi = 2,
      mi = (function (e) {
        var t = {};
        return function (n) {
          var r = "_" + n;
          if (void 0 !== t[r]) return t[r];
          var o = e(n);
          return (t[r] = o), o;
        };
      })(function (e) {
        return window.ApplePaySession.canMakePaymentsWithActiveCard(e);
      }),
      yi = function (e) {
        if (!window.ApplePaySession) return !1;
        try {
          return window.ApplePaySession.supportsVersion(e);
        } catch (e) {
          return !1;
        }
      },
      vi = function (e, t, n, r) {
        var o =
            arguments.length > 4 && void 0 !== arguments[4] ? arguments[4] : hi,
          i = Math.max(hi, o);
        if (window.ApplePaySession) {
          if (_i()) {
            if (window.ApplePaySession.supportsVersion(i)) {
              var a = t ? [e, t] : [e],
                c = "merchant." + a.join(".") + ".stripe";
              return mi(c).then(function (o) {
                if (
                  (r("pr.apple_pay.can_make_payment_native_response", {
                    available: o,
                  }),
                  n && !o && window.console)
                ) {
                  var i = t ? "or stripeAccount parameter (" + t + ") " : "";
                  window.console.warn(
                    "Either you do not have a card saved to your Wallet or the current domain (" +
                      e +
                      ") " +
                      i +
                      "is not registered for Apple Pay. Visit https://dashboard.stripe.com/account/apple_pay to register this domain."
                  );
                }
                return o;
              });
            }
            return (
              n &&
                window.console &&
                window.console.warn(
                  "This version of Safari does not support ApplePay JS version " +
                    i +
                    "."
                ),
              Le.resolve(!1)
            );
          }
          return Le.resolve(!1);
        }
        return Le.resolve(!1);
      },
      bi = ["mastercard", "visa"],
      gi = [
        "AT",
        "AU",
        "BE",
        "CA",
        "CH",
        "DE",
        "DK",
        "EE",
        "ES",
        "FI",
        "FR",
        "GB",
        "GR",
        "HK",
        "IE",
        "IT",
        "JP",
        "LT",
        "LU",
        "LV",
        "MX",
        "NL",
        "NO",
        "NZ",
        "PL",
        "PT",
        "SE",
        "SG",
        "US",
      ],
      Ei = function (e, t) {
        var n = "US" === e || t ? ["discover", "diners", "jcb"].concat(bi) : bi;
        return -1 !== gi.indexOf(e) ? ["amex"].concat(G(n)) : n;
      },
      wi = function (e, t) {
        return Ei(e, t).reduce(function (e, t) {
          return "mastercard" === t
            ? [].concat(G(e), ["masterCard"])
            : "diners" === t
            ? e
            : [].concat(G(e), [t]);
        }, []);
      },
      Si = {
        bif: 1,
        clp: 1,
        djf: 1,
        gnf: 1,
        jpy: 1,
        kmf: 1,
        krw: 1,
        mga: 1,
        pyg: 1,
        rwf: 1,
        vnd: 1,
        vuv: 1,
        xaf: 1,
        xof: 1,
        xpf: 1,
      },
      Pi = function (e) {
        var t = Si[e.toLowerCase()] || 100;
        return { unitSize: 1 / t, fractionDigits: Math.log(t) / Math.log(10) };
      },
      Oi = function (e, t) {
        var n = Pi(t);
        return (e * n.unitSize).toFixed(n.fractionDigits);
      },
      ki =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Ai = function (e, t) {
        return {
          amount: Oi(e.amount, t.currency),
          label: e.label,
          type: e.pending ? "pending" : "final",
        };
      },
      Ti = function (e, t) {
        return {
          amount: Oi(e.amount, t.currency),
          label: e.label,
          detail: e.detail,
          identifier: e.id,
        };
      },
      Ri = function (e, t) {
        return new window.ApplePayError(e, t);
      },
      Ii = function (e) {
        return function (t) {
          return t[e] && "string" == typeof t[e] ? t[e].toUpperCase() : null;
        };
      },
      Ni =
        ((Oe = {}),
        W(Oe, ei.success, 0),
        W(Oe, ei.fail, 1),
        W(Oe, ei.invalid_payer_name, 2),
        W(Oe, ei.invalid_shipping_address, 3),
        W(Oe, ei.invalid_payer_phone, 4),
        W(Oe, ei.invalid_payer_email, 4),
        Oe),
      Mi =
        ((ke = {}),
        W(ke, ei.success, function () {
          return null;
        }),
        W(ke, ei.fail, function () {
          return null;
        }),
        W(ke, ei.invalid_payer_name, function () {
          return Ri("billingContactInvalid", "name");
        }),
        W(ke, ei.invalid_shipping_address, function () {
          return Ri("shippingContactInvalid", "postalAddress");
        }),
        W(ke, ei.invalid_payer_phone, function () {
          return Ri("shippingContactInvalid", "phoneNumber");
        }),
        W(ke, ei.invalid_payer_email, function () {
          return Ri("shippingContactInvalid", "emailAddress");
        }),
        ke),
      Ci =
        ((Ae = {}),
        W(Ae, Zo.pickup, "storePickup"),
        W(Ae, Zo.shipping, "shipping"),
        W(Ae, Zo.delivery, "delivery"),
        Ae),
      ji = {
        total: function (e) {
          return Ai(e.total, e);
        },
        lineItems: function (e) {
          return e.displayItems
            ? e.displayItems.map(function (t) {
                return Ai(t, e);
              })
            : [];
        },
        shippingMethods: function (e) {
          return e.shippingOptions
            ? e.shippingOptions.map(function (t) {
                return Ti(t, e);
              })
            : [];
        },
      },
      Li = {
        shippingType: function (e) {
          var t = e.shippingType;
          if (!t) return null;
          var n = Ci[t];
          if (void 0 !== n) return n;
          throw new Ie("Invalid value for shippingType: " + t);
        },
        requiredBillingContactFields: function (e) {
          return e.requestPayerName ? ["postalAddress"] : null;
        },
        requiredShippingContactFields: function (e) {
          var t = [];
          return (
            e.requestShipping && t.push("postalAddress"),
            e.requestPayerEmail && t.push("email"),
            e.requestPayerPhone && t.push("phone"),
            t.length ? t : null
          );
        },
        countryCode: Ii("country"),
        currencyCode: Ii("currency"),
        merchantCapabilities: (function (e) {
          return function (t) {
            return t[e] || null;
          };
        })("merchantCapabilities"),
        supportedNetworks: function (e) {
          var t = wi(e.country, e.jcbEnabled || !1);
          return yi(4) && t.push("maestro"), t;
        },
      },
      xi = {
        status: function (e) {
          var t = Ni[e.status];
          return yi(3) && t > 1 ? 1 : t;
        },
        error: function (e) {
          return yi(3) ? Mi[e.status]() : null;
        },
      },
      qi = ki({}, ji, Li),
      Di = ki({}, ji, xi),
      Bi = function (e) {
        var t = ki({}, ti, e);
        return Object.keys(qi).reduce(function (e, n) {
          var r = qi[n],
            o = r(t);
          return null !== o ? ki({}, e, W({}, n, o)) : e;
        }, {});
      },
      Fi = function (e) {
        return Object.keys(Di).reduce(function (t, n) {
          var r = Di[n],
            o = r(e);
          return null !== o ? ki({}, t, W({}, n, o)) : t;
        }, {});
      },
      Ui = function (e) {
        return "string" == typeof e ? e : null;
      },
      Hi = function (e) {
        return e ? Ui(e.phoneNumber) : null;
      },
      Gi = function (e) {
        return e ? Ui(e.emailAddress) : null;
      },
      Wi = function (e) {
        return e
          ? [e.givenName, e.familyName]
              .filter(function (e) {
                return e && "string" == typeof e;
              })
              .join(" ")
          : null;
      },
      Yi = function (e) {
        var t = e.addressLines,
          n = e.countryCode,
          r = e.postalCode,
          o = e.administrativeArea,
          i = e.locality,
          a = e.phoneNumber,
          c = Ui(n);
        return {
          addressLine: Array.isArray(t)
            ? t.reduce(function (e, t) {
                return "string" == typeof t ? [].concat(Y(e), [t]) : e;
              }, [])
            : [],
          country: c ? c.toUpperCase() : "",
          postalCode: Ui(r) || "",
          recipient: Wi(e) || "",
          region: Ui(o) || "",
          city: Ui(i) || "",
          phone: Ui(a) || "",
          sortingCode: "",
          dependentLocality: "",
          organization: "",
        };
      },
      zi = function (e, t) {
        var n = e.identifier,
          r = e.label;
        return t.filter(function (e) {
          return e.id === n && e.label === r;
        })[0];
      },
      Ki = function (e, t) {
        var n = e.shippingContact,
          r = e.shippingMethod,
          o = e.billingContact;
        return {
          shippingOption:
            r && t.shippingOptions && t.shippingOptions.length
              ? zi(r, t.shippingOptions)
              : null,
          shippingAddress: n ? Yi(n) : null,
          payerEmail: Gi(n),
          payerPhone: Hi(n),
          payerName: Wi(o),
          methodName: "apple-pay",
        };
      },
      Vi = Ki,
      Ji =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Xi = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Qi =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      $i = {
        australia: "AU",
        austria: "AT",
        canada: "CA",
        schweiz: "CH",
        deutschland: "DE",
        hongkong: "HK",
        saudiarabia: "SA",
        espaa: "ES",
        singapore: "SG",
        us: "US",
        usa: "US",
        unitedstatesofamerica: "US",
        unitedstates: "US",
        england: "GB",
        gb: "GB",
        uk: "GB",
        unitedkingdom: "GB",
      },
      Zi = function (e, t) {
        return e && "object" === (void 0 === e ? "undefined" : Qi(e))
          ? t(e)
          : null;
      },
      ea = (function () {
        function e(t) {
          var n = this;
          z(this, e),
            (this._onEvent = function () {}),
            (this.setEventHandler = function (e) {
              n._onEvent = e;
            }),
            (this.canMakePayment = function () {
              return vi(
                window.location.hostname,
                n._authentication.accountId,
                $e(n._authentication.apiKey) === Qe.test,
                n._report,
                n._minimumVersion
              );
            }),
            (this.update = function (e) {
              (n._initialPaymentRequest = Wr(n._paymentRequestOptions, e)),
                n._initializeSessionState();
            }),
            (this.show = function () {
              n._initializeSessionState();
              var e = void 0;
              try {
                e = new window.ApplePaySession(
                  n._minimumVersion,
                  Bi(n._paymentRequestOptions)
                );
              } catch (e) {
                throw "Must create a new ApplePaySession from a user gesture handler." ===
                  e.message
                  ? new Ie(
                      "show() must be called from a user gesture handler (such as a click handler, after the user clicks a button)."
                    )
                  : e;
              }
              (n._privateSession = e),
                n._setupSession(e, n._usesButtonElement()),
                e.begin(),
                (n._isShowing = !0);
            }),
            (this.abort = function () {
              n._privateSession && n._privateSession.abort();
            }),
            (this._warn = function (e) {}),
            (this._report = function (e, t) {
              n._controller.report(
                e,
                Ji({}, t, {
                  backingLibrary: "APPLE_PAY",
                  usesButtonElement: n._usesButtonElement(),
                })
              );
            }),
            (this._validateMerchant = function (e, t) {
              return function (r) {
                n._controller.action
                  .createApplePaySession({
                    data: {
                      validation_url: r.validationURL,
                      domain_name: window.location.hostname,
                      display_name: n._paymentRequestOptions.total.label,
                    },
                    usesButtonElement: t,
                  })
                  .then(function (t) {
                    if (n._isShowing)
                      switch (t.type) {
                        case "object":
                          e.completeMerchantValidation(
                            JSON.parse(t.object.session)
                          );
                          break;
                        case "error":
                          n._handleValidationError(e)(t.error);
                          break;
                        default:
                          Ne(t);
                      }
                  }, n._handleValidationError(e));
              };
            }),
            (this._handleValidationError = function (e) {
              return function (t) {
                n._report("error.pr.apple_pay.session_creation_failed", {
                  error: t,
                }),
                  e.abort();
                var r = t.message;
                "string" == typeof r && n._controller.warn(r);
              };
            }),
            (this._paymentAuthorized = function (e) {
              return function (t) {
                var r = t.payment,
                  o = n._usesButtonElement() ? Wt.paymentRequestButton : null;
                n._controller.action
                  .tokenizeWithData({
                    type: "apple_pay",
                    elementName: o,
                    tokenData: Ji({}, r, {
                      billingContact: Zi(r.billingContact, n._normalizeContact),
                    }),
                    mids: n._mids,
                  })
                  .then(function (t) {
                    if ("error" === t.type)
                      e.completePayment(window.ApplePaySession.STATUS_FAILURE),
                        n._report("error.pr.create_token_failed", {
                          error: t.error,
                        });
                    else {
                      var o = Zi(r.shippingContact, n._normalizeContact),
                        i = Zi(r.billingContact, n._normalizeContact);
                      o &&
                        n._paymentRequestOptions.requestShipping &&
                        !o.countryCode &&
                        e.completePayment(
                          window.ApplePaySession
                            .STATUS_INVALID_SHIPPING_POSTAL_ADDRESS
                        );
                      var a = Vi(
                        { shippingContact: o, billingContact: i },
                        n._paymentRequestOptions
                      );
                      n._onToken(e)(
                        Ji({}, a, {
                          shippingOption: n._privateShippingOption,
                          token: t.object,
                        })
                      );
                    }
                  });
              };
            }),
            (this._normalizeContact = function (e) {
              if (e.country && "string" == typeof e.country) {
                var t = e.country.toLowerCase().replace(/[^a-z]+/g, ""),
                  r = void 0;
                return (
                  e.countryCode
                    ? "string" == typeof e.countryCode &&
                      (r = e.countryCode.toUpperCase())
                    : (r = $i[t]) ||
                      n._report("warn.pr.apple_pay.missing_country_code", {
                        country: e.country,
                      }),
                  Ji({}, e, { countryCode: r })
                );
              }
              return e;
            }),
            (this._onToken = function (e) {
              return function (t) {
                n._onEvent({
                  type: "paymentresponse",
                  payload: Ji({}, t, { complete: n._completePayment(e) }),
                });
              };
            }),
            (this._completePayment = function (e) {
              return function (t) {
                n._paymentRequestOptions = Wr(n._paymentRequestOptions, {
                  status: t,
                });
                var r = Fi(n._paymentRequestOptions),
                  o = r.status,
                  i = r.error;
                i
                  ? e.completePayment({ status: o, errors: [i] })
                  : e.completePayment(o),
                  (0 === o || (1 === o && null == i)) &&
                    ((n._isShowing = !1),
                    n._onEvent && n._onEvent({ type: "close" }));
              };
            }),
            (this._shippingContactSelected = function (e) {
              return function (t) {
                n._onEvent({
                  type: "shippingaddresschange",
                  payload: {
                    shippingAddress: Yi(n._normalizeContact(t.shippingContact)),
                    updateWith: n._completeShippingContactSelection(e),
                  },
                });
              };
            }),
            (this._completeShippingContactSelection = function (e) {
              return function (t) {
                (n._paymentRequestOptions = Wr(n._paymentRequestOptions, t)),
                  n._paymentRequestOptions.shippingOptions &&
                    n._paymentRequestOptions.shippingOptions.length &&
                    (n._privateShippingOption =
                      n._paymentRequestOptions.shippingOptions[0]);
                var r = Fi(n._paymentRequestOptions),
                  o = r.status,
                  i = r.shippingMethods,
                  a = r.total,
                  c = r.lineItems;
                e.completeShippingContactSelection(o, i, a, c);
              };
            }),
            (this._shippingMethodSelected = function (e) {
              return function (t) {
                if (n._paymentRequestOptions.shippingOptions) {
                  var r = zi(
                    t.shippingMethod,
                    n._paymentRequestOptions.shippingOptions
                  );
                  (n._privateShippingOption = r),
                    n._onEvent({
                      type: "shippingoptionchange",
                      payload: {
                        shippingOption: r,
                        updateWith: n._completeShippingMethodSelection(e),
                      },
                    });
                }
              };
            }),
            (this._completeShippingMethodSelection = function (e) {
              return function (t) {
                n._paymentRequestOptions = Wr(n._paymentRequestOptions, t);
                var r = Fi(n._paymentRequestOptions),
                  o = r.status,
                  i = r.total,
                  a = r.lineItems;
                e.completeShippingMethodSelection(o, i, a);
              };
            });
          var r = t.controller,
            o = t.authentication,
            i = t.mids,
            a = t.options,
            c = t.usesButtonElement,
            s = t.listenerRegistry;
          (this._controller = r),
            (this._authentication = o),
            (this._mids = i),
            (this._minimumVersion = a.__minApplePayVersion || hi),
            (this._usesButtonElement = c),
            (this._listenerRegistry = s),
            (this._initialPaymentRequest = a),
            (this._isShowing = !1),
            this._initializeSessionState();
        }
        return (
          Xi(e, [
            {
              key: "_initializeSessionState",
              value: function () {
                (this._paymentRequestOptions = Ji(
                  {},
                  ti,
                  this._initialPaymentRequest,
                  { status: ei.success }
                )),
                  (this._privateSession = null),
                  (this._privateShippingOption = null);
                var e = this._paymentRequestOptions.shippingOptions;
                e && e.length && (this._privateShippingOption = e[0]);
              },
            },
            {
              key: "_setupSession",
              value: function (e, t) {
                var n = this;
                this._listenerRegistry.addEventListener(
                  e,
                  "validatemerchant",
                  wn(this._validateMerchant(e, t))
                ),
                  this._listenerRegistry.addEventListener(
                    e,
                    "paymentauthorized",
                    wn(this._paymentAuthorized(e))
                  ),
                  this._listenerRegistry.addEventListener(
                    e,
                    "cancel",
                    wn(function () {
                      (n._isShowing = !1),
                        n._onEvent({ type: "cancel" }),
                        n._onEvent({ type: "close" });
                    })
                  ),
                  this._listenerRegistry.addEventListener(
                    e,
                    "shippingcontactselected",
                    wn(this._shippingContactSelected(e))
                  ),
                  this._listenerRegistry.addEventListener(
                    e,
                    "shippingmethodselected",
                    wn(this._shippingMethodSelected(e))
                  );
              },
            },
          ]),
          e
        );
      })(),
      ta = ea,
      na = null,
      ra = function (e) {
        return null !== na
          ? Le.resolve(na)
          : e().then(function (e) {
              return (na = e);
            });
      },
      oa = ra,
      ia = function () {
        return !(!Xn && !Qn);
      },
      aa = ia,
      ca =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      sa = function e(t) {
        var n = this;
        K(this, e),
          (this._mids = null),
          (this._frame = null),
          (this._initFrame = function (e) {
            var t = n._controller.createHiddenFrame(
              Dt.PAYMENT_REQUEST_GOOGLE_PAY,
              { authentication: n._authentication, mids: n._mids }
            );
            t.send({ action: "stripe-pr-initialize", payload: { data: e } }),
              n._initFrameEventHandlers(t),
              (n._frame = t);
          }),
          (this._initFrameEventHandlers = function (e) {
            e._on("pr-cancel", function () {
              n._onEvent({ type: "cancel" });
            }),
              e._on("pr-close", function () {
                n._backdrop.fadeOut().then(function () {
                  n._backdrop.unmount();
                }),
                  n._onEvent({ type: "close" });
              }),
              e._on("pr-error", function (e) {
                n._onEvent({
                  type: "error",
                  payload: {
                    errorMessage: e.errorMessage,
                    errorCode: e.errorCode,
                  },
                });
              }),
              e._on("pr-callback", function (t) {
                var r = t.event,
                  o = t.options,
                  i = t.nonce;
                switch (r) {
                  case "paymentresponse":
                    n._handlePaymentResponse(e, o, i);
                    break;
                  case "shippingaddresschange":
                    n._handleShippingAddressChange(e, o, i);
                    break;
                  case "shippingoptionchange":
                    n._handleShippingOptionChange(e, o, i);
                    break;
                  default:
                    throw new Error("Unexpected event name: " + r);
                }
              });
          }),
          (this._handlePaymentResponse = function (e, t, r) {
            var o = function (t) {
              e.send({
                action: "stripe-pr-callback-complete",
                payload: { nonce: r, data: { status: t } },
              });
            };
            n._onEvent({
              type: "paymentresponse",
              payload: ca({}, t, { complete: o }),
            });
          }),
          (this._handleShippingAddressChange = function (e, t, r) {
            var o = function (t) {
              e.send({
                action: "stripe-pr-callback-complete",
                payload: { nonce: r, data: t },
              });
            };
            n._onEvent({
              type: "shippingaddresschange",
              payload: ca({}, t, { updateWith: o }),
            });
          }),
          (this._handleShippingOptionChange = function (e, t, r) {
            var o = function (t) {
              e.send({
                action: "stripe-pr-callback-complete",
                payload: { nonce: r, data: t },
              });
            };
            n._onEvent({
              type: "shippingoptionchange",
              payload: ca({}, t, { updateWith: o }),
            });
          }),
          (this.setEventHandler = function (e) {
            n._onEvent = e;
          }),
          (this.canMakePayment = function () {
            if (!aa()) return Le.resolve(!1);
            if (!n._frame) throw new Error("Frame not initialized.");
            var e = n._frame;
            return oa(function () {
              return e.action.checkCanMakePayment().then(function (e) {
                return !0 === e.available;
              });
            });
          }),
          (this.show = function () {
            n._frame &&
              (n._frame.send({
                action: "stripe-pr-show",
                payload: {
                  data: { usesButtonElement: n._usesButtonElement() },
                },
              }),
              n._backdrop.mount(),
              n._backdrop.show(),
              n._backdrop.fadeIn());
          }),
          (this.update = function (e) {
            n._frame &&
              n._frame.send({
                action: "stripe-pr-update",
                payload: { data: e },
              });
          }),
          (this.abort = function () {
            n._frame &&
              n._frame.send({ action: "stripe-pr-abort", payload: {} });
          }),
          (this._controller = t.controller),
          (this._authentication = t.authentication),
          (this._mids = t.mids),
          (this._usesButtonElement = t.usesButtonElement),
          (this._backdrop = new _r({
            lockScrolling: !1,
            lockFocus: !0,
            lockFocusOn: null,
            listenerRegistry: t.listenerRegistry,
          })),
          aa() &&
            this._controller &&
            (this._controller.action.fetchLocale({ locale: "auto" }),
            this._initFrame(t.options));
      },
      ua = sa,
      la = (function () {
        if (!window.PaymentRequest) return null;
        if (/CriOS\/59/.test(navigator.userAgent)) return null;
        if (/.*\(.*; wv\).*Chrome\/(?:53|54)\.\d.*/g.test(navigator.userAgent))
          return null;
        if (Jn) return null;
        var e = window.PaymentRequest;
        return (
          e.prototype.canMakePayment ||
            (e.prototype.canMakePayment = function () {
              return Le.resolve(!1);
            }),
          e
        );
      })(),
      pa = null,
      fa = function (e, t) {
        return null !== pa
          ? Le.resolve(pa)
          : la && e
          ? e.action.checkCanMakePayment().then(function (e) {
              var t = e.available;
              return (pa = !0 === t);
            })
          : Le.resolve(!1);
      },
      da =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      _a = function e(t) {
        V(this, e), ha.call(this);
        var n = t.authentication,
          r = t.controller,
          o = t.mids,
          i = t.usesButtonElement,
          a = t.options;
        if (
          ((this._authentication = n),
          (this._controller = r),
          (this._mids = o),
          (this._usesButtonElement = i),
          la && "https:" === window.location.protocol)
        ) {
          this._controller.action.fetchLocale({ locale: "auto" });
          var c = this._controller.createHiddenFrame(
            Dt.PAYMENT_REQUEST_BROWSER,
            { authentication: n, mids: this._mids }
          );
          this._setupPrFrame(c, a), (this._prFrame = c);
        } else this._prFrame = null;
      },
      ha = function () {
        var e = this;
        (this._onEvent = function () {}),
          (this.setEventHandler = function (t) {
            e._onEvent = t;
          }),
          (this.canMakePayment = function () {
            return fa(e._prFrame, ($e(e._authentication.apiKey), Qe.test));
          }),
          (this.update = function (t) {
            var n = e._prFrame;
            n && n.send({ action: "stripe-pr-update", payload: { data: t } });
          }),
          (this.show = function () {
            if (!e._prFrame)
              throw new Ie("Payment Request is not available in this browser.");
            e._prFrame.send({
              action: "stripe-pr-show",
              payload: { data: { usesButtonElement: e._usesButtonElement() } },
            });
          }),
          (this.abort = function () {
            e._prFrame &&
              e._prFrame.send({ action: "stripe-pr-abort", payload: {} });
          }),
          (this._setupPrFrame = function (t, n) {
            t.send({ action: "stripe-pr-initialize", payload: { data: n } }),
              t._on("pr-cancel", function () {
                e._onEvent({ type: "cancel" });
              }),
              t._on("pr-close", function () {
                e._onEvent({ type: "close" });
              }),
              t._on("pr-error", function (t) {
                e._onEvent({
                  type: "error",
                  payload: {
                    errorMessage: t.message || "",
                    errorCode: t.code || "",
                  },
                });
              }),
              t._on("pr-callback", function (n) {
                var r = n.event,
                  o = n.nonce,
                  i = n.options;
                switch (r) {
                  case "token":
                    e._onEvent({
                      type: "paymentresponse",
                      payload: da({}, i, {
                        complete: function (e) {
                          t.send({
                            action: "stripe-pr-callback-complete",
                            payload: { data: { status: e }, nonce: o },
                          });
                        },
                      }),
                    });
                    break;
                  case "shippingaddresschange":
                    e._onEvent({
                      type: "shippingaddresschange",
                      payload: {
                        shippingAddress: i.shippingAddress,
                        updateWith: function (e) {
                          t.send({
                            action: "stripe-pr-callback-complete",
                            payload: { nonce: o, data: e },
                          });
                        },
                      },
                    });
                    break;
                  case "shippingoptionchange":
                    e._onEvent({
                      type: "shippingoptionchange",
                      payload: {
                        shippingOption: i.shippingOption,
                        updateWith: function (e) {
                          t.send({
                            action: "stripe-pr-callback-complete",
                            payload: { nonce: o, data: e },
                          });
                        },
                      },
                    });
                    break;
                  default:
                    throw new Error(
                      "Unexpected event from PaymentRequest inner: " + r
                    );
                }
              });
          });
      },
      ma = _a,
      ya =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      va = (function (e) {
        function t(e) {
          Q(this, t);
          var n = $(this, (t.__proto__ || Object.getPrototypeOf(t)).call(this));
          ba.call(n),
            (n._controller = e.controller),
            (n._authentication = e.authentication),
            (n._mids = e.mids),
            (n._listenerRegistry = e.listenerRegistry),
            n._report("pr.options", { options: e.rawOptions });
          var r = xt(ci, e.rawOptions || {}, "paymentRequest()"),
            o = r.value;
          if (
            (r.warnings.forEach(function (e) {
              return n._warn(e);
            }),
            o.__billingDetailsEmailOverride && o.requestPayerEmail)
          )
            throw new Ie(
              "When providing `__billingDetailsEmailOverride`, `requestPayerEmail` has to be `false` so that the customer is not prompted for their email in the payment sheet."
            );
          return (
            (n._queryStrategy = e.queryStrategyOverride || di(e.betas)),
            n._report("pr.query_strategy", { queryStrategy: n._queryStrategy }),
            (n._initialOptions = ya({}, o, {
              __skipGooglePayInPaymentRequest:
                -1 !== n._queryStrategy.indexOf("GOOGLE_PAY"),
            })),
            n._initBackingLibraries(n._initialOptions),
            n
          );
        }
        return Z(t, e), t;
      })(An),
      ba = function () {
        var e = this;
        (this._usedByButtonElement = null),
          (this._showCalledByButtonElement = !1),
          (this._isShowing = !1),
          (this._backingLibraries = {
            APPLE_PAY: null,
            GOOGLE_PAY: null,
            BROWSER: null,
          }),
          (this._activeBackingLibraryName = null),
          (this._activeBackingLibrary = null),
          (this._canMakePaymentAvailability = {
            APPLE_PAY: null,
            GOOGLE_PAY: null,
            BROWSER: null,
          }),
          (this._canMakePaymentResolved = !1),
          (this._validateUserOn = function (t, n) {
            "string" == typeof t &&
              (("source" === t && e._hasRegisteredListener("paymentmethod")) ||
                ("paymentmethod" === t &&
                  e._hasRegisteredListener("source"))) &&
              (e._report("pr.double_callback_registration"),
              e._controller.warn(
                "Do not register event listeners for both `source` or `paymentmethod`. Only one of them will succeed."
              ));
          }),
          (this._report = function (t, n) {
            e._controller.report(
              t,
              ya({}, n, {
                activeBackingLibrary: e._activeBackingLibraryName,
                usesButtonElement: e._usedByButtonElement || !1,
              })
            );
          }),
          (this._warn = function (t) {
            e._controller.warn(t);
          }),
          (this._registerElement = function () {
            e._usedByButtonElement = !0;
          }),
          (this._elementShow = function () {
            (e._showCalledByButtonElement = !0), e.show();
          }),
          (this._initBackingLibraries = function (t) {
            e._queryStrategy.forEach(function (n) {
              var r = {
                controller: e._controller,
                authentication: e._authentication,
                mids: e._mids,
                options: t,
                usesButtonElement: function () {
                  return !0 === e._usedByButtonElement;
                },
                listenerRegistry: e._listenerRegistry,
              };
              switch (n) {
                case "APPLE_PAY":
                  (e._backingLibraries.APPLE_PAY = new ta(r)),
                    e._backingLibraries.APPLE_PAY.setEventHandler(
                      e._handleInternalEvent
                    );
                  break;
                case "GOOGLE_PAY":
                  (e._backingLibraries.GOOGLE_PAY = new ua(r)),
                    e._backingLibraries.GOOGLE_PAY.setEventHandler(
                      e._handleInternalEvent
                    );
                  break;
                case "BROWSER":
                  (e._backingLibraries.BROWSER = new ma(r)),
                    e._backingLibraries.BROWSER.setEventHandler(
                      e._handleInternalEvent
                    );
                  break;
                default:
                  Ne(n);
              }
            });
          }),
          (this._handleInternalEvent = function (t) {
            switch (t.type) {
              case "paymentresponse":
                e._emitPaymentResponse(t.payload);
                break;
              case "error":
                e._report("error.pr.internal_error", { error: t.payload });
                break;
              case "close":
                e._isShowing = !1;
                break;
              default:
                e._emitExternalEvent(t);
            }
          }),
          (this._emitExternalEvent = function (t) {
            switch (t.type) {
              case "cancel":
                e._emit("cancel");
                break;
              case "shippingoptionchange":
              case "shippingaddresschange":
                var n = t.type,
                  r = t.payload,
                  o = null,
                  i = !1,
                  a = !1,
                  c = function (c) {
                    if (a && i)
                      return (
                        e._report("pr.update_with_called_after_timeout", {
                          event: n,
                        }),
                        void e._controller.warn(
                          "Call to updateWith() was ignored because it has already timed out. Please ensure that updateWith is called within 30 seconds."
                        )
                      );
                    if (i)
                      return (
                        e._report("pr.update_with_double_call", { event: n }),
                        void e._controller.warn(
                          "Call to updateWith() was ignored because it has already been called. Do not call updateWith more than once."
                        )
                      );
                    o && clearTimeout(o),
                      (i = !0),
                      e._report("pr.update_with", { event: n, updates: c });
                    var s = xt(li, c || {}, n + " callback"),
                      u = s.value;
                    s.warnings.forEach(function (t) {
                      return e._controller.warn(t);
                    });
                    var l = u,
                      p = !1;
                    if (
                      e._initialOptions.__isCheckout &&
                      "APPLE_PAY" === e._activeBackingLibraryName &&
                      u.shippingOptions &&
                      1 === u.shippingOptions.length &&
                      0 === u.shippingOptions[0].amount
                    ) {
                      u.shippingOptions;
                      (l = X(u, ["shippingOptions"])), (p = !0);
                    }
                    var f =
                      u.shippingOptions || e._initialOptions.shippingOptions;
                    if (
                      !(
                        p ||
                        "shippingaddresschange" !== t.type ||
                        u.status !== ei.success ||
                        (f && f.length)
                      )
                    )
                      throw new Ie(
                        "When requesting shipping information, you must specify shippingOptions once a shipping address is selected.\nEither provide shippingOptions in stripe.paymentRequest(...) or listen for the shippingaddresschange event and provide shippingOptions to the updateWith callback there."
                      );
                    r.updateWith(l);
                  };
                e._hasRegisteredListener(t.type)
                  ? ((o = setTimeout(function () {
                      (a = !0),
                        e._report("pr.update_with_timed_out", { event: n }),
                        e._controller.warn(
                          'Timed out waiting for a call to updateWith(). If you listen to "' +
                            t.type +
                            '" events, then you must call event.updateWith in the "' +
                            t.type +
                            '" handler within 30 seconds.'
                        ),
                        c({ status: "fail" });
                    }, 29900)),
                    e._emit(n, ya({}, r, { updateWith: c })))
                  : c({ status: "success" });
                break;
              case "token":
              case "source":
              case "paymentmethod":
                var s = t.type,
                  u = t.payload,
                  l = null,
                  p = !1,
                  f = !1,
                  d = function (t) {
                    if (p && f)
                      return (
                        e._report("pr.complete_called_after_timeout"),
                        void e._controller.warn(
                          "Call to complete() was ignored because it has already timed out. Please ensure that complete is called within 30 seconds."
                        )
                      );
                    if (f)
                      return (
                        e._report("pr.complete_double_call"),
                        void e._controller.warn(
                          "Call to complete() was ignored because it has already been called. Do not call complete more than once."
                        )
                      );
                    l && clearTimeout(l), (f = !0);
                    var n = xt(pi, t, "status for PaymentRequest completion"),
                      r = n.value;
                    n.warnings.forEach(function (t) {
                      return e._controller.warn(t);
                    }),
                      u.complete(r);
                  };
                (l = setTimeout(function () {
                  (p = !0),
                    e._report("pr.complete_timed_out"),
                    e._controller.warn(
                      'Timed out waiting for a call to complete(). Once you have processed the payment in the "' +
                        t.type +
                        '" handler, you must call event.complete within 30 seconds.'
                    ),
                    d("fail");
                }, 29900)),
                  e._emit(s, ya({}, u, { complete: d }));
                break;
              default:
                Ne(t);
            }
          }),
          (this._maybeEmitPaymentResponse = function (t) {
            e._isShowing && e._emitExternalEvent(t);
          }),
          (this._emitPaymentResponse = function (t) {
            e._report("pr.payment_authorized");
            var n = t.token,
              r = X(t, ["token"]),
              o = r.payerEmail,
              i = r.payerPhone,
              a = r.complete,
              c = e._showCalledByButtonElement ? Wt.paymentRequestButton : null;
            e._hasRegisteredListener("token") &&
              e._maybeEmitPaymentResponse({ type: "token", payload: t }),
              e._hasRegisteredListener("source") &&
                e._controller.action
                  .createSourceWithData({
                    elementName: c,
                    type: "card",
                    sourceData: {
                      token: n.id,
                      owner: {
                        email:
                          e._initialOptions.__billingDetailsEmailOverride || o,
                        phone: i,
                      },
                    },
                    mids: null,
                  })
                  .then(function (t) {
                    "error" === t.type
                      ? t.error.code && "email_invalid" === t.error.code
                        ? a("invalid_payer_email")
                        : (e._report("fatal.pr.token_to_source_failed", {
                            error: t.error,
                            token: n.id,
                          }),
                          a("fail"))
                      : e._maybeEmitPaymentResponse({
                          type: "source",
                          payload: ya({}, r, { source: t.object }),
                        });
                  }),
              e._hasRegisteredListener("paymentmethod") &&
                e._controller.action
                  .createPaymentMethodWithData({
                    elementName: c,
                    type: "card",
                    paymentMethodData: {
                      card: { token: n.id },
                      billing_details: {
                        email:
                          e._initialOptions.__billingDetailsEmailOverride || o,
                        phone: i,
                      },
                    },
                    mids: null,
                  })
                  .then(function (t) {
                    "error" === t.type
                      ? t.error.code && "email_invalid" === t.error.code
                        ? a("invalid_payer_email")
                        : (e._report(
                            "fatal.pr.token_to_payment_method_failed",
                            { error: t.error, token: n.id }
                          ),
                          a("fail"))
                      : e._maybeEmitPaymentResponse({
                          type: "paymentmethod",
                          payload: ya({}, r, { paymentMethod: t.object }),
                        });
                  });
          }),
          (this._canMakePaymentForBackingLibrary = function (t) {
            var n = e._backingLibraries[t];
            if (!n)
              throw new Error(
                "Unexpectedly calling canMakePayment on uninitialized backing library."
              );
            return Le.race([
              new Le(function (e) {
                return setTimeout(e, 1e4);
              }).then(function () {
                return !1;
              }),
              n.canMakePayment().then(function (e) {
                return !!e;
              }),
            ]).then(function (n) {
              return (
                (e._canMakePaymentAvailability = ya(
                  {},
                  e._canMakePaymentAvailability,
                  J({}, t, n)
                )),
                { backingLibraryName: t, available: n }
              );
            });
          }),
          (this._constructCanMakePaymentResponse = function () {
            return ya(
              { applePay: !!e._canMakePaymentAvailability.APPLE_PAY },
              -1 !== e._queryStrategy.indexOf("GOOGLE_PAY")
                ? { googlePay: !!e._canMakePaymentAvailability.GOOGLE_PAY }
                : {}
            );
          }),
          (this.canMakePayment = wn(function () {
            if ((e._report("pr.can_make_payment"), e._canMakePaymentResolved)) {
              var t =
                null !== e._activeBackingLibrary
                  ? e._constructCanMakePaymentResponse()
                  : null;
              return (
                e._report("pr.can_make_payment_response", {
                  response: t,
                  cached: !0,
                }),
                Le.resolve(t)
              );
            }
            if ("https:" !== window.location.protocol)
              return (
                e._controller.warn(
                  "If you are testing the PaymentRequest button (to accept Apple Pay, Google Pay, etc.) you must serve this page over HTTPS as it will not work over HTTP. Please read https://stripe.com/docs/stripe-js/elements/payment-request-button#html-js-prerequisites for more details."
                ),
                (e._canMakePaymentResolved = !0),
                Le.resolve(null)
              );
            var n = e._queryStrategy.map(function (t) {
                return function () {
                  return e._canMakePaymentForBackingLibrary(t);
                };
              }),
              r = new Fe();
            return Jo(n, function (t) {
              var n = t.backingLibraryName,
                r = t.available;
              return (
                r &&
                  ((e._activeBackingLibraryName = n),
                  (e._activeBackingLibrary = e._backingLibraries[n])),
                r
              );
            }).then(function (t) {
              var n = new Fe();
              e._canMakePaymentResolved = !0;
              var o = null;
              return (
                "SATISFIED" === t.type &&
                  (o = e._constructCanMakePaymentResponse()),
                e._report("pr.can_make_payment_response", {
                  response: o,
                  cached: !1,
                  duration: r.getElapsedTime(n),
                }),
                o
              );
            });
          })),
          (this.update = wn(function (t) {
            if (e._isShowing)
              throw (
                (e._report("pr.update_called_while_showing"),
                new Ie(
                  "You cannot update Payment Request options while the payment sheet is showing."
                ))
              );
            e._report("pr.update", { updates: t });
            var n = xt(si, t, "PaymentRequest update()"),
              r = n.value;
            n.warnings.forEach(function (t) {
              return e._warn(t);
            }),
              e._activeBackingLibrary && e._activeBackingLibrary.update(r);
          })),
          (this.show = wn(function () {
            if (
              (e._usedByButtonElement &&
                !e._showCalledByButtonElement &&
                (e._report("pr.show_called_with_button"),
                e._warn(
                  "Do not call show() yourself if you are using the paymentRequestButton Element. The Element handles showing the payment sheet."
                )),
              !e._canMakePaymentResolved)
            )
              throw (
                (e._report("pr.show_called_before_can_make_payment"),
                new Ie(
                  "You must first check the Payment Request API's availability using paymentRequest.canMakePayment() before calling show()."
                ))
              );
            if (!e._activeBackingLibrary)
              throw (
                (e._report("pr.show_called_with_can_make_payment_false"),
                new Ie("Payment Request is not available in this browser."))
              );
            var t = e._activeBackingLibrary;
            e._report("pr.show", {
              listeners: Object.keys(e._callbacks).sort(),
            }),
              (e._isShowing = !0),
              t.show();
          })),
          (this.abort = wn(function () {
            if (e._activeBackingLibrary) {
              var t = e._activeBackingLibrary;
              e._report("pr.abort"), t.abort();
            }
          })),
          (this.isShowing = function () {
            return e._isShowing;
          });
      },
      ga = va,
      Ea = {
        base: pt(At),
        complete: pt(At),
        empty: pt(At),
        invalid: pt(At),
        paymentRequestButton: pt(At),
      },
      wa = {
        classes: pt(
          Ct({
            base: pt(bt),
            complete: pt(bt),
            empty: pt(bt),
            focus: pt(bt),
            invalid: pt(bt),
            webkitAutofill: pt(bt),
          })
        ),
        hidePostalCode: pt(Et),
        hideIcon: pt(Et),
        showIcon: pt(Et),
        style: pt(Ct(Ea)),
        iconStyle: pt(ht("solid", "default")),
        value: pt(ft(bt, At)),
        __privateCvcOptional: pt(Et),
        __privateValue: pt(ft(bt, At)),
        __privateEmitIbanValue: pt(Et),
        error: pt(
          Ct({ type: bt, code: pt(bt), decline_code: pt(bt), param: pt(bt) })
        ),
        locale: It("elements()"),
        fonts: It("elements()"),
        placeholder: pt(bt),
        disabled: pt(Et),
        placeholderCountry: pt(bt),
        paymentRequest: pt(
          (function (e, t) {
            return function (n, r) {
              return n instanceof e ? ct(n) : lt("a " + t + " instance", n, r);
            };
          })(ga, "stripe.paymentRequest(...)")
        ),
        supportedCountries: pt(Tt(bt)),
        accountHolderType: pt(ht("individual", "company")),
      },
      Sa = Ct(wa),
      Pa = ["hu", "mt", "tr", "th"],
      Oa = (function (e) {
        return function (t, n) {
          return Co(n, No.stripe_js_beta_locales)
            ? t
            : -1 === e.indexOf(t)
            ? t
            : "auto";
        };
      })(Pa),
      ka =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      Aa = function (e) {
        return "string" == typeof e
          ? He(Object.keys(lo), function (t) {
              return t === e;
            }) || null
          : null;
      },
      Ta = function (e) {
        return null != e &&
          e.__elementType &&
          "string" == typeof e.__elementType &&
          "function" == typeof e
          ? e.__elementType
          : null;
      },
      Ra = function (e, t) {
        var n = Aa(e);
        if (!n)
          throw new Ie(
            "A valid Element name must be provided. Valid Elements are:\n" +
              Object.keys(lo)
                .filter(function (e) {
                  return !lo[e].beta;
                })
                .join(", ") +
              "; you passed: " +
              (n || (void 0 === e ? "undefined" : ka(e))) +
              "."
          );
      },
      Ia = function (e, t, n) {
        if ((Ra(e), lo[e].unique && -1 !== t.indexOf(e)))
          throw new Ie("Can only create one Element of type " + e + ".");
        var r = lo[e].conflict,
          o = Ye(t, r);
        if (o.length) {
          var i = o[0];
          throw new Ie(
            "Cannot create an Element of type " +
              e +
              " after an Element of type " +
              i +
              " has already been created."
          );
        }
      },
      Na = "14px",
      Ma = function (e) {
        var t = e.split(" ").map(function (e) {
          return parseInt(e.trim(), 10);
        });
        return 1 === t.length || 2 === t.length
          ? 2 * t[0]
          : 3 === t.length || 4 === t.length
          ? t[0] + t[2]
          : 0;
      },
      Ca = function () {
        var e =
            arguments.length > 0 && void 0 !== arguments[0]
              ? arguments[0]
              : "1.2em",
          t =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : Na,
          n =
            arguments.length > 2 && void 0 !== arguments[2]
              ? arguments[2]
              : "0",
          r = Ma(n);
        if ("string" == typeof e && /^[0-9.]+px$/.test(e)) {
          return parseFloat(e.toString().replace(/[^0-9.]/g, "")) + r + "px";
        }
        var o = parseFloat(e.toString().replace(/[^0-9.]/g, "")),
          i = parseFloat(Na.replace(/[^0-9.]/g, "")),
          a = parseFloat(t.toString().replace(/[^0-9.]/g, "")),
          c = void 0;
        if ("string" == typeof t && /^(\d+|\d*\.\d+)px$/.test(t)) c = a;
        else if ("string" == typeof t && /^(\d+|\d*\.\d+)em$/.test(t))
          c = a * i;
        else if ("string" == typeof t && /^(\d+|\d*\.\d+)%$/.test(t))
          c = (a / 100) * i;
        else {
          if (
            "string" != typeof t ||
            (!/^[\d.]+$/.test(t) && !/^\d*\.(px|em|%)$/.test(t))
          )
            return "100%";
          c = i;
        }
        var s = o * c + r,
          u = s + "px";
        return /^[0-9.]+px$/.test(u) ? u : "100%";
      },
      ja = Ca,
      La =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      xa = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      qa = {
        base: "StripeElement",
        focus: "StripeElement--focus",
        invalid: "StripeElement--invalid",
        complete: "StripeElement--complete",
        empty: "StripeElement--empty",
        webkitAutofill: "StripeElement--webkit-autofill",
      },
      Da = {
        margin: "0",
        padding: "0",
        border: "none",
        display: "block",
        background: "transparent",
        position: "relative",
        opacity: "1",
      },
      Ba = {
        border: "none",
        display: "block",
        position: "absolute",
        height: "1px",
        top: "0",
        left: "0",
        padding: "0",
        margin: "0",
        width: "100%",
        opacity: "0",
        background: "transparent",
        "pointer-events": "none",
        "font-size": "16px",
      },
      Fa = function (e) {
        return parseFloat(e.toFixed(1));
      },
      Ua = function (e) {
        return /^\d+(\.\d*)?px$/.test(e);
      },
      Ha = (function (e) {
        function t(e, n) {
          ne(this, t);
          var r = re(
            this,
            (t.__proto__ || Object.getPrototypeOf(t)).call(this)
          );
          Ga.call(r);
          var o = e.controller,
            i = e.componentName,
            a = e.paymentRequest;
          (r._controller = o),
            (r._listenerRegistry = n),
            (r._componentName = i);
          var c = "paymentRequestButton" === r._componentName;
          if (c) {
            if (!a)
              throw new Ie(
                "You must pass in a stripe.paymentRequest object in order to use this Element."
              );
            (r._paymentRequest = a), r._paymentRequest._registerElement();
          }
          return (
            r._createComponent(e, i),
            (r._classes = qa),
            r._computeCustomClasses(e.classes || {}),
            (r._lastBackgroundColor = ""),
            (r._destroyed = !1),
            (r._focused = !1),
            (r._empty = !c),
            (r._invalid = !1),
            (r._complete = !1),
            (r._autofilled = !1),
            (r._lastSubmittedAt = null),
            r
          );
        }
        return (
          oe(t, e),
          xa(t, [
            {
              key: "_checkDestroyed",
              value: function () {
                if (this._destroyed)
                  throw new Ie(
                    "This Element has already been destroyed. Please create a new one."
                  );
              },
            },
            {
              key: "_isMounted",
              value: function () {
                return (
                  !!document.body && document.body.contains(this._component)
                );
              },
            },
            {
              key: "_mountToParent",
              value: function (e) {
                var t = this._component.parentElement,
                  n = this._isMounted();
                if (e === t) {
                  if (n) return;
                  this.unmount(), this._mountTo(e);
                } else if (t) {
                  if (n)
                    throw new Ie(
                      "This Element is already mounted. Use `unmount()` to unmount the Element before re-mounting."
                    );
                  this.unmount(), this._mountTo(e);
                } else this._mountTo(e);
              },
            },
            {
              key: "_mountTo",
              value: function (e) {
                var t = new Fe(),
                  n = cr(e, null),
                  r = !!n && "rtl" === n.getPropertyValue("direction"),
                  o = this._paymentRequest
                    ? this._paymentRequest._activeBackingLibraryName
                    : null;
                for (this._parent = e; e.firstChild; )
                  e.removeChild(e.firstChild);
                e.appendChild(this._component),
                  this._frame.send({
                    action: "stripe-user-mount",
                    payload: {
                      mountTime: t.getAsPosixTime(),
                      rtl: r,
                      paymentRequestButtonType: o,
                    },
                  }),
                  this._findPossibleLabel(),
                  this._updateClasses();
              },
            },
            {
              key: "_updateClasses",
              value: function () {
                this._parent &&
                  pn(this._parent, [
                    [this._classes.base, !0],
                    [this._classes.empty, this._empty],
                    [this._classes.focus, this._focused],
                    [this._classes.invalid, this._invalid],
                    [this._classes.complete, this._complete],
                    [this._classes.webkitAutofill, this._autofilled],
                  ]);
              },
            },
            {
              key: "_removeClasses",
              value: function () {
                this._parent &&
                  pn(this._parent, [
                    [this._classes.base, !1],
                    [this._classes.empty, !1],
                    [this._classes.focus, !1],
                    [this._classes.invalid, !1],
                    [this._classes.complete, !1],
                    [this._classes.webkitAutofill, !1],
                  ]);
              },
            },
            {
              key: "_findPossibleLabel",
              value: function () {
                var e = this._parent;
                if (e) {
                  var t = e.getAttribute("id"),
                    n = void 0;
                  if (
                    (t &&
                      (n = document.querySelector("label[for='" + t + "']")),
                    n)
                  )
                    this._listenerRegistry.addEventListener(
                      e,
                      "click",
                      this.focus
                    );
                  else
                    for (
                      n = n || e.parentElement;
                      n && "LABEL" !== n.nodeName;

                    )
                      n = n.parentElement;
                  n
                    ? ((this._label = n),
                      this._listenerRegistry.addEventListener(
                        n,
                        "click",
                        this.focus
                      ))
                    : this._listenerRegistry.addEventListener(
                        e,
                        "click",
                        this.focus
                      );
                }
              },
            },
            {
              key: "_computeCustomClasses",
              value: function (e) {
                var t = {};
                return (
                  Object.keys(e).forEach(function (n) {
                    if (!qa[n])
                      throw new Ie(
                        n +
                          " is not a customizable class name.\nYou can customize: " +
                          Object.keys(qa).join(", ")
                      );
                    var r = e[n] || qa[n];
                    t[n] = r.replace(/\./g, " ");
                  }),
                  (this._classes = La({}, this._classes, t)),
                  this
                );
              },
            },
            {
              key: "_emitEvent",
              value: function (e, t) {
                return this._emit(
                  e,
                  La({ elementType: this._componentName }, t)
                );
              },
            },
            {
              key: "_setupEvents",
              value: function () {
                var e = this;
                this._frame._on("redirectfocus", function (t) {
                  var n = t.focusDirection,
                    r = sr(e._component, n);
                  r && r.focus();
                }),
                  this._frame._on("focus", function () {
                    (e._focused = !0), e._updateClasses();
                  }),
                  this._frame._on("blur", function () {
                    (e._focused = !1),
                      e._updateClasses(),
                      e._lastSubmittedAt &&
                        "paymentRequestButton" === e._componentName &&
                        (e._controller.report(
                          "payment_request_button.sheet_visible",
                          { latency: new Date() - e._lastSubmittedAt }
                        ),
                        (e._lastSubmittedAt = null));
                  }),
                  this._frame._on("submit", function () {
                    if ("paymentRequestButton" === e._componentName) {
                      e._lastSubmittedAt = new Date();
                      var t = !1,
                        n = !1;
                      so(),
                        e._emitEvent("click", {
                          preventDefault: function () {
                            e._controller.report(
                              "payment_request_button.default_prevented"
                            ),
                              t &&
                                e._controller.warn(
                                  "event.preventDefault() was called after the payment sheet was shown. Make sure to call it synchronously when handling the `click` event."
                                ),
                              (n = !0);
                          },
                        }),
                        !n &&
                          e._paymentRequest &&
                          (e._paymentRequest._elementShow(), (t = !0));
                    } else e._emitEvent("submit"), e._formSubmit();
                  }),
                  ["ready", "focus", "blur", "escape"].forEach(function (t) {
                    e._frame._on(t, function () {
                      e._emitEvent(t);
                    });
                  }),
                  this._frame._on("change", function (t) {
                    so();
                    var n = {};
                    ["error", "value", "empty", "complete"]
                      .concat(te(yo[e._componentName] || []))
                      .forEach(function (e) {
                        return (n[e] = t[e]);
                      }),
                      e._emitEvent("change", n),
                      (e._empty = n.empty),
                      (e._invalid = !!n.error),
                      (e._complete = n.complete),
                      e._updateClasses();
                  }),
                  this._frame._on("__privateIntegrationError", function (t) {
                    var n = t.message;
                    e._emitEvent("__privateIntegrationError", { message: n });
                  }),
                  this._frame._on("dimensions", function (t) {
                    if (e._parent) {
                      var n = cr(e._parent, null);
                      if (n) {
                        var r = parseFloat(n.getPropertyValue("height")),
                          o = t.height;
                        if ("border-box" === n.getPropertyValue("box-sizing")) {
                          var i = parseFloat(n.getPropertyValue("padding-top")),
                            a = parseFloat(
                              n.getPropertyValue("padding-bottom")
                            );
                          r =
                            r -
                            parseFloat(n.getPropertyValue("border-top")) -
                            parseFloat(n.getPropertyValue("border-bottom")) -
                            i -
                            a;
                        }
                        0 !== r &&
                          Fa(r) < Fa(o) &&
                          e._controller.report("wrapper_height_mismatch", {
                            height: o,
                            outer_height: r,
                          });
                        var c = e._component.getBoundingClientRect().height;
                        0 !== c &&
                          0 !== o &&
                          Fa(c) !== Fa(o) &&
                          (e._frame.updateStyle({ height: o + "px" }),
                          e._controller.report("iframe_height_update", {
                            height: o,
                            calculated_height: c,
                          }));
                      }
                    }
                  }),
                  this._frame._on("autofill", function () {
                    if (e._parent) {
                      var t = e._parent.style.backgroundColor,
                        n = "#faffbd" === t || "rgb(250, 255, 189)" === t;
                      (e._lastBackgroundColor = n ? e._lastBackgroundColor : t),
                        (e._parent.style.backgroundColor = "#faffbd"),
                        (e._autofilled = !0),
                        e._updateClasses();
                    }
                  }),
                  this._frame._on("autofill-cleared", function () {
                    (e._autofilled = !1),
                      e._parent &&
                        (e._parent.style.backgroundColor =
                          e._lastBackgroundColor),
                      e._updateClasses();
                  });
              },
            },
            {
              key: "_handleOutsideClick",
              value: function () {
                this._secondaryFrame &&
                  this._secondaryFrame.send({
                    action: "stripe-outside-click",
                    payload: {},
                  });
              },
            },
            {
              key: "_createSecondFrame",
              value: function (e, t, n) {
                var r = this._controller.createSecondaryElementFrame(
                  e,
                  La({}, n, { componentName: t })
                );
                return (
                  r &&
                    r.on &&
                    r.on("height-change", function (e) {
                      r.updateStyle({ height: e.height + "px" });
                    }),
                  r
                );
              },
            },
            {
              key: "_createComponent",
              value: function (e, t) {
                this._createElement(e, t),
                  this._setupEvents(),
                  this._updateFrameHeight(e, !0);
              },
            },
            {
              key: "_updateFrameHeight",
              value: function (e) {
                var t =
                  arguments.length > 1 &&
                  void 0 !== arguments[1] &&
                  arguments[1];
                if ("paymentRequestButton" === this._componentName) {
                  var n = (e.style && e.style.paymentRequestButton) || {},
                    r = n.height,
                    o = "string" == typeof r ? r : void 0;
                  (t || o) &&
                    (this._frame.updateStyle({
                      height: o || this._lastHeight || "40px",
                    }),
                    (this._lastHeight = o || this._lastHeight));
                } else {
                  var i = (e.style && e.style.base) || {},
                    a = i.lineHeight,
                    c = i.fontSize,
                    s = i.padding,
                    u =
                      "string" != typeof a || isNaN(parseFloat(a)) ? void 0 : a,
                    l = "string" == typeof c ? c : void 0,
                    p = "string" == typeof s ? s : void 0;
                  if (
                    (l &&
                      !Ua(l) &&
                      this._controller.warn(
                        "The fontSize style you specified (" +
                          l +
                          ") is not in px. We do not recommend using relative css units, as they will be calculated relative to our iframe's styles rather than your site's."
                      ),
                    t || u || l)
                  ) {
                    var f =
                        -1 === en.indexOf(this._componentName)
                          ? void 0
                          : p || this._lastPadding,
                      d = ja(u || this._lastHeight, l || this._lastFontSize, f);
                    this._frame.updateStyle({ height: d }),
                      (this._lastFontSize = l || this._lastFontSize),
                      (this._lastHeight = u || this._lastHeight),
                      (this._lastPadding = f);
                  }
                }
              },
            },
            {
              key: "_createElement",
              value: function (e, t) {
                var n = this,
                  r =
                    (e.classes,
                    e.controller,
                    e.paymentRequest,
                    ee(e, ["classes", "controller", "paymentRequest"])),
                  o = document.createElement("div");
                o.className = "__PrivateStripeElement";
                var i = document.createElement("input");
                (i.className = "__PrivateStripeElement-input"),
                  i.setAttribute("aria-hidden", "true"),
                  i.setAttribute("aria-label", " "),
                  i.setAttribute("autocomplete", "false"),
                  (i.maxLength = 1),
                  (i.disabled = !0),
                  fn(o, Da),
                  fn(i, Ba);
                var a = cr(document.body),
                  c = !!a && "rtl" === a.getPropertyValue("direction"),
                  s = fo[t],
                  u = La({}, r, { rtl: c }),
                  l = this._controller.createElementFrame(s, u);
                if (
                  (l._on("load", function () {
                    i.disabled = !1;
                  }),
                  this._listenerRegistry.addEventListener(
                    i,
                    "focus",
                    function () {
                      l.focus(-1 !== n._controller._flags.indexOf("a"));
                    }
                  ),
                  l.appendTo(o),
                  vo[t])
                ) {
                  var p = vo[t].secondary;
                  (this._secondaryFrame = this._createSecondFrame(
                    s,
                    p,
                    La({}, u, { primaryElementType: t })
                  )),
                    this._secondaryFrame.appendTo(o),
                    this._listenerRegistry.addEventListener(
                      window,
                      "click",
                      function () {
                        return n._handleOutsideClick();
                      }
                    );
                }
                if ((o.appendChild(i), Kn && t !== Wt.paymentRequestButton)) {
                  var f = document.createElement("input");
                  (f.className = "__PrivateStripeElement-safariInput"),
                    f.setAttribute("aria-hidden", "true"),
                    f.setAttribute("tabindex", "-1"),
                    f.setAttribute("autocomplete", "false"),
                    (f.maxLength = 1),
                    (f.disabled = !0),
                    fn(f, Ba),
                    o.appendChild(f);
                }
                (this._component = o), (this._frame = l), (this._fakeInput = i);
              },
            },
          ]),
          t
        );
      })(An),
      Ga = function () {
        var e = this;
        (this._paymentRequest = null),
          (this.mount = wn(function (t) {
            e._checkDestroyed();
            var n = void 0;
            if (!t)
              throw new Ie(
                "Missing argument. Make sure to call mount() with a valid DOM element or selector."
              );
            if ("string" == typeof t) {
              var r = document.querySelectorAll(t);
              if (
                (r.length > 1 &&
                  e._controller.warn(
                    "The selector you specified (" +
                      t +
                      ") applies to " +
                      r.length +
                      " DOM elements that are currently on the page.\nThe Stripe Element will be mounted to the first one."
                  ),
                !r.length)
              )
                throw new Ie(
                  "The selector you specified (" +
                    t +
                    ") applies to no DOM elements that are currently on the page.\nMake sure the element exists on the page before calling mount()."
                );
              n = r[0];
            } else {
              if (!t.appendChild)
                throw new Ie(
                  "Invalid DOM element. Make sure to call mount() with a valid DOM element or selector."
                );
              n = t;
            }
            if ("INPUT" === n.nodeName)
              throw new Ie(
                "Stripe Elements must be mounted in a DOM element that\ncan contain child nodes. `input` elements are not permitted to have child\nnodes. Try using a `div` element instead."
              );
            if (
              (n.children.length &&
                e._controller.warn(
                  "This Element will be mounted to a DOM element that contains child nodes."
                ),
              e._paymentRequest)
            ) {
              if (!e._paymentRequest._canMakePaymentResolved)
                throw new Ie(
                  "For the paymentRequestButton Element, you must first check availability using paymentRequest.canMakePayment() before mounting the Element."
                );
              if (!e._paymentRequest._activeBackingLibraryName)
                throw new Ie(
                  "The paymentRequestButton Element is not available in the current environment."
                );
              e._mountToParent(n);
            } else e._mountToParent(n);
          })),
          (this.update = wn(function (t) {
            e._checkDestroyed();
            var n = xt(Sa, t || {}, "element.update()"),
              r = n.value;
            if (
              (n.warnings.forEach(function (t) {
                return e._controller.warn(t);
              }),
              r)
            ) {
              var o = r.classes,
                i = ee(r, ["classes"]);
              o &&
                (e._removeClasses(),
                e._computeCustomClasses(o),
                e._updateClasses()),
                e._updateFrameHeight(r),
                Object.keys(i).length &&
                  (e._frame.update(i),
                  e._secondaryFrame && e._secondaryFrame.update(i));
            }
            return e;
          })),
          (this.focus = wn(function (t) {
            return (
              e._checkDestroyed(),
              t && t.preventDefault(),
              document.activeElement &&
                document.activeElement.blur &&
                document.activeElement.blur(),
              e._fakeInput.focus(),
              e
            );
          })),
          (this.blur = wn(function () {
            return e._checkDestroyed(), e._frame.blur(), e._fakeInput.blur(), e;
          })),
          (this.clear = wn(function () {
            return e._checkDestroyed(), e._frame.clear(), e;
          })),
          (this.unmount = wn(function () {
            e._checkDestroyed();
            var t = e._component.parentElement,
              n = e._label;
            return (
              t &&
                (t.removeChild(e._component),
                e._listenerRegistry.removeEventListener(t, "click", e.focus),
                e._removeClasses()),
              (e._parent = null),
              n &&
                (e._listenerRegistry.removeEventListener(n, "click", e.focus),
                (e._label = null)),
              e._secondaryFrame &&
                (e._secondaryFrame.unmount(),
                e._listenerRegistry.removeEventListener(
                  window,
                  "click",
                  e._handleOutsideClick
                )),
              (e._fakeInput.disabled = !0),
              e._frame.unmount(),
              e
            );
          })),
          (this.destroy = wn(function () {
            return (
              e._checkDestroyed(),
              e.unmount(),
              (e._destroyed = !0),
              e._emitEvent("destroy"),
              e
            );
          })),
          (this._formSubmit = function () {
            for (
              var t = e._component.parentElement;
              t && "FORM" !== t.nodeName;

            )
              t = t.parentElement;
            if (t) {
              var n = document.createEvent("Event");
              n.initEvent("submit", !0, !0), t.dispatchEvent(n);
            }
          });
      },
      Wa = Ha,
      Ya =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      za = {
        locale: pt(bt),
        fonts: pt(Tt(At)),
        betas: pt(Tt(mt.apply(void 0, ce(Mo)))),
      },
      Ka = Ct(za),
      Va = function e(t, n, r) {
        var o = this;
        ae(this, e), Ja.call(this);
        var i = xt(Ka, r || {}, "elements()"),
          a = i.value;
        i.warnings.forEach(function (e) {
          return t.warn(e);
        }),
          Io(t.warn),
          t.report("elements", { options: r }),
          (this._elements = []),
          (this._id = nn("elements")),
          (this._controller = t),
          (this._betas = a.betas || []),
          (this._listenerRegistry = n),
          (a.locale = Oa(a.locale, this._betas));
        var c = a.locale,
          s = a.fonts || [];
        this._controller.action.fetchLocale({ locale: c || "auto" });
        var u = s
            .filter(function (e) {
              return !e.cssSrc || "string" != typeof e.cssSrc;
            })
            .map(function (e) {
              return Ya({}, e, {
                __resolveFontRelativeTo: window.location.href,
              });
            }),
          l = s
            .map(function (e) {
              return e.cssSrc;
            })
            .reduce(function (e, t) {
              return "string" == typeof t ? [].concat(ce(e), [t]) : e;
            }, [])
            .map(function (e) {
              return tt(e) ? e : rt(window.location.href, e);
            });
        this._pendingFonts = l.length;
        var p = (a.betas, ie(a, ["betas"]));
        return (
          (this._commonOptions = Ya({}, p, { fonts: u })),
          l.forEach(function (e) {
            if ("string" == typeof e) {
              var t = new Fe();
              Ko(e)
                .then(function (n) {
                  o._controller.report("font.loaded", {
                    load_time: t.getElapsedTime(),
                    font_count: n.length,
                    css_src: e,
                  });
                  var r = n.map(function (t) {
                    return Ya({}, t, { __resolveFontRelativeTo: e });
                  });
                  o._controller.action.updateCSSFonts({
                    fonts: r,
                    groupId: o._id,
                  }),
                    (o._commonOptions = Ya({}, o._commonOptions, {
                      fonts: [].concat(
                        ce(
                          o._commonOptions.fonts ? o._commonOptions.fonts : []
                        ),
                        ce(r)
                      ),
                    }));
                })
                .catch(function (n) {
                  o._controller.report("error.font.not_loaded", {
                    load_time: t.getElapsedTime(),
                    message: n && n.message && n.message,
                    css_src: e,
                  }),
                    o._controller.warn("Failed to load CSS file at " + e + ".");
                });
            }
          }),
          this
        );
      },
      Ja = function () {
        var e = this;
        (this.getElement = wn(function (t) {
          var n = Ta(t) || t;
          return (
            Ra(n, e._betas),
            He(e._elements, function (e) {
              return e._componentName === n;
            }) || null
          );
        })),
          (this.create = Sn(function (t, n) {
            Ia(
              t,
              e._elements.map(function (e) {
                return e._componentName;
              }),
              e._betas
            );
            var r = xt(Sa, n || {}, "create()"),
              o = r.value;
            r.warnings.forEach(function (t) {
              return e._controller.warn(t);
            });
            var i = Ya({}, o, e._commonOptions, {
                componentName: t,
                groupId: e._id,
              }),
              a = (i.paymentRequest, ie(i, ["paymentRequest"])),
              c = (Yn || zn) && cn(a).length > 2e3,
              s = !!e._pendingFonts || c,
              u = new Wa(
                Ya({}, i, {
                  fonts: c ? null : e._commonOptions.fonts,
                  controller: e._controller,
                  wait: s,
                }),
                e._listenerRegistry
              );
            return (
              (e._elements = [].concat(ce(e._elements), [u])),
              u._on("destroy", function () {
                e._elements = e._elements.filter(function (e) {
                  return e._componentName !== t;
                });
              }),
              c &&
                u._frame.send({
                  action: "stripe-user-update",
                  payload: { fonts: e._commonOptions.fonts },
                }),
              u
            );
          }));
      },
      Xa = Va,
      Qa = function (e, t, n, r, o, i, a) {
        return new ga({
          controller: e,
          authentication: t,
          mids: n,
          rawOptions: r,
          betas: o,
          queryStrategyOverride: i,
          listenerRegistry: a,
        });
      },
      $a = Qa,
      Za = { _componentName: bt, _frame: Ct({ id: bt }) },
      ec = Ct(Za),
      tc = function (e) {
        var t = Lt(ec, e, "");
        return "error" === t.type ? null : t.value;
      },
      nc = {
        alipay: "alipay",
        afterpay_clearpay: "afterpay_clearpay",
        au_becs_debit: "au_becs_debit",
        acss_debit: "acss_debit",
        bacs_debit: "bacs_debit",
        bancontact: "bancontact",
        boleto_pilot: "boleto_pilot",
        card: "card",
        eps: "eps",
        fpx: "fpx",
        giropay: "giropay",
        grabpay: "grabpay",
        ideal: "ideal",
        oxxo: "oxxo",
        p24: "p24",
        sepa_debit: "sepa_debit",
        sofort: "sofort",
        three_d_secure: "three_d_secure",
        upi: "upi",
        wechat_pay: "wechat_pay",
      },
      rc =
        ((Te = {}),
        se(Te, Wt.auBankAccount, nc.au_becs_debit),
        se(Te, Wt.card, nc.card),
        se(Te, Wt.cardNumber, nc.card),
        se(Te, Wt.cardExpiry, nc.card),
        se(Te, Wt.cardCvc, nc.card),
        se(Te, Wt.postalCode, nc.card),
        se(Te, Wt.iban, nc.sepa_debit),
        se(Te, Wt.idealBank, nc.ideal),
        se(Te, Wt.fpxBank, nc.fpx),
        Te),
      oc = function (e) {
        return -1 === Vt.indexOf(e);
      },
      ic = function (e, t) {
        return null != t ? t : oc(e) ? null : rc[e] || null;
      },
      ac =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      cc = function (e, t) {
        switch (e.type) {
          case "object":
            return { paymentIntent: e.object };
          case "error":
            return { error: ac({}, t ? { payment_intent: t } : {}, e.error) };
          default:
            return Ne(e);
        }
      },
      sc = function (e) {
        switch (e.type) {
          case "error":
            return { error: e.error };
          case "object":
            return { setupIntent: e.object };
          default:
            return Ne(e);
        }
      },
      uc = function (e) {
        var t = e.trim().match(/^([a-z]+_[^_]+)_secret_[^-]+$/);
        return t ? { id: t[1], clientSecret: t[0] } : null;
      },
      lc = function (e) {
        return { id: e.id, clientSecret: e.client_secret };
      },
      pc = function (e) {
        return "requires_source_action" === e || "requires_action" === e;
      },
      fc = function (e) {
        return "requires_source_action" === e.status ||
          "requires_action" === e.status
          ? e.next_action
          : null;
      },
      dc =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      _c =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      hc = function (e, t) {
        if ("string" != typeof e) return lt("a client_secret string", e, t);
        var n = uc(e);
        return null === n
          ? lt("a client secret of the form ${id}_secret_${secret}", e, t)
          : ct(n, []);
      },
      mc = function (e, t) {
        if (null === e) return ut("object", "null", t);
        if ("object" !== (void 0 === e ? "undefined" : _c(e)))
          return ut("object", void 0 === e ? "undefined" : _c(e), t);
        var n = e.client_secret,
          r = e.status,
          o = e.next_action,
          i = hc(n, jt(t, "client_secret"));
        if ("error" === i.type) return i;
        if ("string" != typeof r)
          return ut(
            "string",
            void 0 === r ? "undefined" : _c(r),
            jt(t, "status")
          );
        if (
          ("requires_source_action" === r || "requires_action" === r) &&
          "object" !== (void 0 === o ? "undefined" : _c(o))
        )
          return ut(
            "object",
            void 0 === o ? "undefined" : _c(o),
            jt(t, "next_action")
          );
        if ("payment_intent" === e.object) {
          return ct(e, []);
        }
        return ct(e, []);
      },
      yc = function (e) {
        return function (t, n) {
          if ("object" !== (void 0 === t ? "undefined" : _c(t)))
            return ut("object", void 0 === t ? "undefined" : _c(t), n);
          if (null === t) return ut("object", "null", n);
          var r = t.type,
            o = le(t, ["type"]),
            i = void 0;
          if (null === e) {
            if ("string" != typeof r)
              return ut(
                "string",
                void 0 === r ? "undefined" : _c(r),
                jt(n, "type")
              );
            i = r;
          } else {
            if (void 0 !== r && r !== e)
              return "string" != typeof r
                ? ut(
                    "string",
                    void 0 === r ? "undefined" : _c(r),
                    jt(n, "type")
                  )
                : ut('"' + r + '"', '"' + e + '"', jt(n, "type"));
            i = e;
          }
          var a = [
              "afterpay_clearpay",
              "alipay",
              "bancontact",
              "eps",
              "giropay",
              "grabpay",
              "oxxo",
              "p24",
              "wechat_pay",
            ],
            c = o[i],
            s = (o[i], le(o, [i]));
          if (
            (-1 !== a.indexOf(i) && void 0 === c && (c = {}),
            "object" !== (void 0 === c ? "undefined" : _c(c)))
          )
            return ut("object or element", _c(t[i]), jt(n, i));
          if (null === c) return ut("object or element", "null", jt(n, i));
          var u = tc(c);
          if (u) {
            var l = u._componentName;
            if (rc[l] !== i) {
              var p = [].concat(ue(n.path), [i]).join("."),
                f = n.label,
                d = new Ie(
                  "Invalid value for " +
                    f +
                    ": " +
                    p +
                    " was `" +
                    l +
                    "` Element, which cannot be used to create " +
                    i +
                    " PaymentMethods."
                );
              return st(d);
            }
            return ct({ type: i, element: u, data: s });
          }
          return ct({ type: i, element: null, data: o });
        };
      },
      vc = function (e) {
        return function (t, n) {
          if (null == t) return ct(null);
          if ("object" !== (void 0 === t ? "undefined" : _c(t)))
            return ut("object", void 0 === t ? "undefined" : _c(t), n);
          var r = t.card,
            o = le(t, ["card"]);
          if (!r || "object" !== (void 0 === r ? "undefined" : _c(r)))
            return ct(t);
          var i = r.cvc,
            a = le(r, ["cvc"]);
          if (null == i) return ct(t);
          var c = tc(i),
            s = c ? c._componentName : "";
          return Wt.cardCvc !== s
            ? ut(
                "`" + Wt.cardCvc + "` Element",
                s ? "`" + s + "` Element" : void 0 === i ? "undefined" : _c(i),
                jt(n, e + ".cvc")
              )
            : ct(dc({}, o, { card: dc({}, a, { cvc: c }) }));
        };
      },
      bc = gt(
        Ct({
          handleActions: gt(Et, function () {
            return !0;
          }),
        }),
        function () {
          return { handleActions: !0 };
        }
      ),
      gc = function (e, t) {
        return function (n, r) {
          if (void 0 === n)
            return ct({
              paymentMethodData: null,
              paymentMethodOptions: null,
              source: null,
              paymentMethod: null,
              otherParams: {},
            });
          if ("object" !== (void 0 === n ? "undefined" : _c(n)))
            return ut("object", void 0 === n ? "undefined" : _c(n), r);
          if (null === n) return ut("object", "null", r);
          var o = n.source,
            i = n.source_data,
            a = n.payment_method_data,
            c = n.payment_method_options,
            s = n.payment_method,
            u = le(n, [
              "source",
              "source_data",
              "payment_method_data",
              "payment_method_options",
              "payment_method",
            ]);
          if (null != i)
            throw new Ie(
              t + ": Expected payment_method, or source, not source_data."
            );
          if (null != a)
            throw new Ie(
              t +
                ": Expected payment_method, or source, not payment_method_data."
            );
          if (null != o && null != s)
            throw new Ie(
              t + ": Expected either payment_method or source, but not both."
            );
          if (null != o)
            return "string" != typeof o
              ? ut(
                  "string",
                  void 0 === o ? "undefined" : _c(o),
                  jt(r, "source")
                )
              : ct({
                  source: o,
                  paymentMethodData: null,
                  paymentMethodOptions: null,
                  paymentMethod: null,
                  otherParams: u,
                });
          if (
            null != s &&
            "string" != typeof s &&
            "object" !== (void 0 === s ? "undefined" : _c(s))
          )
            return ut(
              "string or object",
              void 0 === s ? "undefined" : _c(s),
              jt(r, "payment_method")
            );
          var l = Lt(vc(e), c, t, {
            path: [].concat(ue(r.path), ["payment_method_options"]),
          });
          if ("error" === l.type) return l;
          if ("string" == typeof s)
            return ct({
              source: null,
              paymentMethodData: null,
              paymentMethodOptions: l.value,
              paymentMethod: s,
              otherParams: u,
            });
          if ("object" === (void 0 === s ? "undefined" : _c(s)) && null !== s) {
            var p = Lt(yc(e), s, t, {
              path: [].concat(ue(r.path), ["payment_method"]),
            });
            if ("error" === p.type) return p;
            var f = p.value;
            return ct({
              source: null,
              paymentMethod: null,
              paymentMethodOptions: l.value,
              paymentMethodData: f,
              otherParams: u,
            });
          }
          return ct({
            source: null,
            paymentMethodData: null,
            paymentMethodOptions: null,
            paymentMethod: null,
            otherParams: u,
          });
        };
      },
      Ec = Ct({
        name: ht("react-stripe-js", "stripe-js", "react-stripe-elements"),
        version: (function (e) {
          return function (t, n) {
            return null === t ? ct(t) : e(t, n);
          };
        })(bt),
      }),
      wc = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      Sc = ["elements", "createToken", "createPaymentMethod"],
      Pc = ["elements", "createSource", "createToken", "createPaymentMethod"],
      Oc = (function () {
        function e(t) {
          var n = this;
          pe(this, e),
            (this._gets = []),
            (this._didDetect = !1),
            (this._onDetection = function (e) {
              (n._didDetect = !0), t(e);
            }),
            window.Stripe &&
              window.Stripe.__cachedInstances &&
              this._onDetection("react-stripe-elements");
        }
        return (
          wc(e, [
            {
              key: "got",
              value: function (e) {
                this._didDetect ||
                  ("elements" === e
                    ? (this._gets = ["elements"])
                    : this._gets.push(e),
                  this._checkForWrapper());
              },
            },
            {
              key: "called",
              value: function (e) {
                this._didDetect ||
                  (this._gets = this._gets.filter(function (t) {
                    return t !== e;
                  }));
              },
            },
            {
              key: "_checkForWrapper",
              value: function () {
                We(this._gets, Sc)
                  ? this._onDetection("react-stripe-js")
                  : We(this._gets, Pc) &&
                    this._onDetection("react-stripe-elements");
              },
            },
          ]),
          e
        );
      })(),
      kc =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      Ac = function (e) {
        if (!e || "object" !== (void 0 === e ? "undefined" : kc(e)))
          return null;
        var t = e.type,
          n = fe(e, ["type"]);
        return { type: "string" == typeof t ? t : null, data: n };
      },
      Tc = function (e) {
        switch (e.type) {
          case "object":
            return { source: e.object };
          case "error":
            return { error: e.error };
          default:
            return Ne(e);
        }
      },
      Rc = {
        source: Ct({ id: _t("src_"), client_secret: _t("src_client_secret_") }),
      },
      Ic = Ct(Rc),
      Nc = function (e) {
        switch (e.type) {
          case "object":
            return { paymentMethod: e.object };
          case "error":
            return { error: e.error };
          default:
            return Ne(e);
        }
      },
      Mc = function (e) {
        return xt(yc(null), e, "createPaymentMethod").value;
      },
      Cc = function (e, t, n, r, o) {
        var i = tc(r),
          a = Ac(i ? o : r),
          c = a || { type: null, data: {} },
          s = c.type,
          u = c.data;
        if (s && n !== s)
          return Le.reject(
            new Ie(
              "The type supplied in payment_method_data is not consistent."
            )
          );
        if (i) {
          var l = i._frame.id,
            p = i._componentName;
          return e.action
            .createPaymentMethodWithElement({
              frameId: l,
              elementName: p,
              type: n,
              paymentMethodData: u,
              mids: t,
            })
            .then(Nc);
        }
        return a
          ? e.action
              .createPaymentMethodWithData({
                elementName: null,
                type: n,
                paymentMethodData: u,
                mids: t,
              })
              .then(Nc)
          : Le.reject(
              new Ie(
                "Please provide either an Element or PaymentMethod creation parameters to createPaymentMethod."
              )
            );
      },
      jc = function (e, t, n, r, o) {
        if ("string" == typeof n) return Cc(e, t, n, r, o);
        try {
          var i = Mc(n),
            a = i.element,
            c = i.type,
            s = i.data;
          if (a) {
            var u = a._frame.id,
              l = a._componentName;
            return e.action
              .createPaymentMethodWithElement({
                frameId: u,
                elementName: l,
                type: c,
                paymentMethodData: s,
                mids: t,
              })
              .then(Nc);
          }
          return e.action
            .createPaymentMethodWithData({
              elementName: null,
              type: c,
              paymentMethodData: s,
              mids: t,
            })
            .then(Nc);
        } catch (e) {
          return Le.reject(e);
        }
      },
      Lc = function (e) {
        return (
          "https://stripe.com/docs/stripe-js/reference#stripe-" +
          e
            .split(/(?=[A-Z])/)
            .join("-")
            .toLowerCase()
        );
      },
      xc = function (e, t) {
        return xt(hc, e, "stripe." + t + " intent secret").value;
      },
      qc = function (e, t) {
        return xt(bc, t, e).value;
      },
      Dc = function (e, t, n) {
        if ("valid" === Lt(ec, n, t).type)
          throw new Ie(
            "Do not pass an Element to stripe." +
              t +
              "() directly.\nFor more information: " +
              Lc(t)
          );
        var r = xt(gc(e, t), n, t),
          o = r.value,
          i = o.source,
          a = o.paymentMethodData,
          c = o.paymentMethodOptions,
          s = o.paymentMethod,
          u = o.otherParams;
        if (null != i && (null != a || null != s))
          throw new Ie(
            t + ": Expected either source or payment_method, but not both."
          );
        return a
          ? a.element
            ? {
                confirmMode: {
                  tag: "paymentMethod-from-element",
                  type: e,
                  elementName: a.element._componentName,
                  frameId: a.element._frame.id,
                  data: a.data,
                  options: c,
                },
                otherParams: u,
              }
            : {
                confirmMode: {
                  tag: "paymentMethod-from-data",
                  type: e,
                  data: a.data,
                  options: c,
                },
                otherParams: u,
              }
          : s
          ? {
              confirmMode: {
                tag: "paymentMethod",
                paymentMethod: s,
                options: c,
              },
              otherParams: u,
            }
          : i
          ? { confirmMode: { tag: "source", source: i }, otherParams: u }
          : { confirmMode: { tag: "none" }, otherParams: u };
      },
      Bc = function (e, t) {
        var n = {
          skipFingerprint: !1,
          sandboxFingerprintFrame: !1,
          sandboxChallengeFrame: !1,
        };
        return (
          -1 !== e.indexOf("Y") &&
            (t.report("3ds2.optimization.Y"), (n.skipFingerprint = !0)),
          -1 !== e.indexOf("k") &&
            (t.report("3ds2.optimization.k"), (n.sandboxFingerprintFrame = !0)),
          -1 !== e.indexOf("5") &&
            (t.report("3ds2.optimization.5"), (n.sandboxChallengeFrame = !0)),
          n
        );
      },
      Fc = function (e) {
        return (
          {
            american_express: "amex",
            visa: "visa",
            mastercard: "mastercard",
            discover: "discover",
          }[e] || "unknown"
        );
      },
      Uc = function (e, t, n) {
        if (!e) return null;
        if ("use_stripe_sdk" === e.type) {
          var r = e.use_stripe_sdk;
          switch (r.type) {
            case "stripe_3ds2_fingerprint":
              return {
                type: "3ds2-fingerprint",
                threeDS2Source: r.three_d_secure_2_source,
                cardBrand: Fc(r.directory_server_name),
                transactionId: r.server_transaction_id,
                optimizations: Bc(r.three_ds_optimizations, n),
                methodUrl: r.three_ds_method_url,
              };
            case "stripe_3ds2_challenge":
              return {
                type: "3ds2-challenge",
                threeDS2Source: r.stripe_js.three_d_secure_2_source,
                cardBrand: Fc(r.stripe_js.directory_server_name),
                transactionId: r.stripe_js.server_transaction_id,
                optimizations: Bc(r.stripe_js.three_ds_optimizations, n),
                acsTransactionId: r.stripe_js.acs_transaction_id,
                acsUrl: r.stripe_js.acs_url,
                creq: r.stripe_js.creq,
              };
            case "three_d_secure_redirect":
              return { type: "3ds1-modal", url: r.stripe_js, source: r.source };
          }
        }
        if ("redirect_to_url" === e.type)
          return { type: "redirect", redirectUrl: e.redirect_to_url.url };
        if ("alipay_handle_redirect" === e.type)
          return {
            type: "redirect",
            redirectUrl: e.alipay_handle_redirect.url,
          };
        if ("display_boleto_details" === e.type)
          return { type: "boleto-display" };
        if ("display_oxxo_details" === e.type)
          return {
            type: "oxxo-display",
            hostedVoucherUrl: e.display_oxxo_details.hosted_voucher_url,
          };
        if ("authorize_with_url" === e.type) {
          var o = e.authorize_with_url.url;
          switch (t) {
            case nc.card:
              return { type: "3ds1-modal", url: o, source: null };
            case nc.ideal:
              return { type: "redirect", redirectUrl: o };
          }
        }
        return "upi_await_notification" === e.type
          ? { type: "upi_await_notification" }
          : "wechat_pay_display_qr_code" === e.type
          ? { type: "wechat_pay_display_qr_code" }
          : null;
      },
      Hc = function (e) {
        switch (e.type) {
          case "error":
            return { error: e.error };
          case "object":
            switch (e.object.object) {
              case "payment_intent":
                return { paymentIntent: e.object };
              case "setup_intent":
                return { setupIntent: e.object };
              default:
                return Ne(e.object);
            }
          default:
            return Ne(e);
        }
      },
      Gc = function (e, t, n, r) {
        return t === zt.PAYMENT_INTENT
          ? n.action
              .retrievePaymentIntent({
                hosted: !1,
                intentSecret: e,
                locale: r,
                asErrorIfNotSucceeded: !0,
              })
              .then(Hc)
          : n.action
              .retrieveSetupIntent({
                hosted: !1,
                intentSecret: e,
                locale: r,
                asErrorIfNotSucceeded: !0,
              })
              .then(Hc);
      },
      Wc = function (e, t, n, r, o) {
        return t === zt.PAYMENT_INTENT
          ? n.action
              .cancelPaymentIntentSource({
                intentSecret: e,
                locale: o,
                sourceId: r,
              })
              .then(Hc)
          : n.action
              .cancelSetupIntentSource({
                intentSecret: e,
                locale: o,
                sourceId: r,
              })
              .then(Hc);
      },
      Yc = function (e) {
        return (
          (e.error
            ? e.error.payment_intent || e.error.setup_intent
            : e.paymentIntent || e.setupIntent) || null
        );
      },
      zc = function (e, t, n, r, o) {
        var i = !0,
          a = 3,
          c = void 0,
          s = 0;
        return (
          (function u() {
            (s += 1),
              Gc(e, t, n, r).then(function (e) {
                if (i) {
                  var t = Yc(e);
                  if (null !== t)
                    switch (((a = 3), t.status)) {
                      case "requires_action":
                      case "requires_source_action":
                        return void (c = setTimeout(u, 5e3));
                      case "processing":
                        return void (c = setTimeout(u, 1e3));
                      default:
                        o(e, s);
                    }
                  else if (a > 0) {
                    var n = 500 * Math.pow(2, 3 - a);
                    (c = setTimeout(u, n)), (a -= 1);
                  } else o(e, s);
                }
              });
          })(),
          function () {
            clearTimeout(c), (i = !1);
          }
        );
      },
      Kc = (function () {
        function e(e, t) {
          var n = [],
            r = !0,
            o = !1,
            i = void 0;
          try {
            for (
              var a, c = e[Symbol.iterator]();
              !(r = (a = c.next()).done) &&
              (n.push(a.value), !t || n.length !== t);
              r = !0
            );
          } catch (e) {
            (o = !0), (i = e);
          } finally {
            try {
              !r && c.return && c.return();
            } finally {
              if (o) throw i;
            }
          }
          return n;
        }
        return function (t, n) {
          if (Array.isArray(t)) return t;
          if (Symbol.iterator in Object(t)) return e(t, n);
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance"
          );
        };
      })(),
      Vc =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Jc = function (e, t, n, r, o) {
        return e.createLightboxFrame({
          type: Dt.AUTHORIZE_WITH_URL,
          options: Vc(
            { url: t, locale: o, intentId: n },
            r ? { source: r } : {}
          ),
        });
      },
      Xc = function (e, t, n, r, o) {
        var i = Ro(),
          a = new Fe(),
          c = Jc(r, e.url, t.id, e.source, o);
        return (
          c.show(),
          r.report("authorize_with_url.loading", {
            viewport: i,
            intentId: t.id,
          }),
          c._on("load", function () {
            r.report("authorize_with_url.loaded", {
              loadDuration: a.getElapsedTime(),
              intentId: t.id,
            }),
              c.fadeInBackdrop();
          }),
          c._on("challenge_complete", function () {
            c.fadeOutBackdrop();
          }),
          new Le(function (i, s) {
            var u = e.source;
            u &&
              c._once("cancel", function () {
                Le.all([Wc(t, n, r, u, o), c.destroy()]).then(function (e) {
                  var t = Kc(e, 1),
                    n = t[0];
                  return i(n);
                });
              }),
              c._once("authorize_with_url_done", function () {
                var e = c.destroy();
                zc(t, n, r, o, function (n, o) {
                  e.then(function () {
                    r.report("authorize_with_url.done", {
                      shownDuration: a.getElapsedTime(),
                      success: !("error" in n),
                      intentId: t.id,
                      iterations: o,
                    }),
                      i(n);
                  });
                });
              });
          })
        );
      },
      Qc = (function () {
        function e(e, t) {
          var n = [],
            r = !0,
            o = !1,
            i = void 0;
          try {
            for (
              var a, c = e[Symbol.iterator]();
              !(r = (a = c.next()).done) &&
              (n.push(a.value), !t || n.length !== t);
              r = !0
            );
          } catch (e) {
            (o = !0), (i = e);
          } finally {
            try {
              !r && c.return && c.return();
            } finally {
              if (o) throw i;
            }
          }
          return n;
        }
        return function (t, n) {
          if (Array.isArray(t)) return t;
          if (Symbol.iterator in Object(t)) return e(t, n);
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance"
          );
        };
      })(),
      $c =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Zc = function (e) {
        return new Le(function (t) {
          e._on("load", function () {
            return t(e);
          });
        });
      },
      es = function (e, t, n, r) {
        var o = e.createHiddenFrame(Dt.STRIPE_3DS2_FINGERPRINT, {
          intentId: t,
          locale: r,
          hosted: n,
        });
        e.report("3ds2.fingerprint_frame.loading", { hosted: n, intentId: t });
        var i = Zc(o);
        return (
          i.then(function () {
            e.report("3ds2.fingerprint_frame.loaded", {
              hosted: n,
              intentId: t,
            });
          }),
          i
        );
      },
      ts = function (e, t, n, r, o) {
        var i = t.createLightboxFrame({
          type: Dt.STRIPE_3DS2_CHALLENGE,
          options: { intentId: e, hosted: r, locale: o },
        });
        t.report("3ds2.challenge_frame.loading", { intentId: e, hosted: r }),
          i._on("challenge_complete", function () {
            i.fadeOutBackdrop();
          });
        var a = Zc(i);
        return (
          a.then(function () {
            return t.report("3ds2.challenge_frame.loaded", {
              intentId: e,
              hosted: r,
            });
          }),
          r && (i.show(), i.action.show3DS2Spinner({ cardBrand: n })),
          a
        );
      },
      ns = function (e, t, n, r, o) {
        return t.optimizations.skipFingerprint
          ? Le.resolve({ fingerprintAttempted: !1, fingerprintData: null })
          : "" === t.methodUrl
          ? (n.report("3ds2.fingerprint.no_method_url", {
              hosted: r,
              intentId: e.id,
            }),
            Le.resolve({ fingerprintAttempted: !1, fingerprintData: null }))
          : es(n, e.id, r, o).then(function (e) {
              return e.action
                .perform3DS2Fingerprint({
                  transactionId: t.transactionId,
                  methodUrl: t.methodUrl,
                  shouldSandbox: t.optimizations.sandboxFingerprintFrame,
                })
                .then(function (t) {
                  return e.destroy(), t;
                });
            });
      },
      rs = function (e, t, n, r, o, i) {
        var a = new Fe(),
          c = ts(e.id, r, n.cardBrand, i, o),
          s = function (a) {
            return new Le(function (s) {
              c.then(function (c) {
                c._once("cancel", function () {
                  c.fadeOutBackdrop(), Wc(e, t, r, n.threeDS2Source, o).then(s);
                }),
                  i || (c.show(), c.fadeInBackdrop());
                var u = (a.type, a.optimizations),
                  l = de(a, ["type", "optimizations"]);
                c.action
                  .perform3DS2Challenge(
                    $c({}, l, { shouldSandbox: u.sandboxChallengeFrame })
                  )
                  .then(function () {
                    s();
                  });
              });
            });
          },
          u = function (t) {
            return (
              r.report("3ds2.authenticate", { hosted: i, intentId: e.id }),
              r.action
                .authenticate3DS2({
                  threeDS2Source: n.threeDS2Source,
                  outerWindowWidth: window.innerWidth,
                  hosted: i,
                  fingerprintResult: t,
                })
                .then(function (t) {
                  return (
                    "error" === t.type
                      ? r.report("3ds2.authenticate.error", {
                          error: t.error,
                          hosted: i,
                          intentId: e.id,
                        })
                      : r.report("3ds2.authenticate.success", {
                          hosted: i,
                          intentId: e.id,
                        }),
                    t
                  );
                })
            );
          },
          l = function (n) {
            return Le.all([
              n ? Le.resolve(n) : Gc(e, t, r, o),
              c.then(function (e) {
                return e.destroy();
              }),
            ]).then(function (t) {
              var n = Qc(t, 1),
                o = n[0];
              return (
                r.report(
                  "3ds2.done",
                  $c(
                    {
                      intentId: e.id,
                      hosted: i,
                      totalDuration: a.getElapsedTime(),
                    },
                    o.error ? { error: o.error, success: !1 } : { success: !0 }
                  )
                ),
                o
              );
            });
          };
        switch (n.type) {
          case "3ds2-challenge":
            return s(n).then(l);
          case "3ds2-fingerprint":
            return ns(e, n, r, i, o)
              .then(u)
              .then(function (t) {
                if ("error" === t.type || null === t.object.ares) return l();
                var o = t.object,
                  a = o.ares,
                  c = o.creq;
                return "C" !== a.transStatus || null == c
                  ? (r.report("3ds2.frictionless", {
                      hosted: i,
                      intentId: e.id,
                    }),
                    l())
                  : s({
                      type: "3ds2-challenge",
                      threeDS2Source: n.threeDS2Source,
                      cardBrand: n.cardBrand,
                      transactionId: n.transactionId,
                      acsUrl: a.acsURL,
                      acsTransactionId: a.acsTransID,
                      optimizations: n.optimizations,
                      creq: c,
                    }).then(l);
              });
          default:
            return Ne(n);
        }
      },
      os = function (e, t) {
        var n = e.createLightboxFrame({ type: Dt.LIGHTBOX_APP, options: t });
        return (
          n.show(),
          n._on("nested-frame-loaded", function () {
            n.fadeInBackdrop(),
              setTimeout(function () {
                n.action.openLightboxFrame();
              }, 200);
          }),
          n
        );
      },
      is = function (e) {
        return e.action.closeLightboxFrame(), e.destroy();
      },
      as = function (e) {
        var t = e.controller,
          n = e.url,
          r = e.intent,
          o = e.locale,
          i = os(t, {
            url: _e(n),
            size: "600x700",
            locale: o,
            frameTitle: "oxxo.voucher_frame_title",
          });
        return new Le(function (e) {
          i._on("request-close", function () {
            is(i).then(function () {
              e({ paymentIntent: r });
            });
          });
        });
      },
      cs = function (e) {
        var t = e.controller,
          n = e.intentSecret,
          r = e.intentType,
          o = e.locale;
        return new Le(function (e) {
          var i = function i() {
            Gc(n, r, t, o).then(function (t) {
              var n = Yc(t);
              if (null !== n)
                switch (n.status) {
                  case "requires_action":
                    return void setTimeout(i, 1e4);
                  default:
                    e(t);
                }
            });
          };
          setTimeout(i, 5e3);
        });
      },
      ss = function (e) {
        return new Le(function (t, n) {
          var r = setTimeout(function () {
            t({
              type: "error",
              error: {
                code: "redirect_error",
                message: "Failed to redirect to " + e,
              },
              locale: "en",
            });
          }, 3e3);
          window.addEventListener("pagehide", function () {
            clearTimeout(r);
          }),
            (window.top.location.href = e);
        });
      },
      us = function (e, t, n) {
        e.report("redirect_error", { initiator: t, error: n.error });
      },
      ls = function (e, t, n, r) {
        return ss(n).then(function (n) {
          return us(r, t + " redirect", n), cc(n, e);
        });
      },
      ps = function (e, t, n, r) {
        return ss(n).then(function (e) {
          return us(r, t + " redirect", e), sc(e);
        });
      },
      fs =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      ds = function (e) {
        switch (e.type) {
          case "error":
            var t = e.error;
            if (
              "payment_intent_unexpected_state" === t.code &&
              "object" === fs(t.payment_intent) &&
              null != t.payment_intent &&
              "string" == typeof t.payment_intent.status &&
              pc(t.payment_intent.status)
            ) {
              var n = t.payment_intent;
              return { type: "object", locale: e.locale, object: n };
            }
            return e;
          case "object":
            return e;
          default:
            return Ne(e);
        }
      },
      _s = function (e, t, n, r, o) {
        var i = Uc(fc(t), n, e),
          a = lc(t);
        if (!i) return Le.resolve({ paymentIntent: t });
        switch (i.type) {
          case "3ds1-modal":
            return Xc(i, a, zt.PAYMENT_INTENT, e, r);
          case "3ds2-fingerprint":
          case "3ds2-challenge":
            return rs(a, zt.PAYMENT_INTENT, i, e, r, o);
          case "redirect":
            return ls(t, n, i.redirectUrl, e);
          case "boleto-display":
            throw new Ie(
              "Expected option `handleActions` to be `false`. The Boleto private beta does not handle the next actions for you automatically (e.g. display Boleto details). Please refer to the Stripe Boleto integration guide for more info: \n\nhttps://stripe.com/docs/payments/boleto"
            );
          case "oxxo-display":
            if (void 0 === i.hostedVoucherUrl)
              throw new Ie(
                "To handle the next actions automatically, set the API version to oxxo_beta=v2. Please refer to the Stripe OXXO integration guide for more info: \n\nhttps://stripe.com/docs/payments/oxxo"
              );
            return as({
              controller: e,
              locale: r,
              url: i.hostedVoucherUrl,
              intent: t,
            });
          case "upi_await_notification":
            return cs({
              controller: e,
              intentSecret: a,
              intentType: zt.PAYMENT_INTENT,
              locale: r,
            });
          case "wechat_pay_display_qr_code":
            throw new Ie("Expected option `handleActions` to be `false`.");
          default:
            return Le.resolve({ paymentIntent: t });
        }
      },
      hs = function (e, t, n, r, o) {
        return _s(e, t, n, r, o).then(function (e) {
          if (e.setupIntent)
            throw new Error("Got unexpected SetupIntent response");
          return e;
        });
      },
      ms = function (e, t, n, r) {
        return function (o) {
          var i = ds(o);
          switch (i.type) {
            case "error":
              var a = i.error,
                c = a.payment_intent;
              return n &&
                c &&
                "payment_intent_unexpected_state" === a.code &&
                ("succeeded" === c.status || "requires_capture" === c.status)
                ? Le.resolve({ paymentIntent: c })
                : Le.resolve(cc(o));
            case "object":
              var s = i.object;
              return hs(e, s, t, i.locale, r);
            default:
              return Ne(i);
          }
        };
      },
      ys =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      vs = function (e, t) {
        return function (n, r, o, i, a) {
          var c = xc(o, e),
            s = Dc(t, e, i),
            u = qc(e, a),
            l = "none" === s.confirmMode.tag,
            p = n.action.confirmPaymentIntent(
              ys({}, s, {
                intentSecret: c,
                expectedType: t,
                options: u,
                mids: r,
              })
            );
          return u.handleActions ? p.then(ms(n, t, l, !1)) : p.then(cc);
        };
      },
      bs = vs("confirmAcssDebitPayment", nc.acss_debit),
      gs = vs("confirmAfterpayClearpayPayment", nc.afterpay_clearpay),
      Es = vs("confirmAuBecsDebitPayment", nc.au_becs_debit),
      ws = vs("confirmBacsDebitPayment", nc.bacs_debit),
      Ss = vs("confirmBancontactPayment", nc.bancontact),
      Ps = vs("confirmBoletoPilotPayment", nc.boleto_pilot),
      Os = vs("confirmCardPayment", nc.card),
      ks = vs("confirmEpsPayment", nc.eps),
      As = vs("confirmFpxPayment", nc.fpx),
      Ts = vs("confirmGiropayPayment", nc.giropay),
      Rs = vs("confirmGrabPayPayment", nc.grabpay),
      Is = vs("confirmIdealPayment", nc.ideal),
      Ns = vs("confirmOxxoPayment", nc.oxxo),
      Ms = vs("confirmAlipayPayment", nc.alipay),
      Cs = vs("confirmP24Payment", nc.p24),
      js = vs("confirmSepaDebitPayment", nc.sepa_debit),
      Ls = vs("confirmSofortPayment", nc.sofort),
      xs = vs("confirmUpiPayment", nc.upi),
      qs = function (e, t, n, r, o) {
        if (o && !0 === o.handleActions)
          throw new Ie("Expected option `handleActions` to be `false`.");
        var i = ys({}, r, {
          payment_method_options: ys(
            {},
            (r && r.payment_method_options) || {},
            {
              wechat_pay: ys(
                {},
                (r &&
                  r.payment_method_options &&
                  r.payment_method_options.wechat_pay) ||
                  {},
                { client: "web_manual_display" }
              ),
            }
          ),
        });
        return vs("confirmWechatPayPayment", nc.wechat_pay)(e, t, n, i, o);
      },
      Ds = function (e, t) {
        var n = xc(e, "retrievePaymentIntent");
        return t.action
          .retrievePaymentIntent({ intentSecret: n, hosted: !1 })
          .then(cc);
      },
      Bs = function (e, t, n) {
        var r = xc(t, "verifyMicrodepositsForSetup"),
          o = xt(At, n, "stripe.verifyMicrodepositsForSetup");
        return e.action
          .verifyMicrodepositsForPayment({ intentSecret: r, data: o.value })
          .then(cc);
      },
      Fs = function (e, t) {
        var n = xc(e, "handleHosted3DS2Setup [internal]");
        return t.action
          .retrievePaymentIntent({ intentSecret: n, hosted: !0 })
          .then(ms(t, nc.card, !1, !0));
      },
      Us = function (e, t) {
        var n = xc(e, "handleCardAction");
        return t.action
          .retrievePaymentIntent({ intentSecret: n, hosted: !1 })
          .then(function (e) {
            var n = ds(e);
            switch (n.type) {
              case "error":
                return Le.resolve(cc(e));
              case "object":
                var r = n.object;
                if (pc(r.status)) {
                  if ("manual" !== r.confirmation_method)
                    throw new Ie(
                      "handleCardAction: The PaymentIntent supplied does not require manual server-side confirmation. Please use confirmCardPayment instead to complete the payment."
                    );
                  return hs(t, r, nc.card, n.locale, !1);
                }
                throw new Ie(
                  "handleCardAction: The PaymentIntent supplied is not in the requires_action state."
                );
              default:
                return Ne(n);
            }
          });
      },
      Hs =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Gs =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      Ws = function (e, t) {
        if (null == e) return ct(null);
        var n = e.type,
          r = he(e, ["type"]),
          o = gt(bt, function () {
            return null;
          })(n, jt(t, "type"));
        return "error" === o.type ? o : ct({ type: o.value, data: r });
      },
      Ys = function (e, t, n, r) {
        if (null === e) {
          if (null === t) {
            throw new Ie(
              n +
                ": you must additionally specify the type of payment method to create within " +
                (r ? "source_data" : "payment_method_data") +
                "."
            );
          }
          return t;
        }
        if (null === t) return e;
        if (t !== e)
          throw new Ie(
            n +
              ": you specified `type: " +
              t +
              "`, but " +
              n +
              " will create a " +
              e +
              " payment method."
          );
        return e;
      },
      zs = function (e) {
        return function (t, n) {
          if ("object" === (void 0 === t ? "undefined" : Gs(t)) && null !== t) {
            var r = t.source,
              o = t.source_data,
              i = t.payment_method,
              a = t.payment_method_data,
              c = he(t, [
                "source",
                "source_data",
                "payment_method",
                "payment_method_data",
              ]);
            if (null != r && "string" != typeof r)
              return ut(
                "string",
                void 0 === r ? "undefined" : Gs(r),
                jt(n, "source")
              );
            if (null != i && "string" != typeof i)
              return ut(
                "string",
                void 0 === i ? "undefined" : Gs(i),
                jt(n, "payment_method")
              );
            if (null != o && "object" !== (void 0 === o ? "undefined" : Gs(o)))
              return ut(
                "object",
                void 0 === o ? "undefined" : Gs(o),
                jt(n, "source_data")
              );
            if (null != a && "object" !== (void 0 === a ? "undefined" : Gs(a)))
              return ut(
                "object",
                void 0 === a ? "undefined" : Gs(a),
                jt(n, "payment_method_data")
              );
            var s = Ws(o, jt(n, "source_data"));
            if ("error" === s.type) return s;
            var u = s.value,
              l = Ws(a, jt(n, "payment_method_data"));
            if ("error" === l.type) return l;
            var p = l.value;
            return ct({
              sourceData: u,
              source: null == r ? null : r,
              paymentMethodData: p,
              paymentMethod: null == i ? null : i,
              otherParams: Hs({}, e, c),
            });
          }
          return null === t
            ? ut("object", "null", n)
            : ut("object", void 0 === t ? "undefined" : Gs(t), n);
        };
      },
      Ks = function (e) {
        return function (t, n) {
          if (void 0 === t)
            return ct({
              sourceData: null,
              paymentMethodData: null,
              source: null,
              paymentMethod: null,
              otherParams: {},
            });
          if ("object" !== (void 0 === t ? "undefined" : Gs(t)))
            return ut("object", void 0 === t ? "undefined" : Gs(t), n);
          if (null === t) return ut("object", "null", n);
          if (e) {
            if (!t.payment_intent)
              return ct({
                sourceData: null,
                paymentMethodData: null,
                source: null,
                paymentMethod: null,
                otherParams: t,
              });
            var r = t.payment_intent,
              o = he(t, ["payment_intent"]);
            return zs(o)(r, jt(n, "payment_intent"));
          }
          return t.payment_intent
            ? st(
                new Ie(
                  "The payment_intent parameter has been removed. To fix, move everything nested under the payment_intent parameter to the top-level object."
                )
              )
            : zs({})(t, n);
        };
      },
      Vs = function (e, t, n, r, o, i) {
        var a = Lt(ec, o, r);
        if ("error" === a.type) return null;
        var c = a.value,
          s = xt(Ks(t), i, r),
          u = s.value,
          l = u.sourceData,
          p = u.source,
          f = u.paymentMethodData,
          d = u.paymentMethod,
          _ = u.otherParams;
        if (!e && l)
          throw new Ie(r + ": Expected payment_method_data, not source_data.");
        if (null != p)
          throw new Ie(
            "When calling " +
              r +
              " on an Element, you can't pass in a pre-existing source ID, as a source will be created using the Element."
          );
        if (null != d)
          throw new Ie(
            "When calling " +
              r +
              " on an Element, you can't pass in a pre-existing PaymentMethod ID, as a PaymentMethod will be created using the Element."
          );
        var h = c._componentName,
          m = c._frame.id,
          y = l || f || { type: null, data: {} },
          v = y.type,
          b = y.data,
          g = ic(h, v),
          E = e && !f,
          w = Ys(n, g, r, E),
          S = { elementName: h, frameId: m, type: w, data: b };
        return E
          ? {
              confirmMode: Hs({ tag: "source-from-element" }, S),
              otherParams: _,
            }
          : {
              confirmMode: Hs(
                { tag: "paymentMethod-from-element", options: null },
                S
              ),
              otherParams: _,
            };
      },
      Js = function (e, t, n, r, o, i) {
        var a = xt(Ks(t), o, r),
          c = a.value,
          s = c.sourceData,
          u = c.source,
          l = c.paymentMethodData,
          p = c.paymentMethod,
          f = c.otherParams;
        if (!e && s)
          throw new Ie(
            r +
              ": Expected payment_method, source, or payment_method_data, not source_data."
          );
        if (null !== u && null !== s)
          throw new Ie(
            r + ": Expected either source or source_data, but not both."
          );
        if (null !== p && null !== l)
          throw new Ie(
            r +
              ": Expected either payment_method or payment_method_data, but not both."
          );
        if (null !== p && null !== u)
          throw new Ie(
            r + ": Expected either payment_method or source, but not both."
          );
        if (s || l) {
          var d = s || l || {},
            _ = d.type,
            h = d.data,
            m = e && !l,
            y = Ys(n, _, r, m);
          return m
            ? {
                confirmMode: { tag: "source-from-data", type: y, data: h },
                otherParams: f,
              }
            : {
                confirmMode: {
                  tag: "paymentMethod-from-data",
                  type: y,
                  data: h,
                  options: null,
                },
                otherParams: f,
              };
        }
        return null !== u
          ? { confirmMode: { tag: "source", source: u }, otherParams: f }
          : null !== p
          ? {
              confirmMode: {
                tag: "paymentMethod",
                paymentMethod: p,
                options: null,
              },
              otherParams: f,
            }
          : { confirmMode: { tag: "none" }, otherParams: f };
      },
      Xs = function (e, t, n, r) {
        return function (o, i) {
          var a = Vs(e, t, n, r, o, i);
          if (a) return a;
          var c = Js(e, t, n, r, o);
          if (c) return c;
          throw new Ie(
            "Expected: stripe." +
              r +
              "(intentSecret, element[, data]) or stripe." +
              r +
              "(intentSecret[, data]). Please see the docs for more usage examples https://stripe.com/docs/payments/dynamic-authentication"
          );
        };
      },
      Qs =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      $s = function (e, t, n, r, o, i) {
        var a = xt(hc, r, "stripe.confirmPaymentIntent intent secret"),
          c = a.value,
          s = Xs(e, !1, null, "confirmPaymentIntent")(o, i);
        return t.action
          .confirmPaymentIntent(
            Qs({}, s, {
              intentSecret: c,
              expectedType: null,
              options: { handleActions: !1 },
              mids: n,
            })
          )
          .then(cc);
      },
      Zs = function (e, t, n, r, o, i, a) {
        var c = xt(hc, o, "stripe.handleCardPayment intent secret"),
          s = c.value,
          u = nc.card,
          l = Xs(e, r, u, "handleCardPayment")(i, a),
          p = !i && !a;
        return t.action
          .confirmPaymentIntent(
            Qs({}, l, {
              intentSecret: s,
              expectedType: u,
              options: { handleActions: !0 },
              mids: n,
            })
          )
          .then(ms(t, u, p, !1));
      },
      eu = function (e, t, n, r, o, i) {
        var a = xt(hc, r, "stripe.handleSepaDebitPayment intent secret"),
          c = a.value,
          s = nc.sepa_debit,
          u = Xs(!1, n, s, "handleSepaDebitPayment")(o, i),
          l = !o && !i;
        return e.action
          .confirmPaymentIntent(
            Qs({}, u, {
              intentSecret: c,
              expectedType: s,
              options: { handleActions: !0 },
              mids: t,
            })
          )
          .then(ms(e, s, l, !1));
      },
      tu = function (e, t, n, r, o, i, a) {
        var c = xt(hc, o, "stripe.handleIdealPayment intent secret"),
          s = c.value,
          u = nc.ideal,
          l = Xs(e, r, u, "handleIdealPayment")(i, a),
          p = !i && !a;
        return t.action
          .confirmPaymentIntent(
            Qs({}, l, {
              intentSecret: s,
              expectedType: u,
              options: { handleActions: !0 },
              mids: n,
            })
          )
          .then(ms(t, u, p, !1));
      },
      nu = function (e, t, n, r, o, i) {
        var a = xt(hc, r, "stripe.handleFpxPayment intent secret"),
          c = a.value,
          s = nc.fpx,
          u = Xs(!1, n, s, "handleFpxPayment")(o, i),
          l = !o && !i;
        return e.action
          .confirmPaymentIntent(
            Qs({}, u, {
              intentSecret: c,
              expectedType: s,
              options: { handleActions: !0 },
              mids: t,
            })
          )
          .then(ms(e, s, l, !1));
      },
      ru = function (e, t, n, r, o) {
        var i = Uc(fc(t), n, e),
          a = lc(t);
        if (!i) return Le.resolve({ setupIntent: t });
        switch (i.type) {
          case "3ds1-modal":
            return Xc(i, a, zt.SETUP_INTENT, e, r);
          case "3ds2-fingerprint":
          case "3ds2-challenge":
            return rs(a, zt.SETUP_INTENT, i, e, r, o);
          case "redirect":
            return ps(0, n, i.redirectUrl, e);
          default:
            return Le.resolve({ setupIntent: t });
        }
      },
      ou = function (e, t, n, r, o) {
        return ru(e, t, n, r, o).then(function (e) {
          if (e.paymentIntent)
            throw new Error("Got unexpected PaymentIntent response");
          return e;
        });
      },
      iu = function (e, t, n, r) {
        return function (o) {
          switch (o.type) {
            case "error":
              var i = o.error,
                a = i.setup_intent;
              return n && a && "succeeded" === a.status
                ? Le.resolve({ setupIntent: a })
                : Le.resolve({ error: i });
            case "object":
              var c = o.object;
              return ou(e, c, t, o.locale, r);
            default:
              return Ne(o);
          }
        };
      },
      au =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      cu = function (e, t) {
        return function (n, r, o, i, a) {
          var c = xc(o, e),
            s = Dc(t, e, i),
            u = qc(e, a),
            l = "none" === s.confirmMode.tag,
            p = n.action.confirmSetupIntent(
              au({}, s, {
                intentSecret: c,
                expectedType: t,
                options: u,
                mids: r,
              })
            );
          return u.handleActions ? p.then(iu(n, t, l, !1)) : p.then(sc);
        };
      },
      su = cu("confirmAcssDebitSetup", nc.acss_debit),
      uu = cu("confirmCardSetup", nc.card),
      lu = cu("confirmSepaDebitSetup", nc.sepa_debit),
      pu = cu("confirmAuBecsDebitSetup", nc.au_becs_debit),
      fu = cu("confirmBacsDebitSetup", nc.bacs_debit),
      du = cu("confirmIdealSetup", nc.ideal),
      _u = cu("confirmAlipaySetup", nc.alipay),
      hu = cu("confirmSofortSetup", nc.sofort),
      mu = cu("confirmBancontactSetup", nc.bancontact),
      yu = function (e, t) {
        var n = xc(e, "retrieveSetupIntent");
        return t.action
          .retrieveSetupIntent({ intentSecret: n, hosted: !1 })
          .then(sc);
      },
      vu = function (e, t, n) {
        var r = xc(t, "verifyMicrodepositsForSetup"),
          o = xt(At, n, "stripe.verifyMicrodepositsForSetup");
        return e.action
          .verifyMicrodepositsForSetup({ intentSecret: r, data: o.value })
          .then(sc);
      },
      bu = function (e, t) {
        var n = xc(e, "handleHosted3DS2Setup [internal]");
        return t.action
          .retrieveSetupIntent({ intentSecret: n, hosted: !0 })
          .then(iu(t, nc.card, !1, !0));
      },
      gu =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Eu = function (e, t, n, r, o) {
        var i = xt(hc, n, "stripe.handleCardSetup intent secret"),
          a = i.value,
          c = nc.card,
          s = Xs(!1, !1, c, "handleCardSetup")(r, o),
          u = !r && !o;
        return e.action
          .confirmSetupIntent(
            gu({}, s, {
              intentSecret: a,
              expectedType: c,
              options: { handleActions: !0 },
              mids: t,
            })
          )
          .then(iu(e, c, u, !1));
      },
      wu = function (e, t, n, r, o) {
        var i = xt(hc, n, "stripe.handleSepaDebitSetup intent secret"),
          a = i.value,
          c = nc.sepa_debit,
          s = Xs(!1, !1, c, "handleSepaDebitSetup")(r, o),
          u = !r && !o;
        return e.action
          .confirmSetupIntent(
            gu({}, s, {
              intentSecret: a,
              expectedType: c,
              options: { handleActions: !0 },
              mids: t,
            })
          )
          .then(iu(e, c, u, !1));
      },
      Su = function (e, t, n, r, o) {
        var i = xt(hc, n, "stripe.confirmSetupIntent intent secret"),
          a = i.value,
          c = Xs(!1, !1, null, "confirmSetupIntent")(r, o);
        return e.action
          .confirmSetupIntent(
            gu({}, c, {
              otherParams: gu({}, c.otherParams),
              intentSecret: a,
              expectedType: null,
              options: { handleActions: !1 },
              mids: t,
            })
          )
          .then(sc);
      },
      Pu = [No.checkout_beta_2, No.checkout_beta_3, No.checkout_beta_4],
      Ou = [
        No.checkout_beta_2,
        No.checkout_beta_3,
        No.checkout_beta_4,
        No.checkout_beta_locales,
        No.checkout_beta_testcards,
      ],
      ku = {
        bg: "bg",
        cs: "cs",
        da: "da",
        de: "de",
        el: "el",
        en: "en",
        "en-GB": "en-GB",
        es: "es",
        "es-419": "es-419",
        et: "et",
        fi: "fi",
        fr: "fr",
        "fr-CA": "fr-CA",
        hu: "hu",
        id: "id",
        it: "it",
        ja: "ja",
        lt: "lt",
        lv: "lv",
        ms: "ms",
        mt: "mt",
        nb: "nb",
        nl: "nl",
        pl: "pl",
        pt: "pt",
        "pt-BR": "pt-BR",
        ro: "ro",
        ru: "ru",
        sk: "sk",
        sl: "sl",
        sv: "sv",
        tr: "tr",
        zh: "zh",
        "zh-HK": "zh-HK",
        "zh-TW": "zh-TW",
      },
      Au = { th: "th", "pt-PT": "pt-PT" },
      Tu = Object.keys(ku),
      Ru = Object.keys(Au),
      Iu =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Nu = {
        sku: pt(bt),
        plan: pt(bt),
        clientReferenceId: pt(bt),
        locale: pt(ht.apply(void 0, ["auto"].concat(ye(Tu)))),
        customerEmail: pt(bt),
        billingAddressCollection: pt(ht("required", "auto")),
        submitType: pt(ht("auto", "pay", "book", "donate")),
        allowIncompleteSubscriptions: pt(Et),
        shippingAddressCollection: pt(Mt({ allowedCountries: Tt(bt) })),
      },
      Mu = function (e, t, n) {
        if ((e && t) || ((e || t) && n))
          throw new Ie(
            "stripe.redirectToCheckout: Expected only one of sku, plan, or items."
          );
        if ("string" == typeof e) return [{ sku: e, quantity: 1 }];
        if ("string" == typeof t) return [{ plan: t, quantity: 1 }];
        if (n)
          return n.map(function (e) {
            return "sku" === e.type
              ? { sku: e.id, quantity: e.quantity }
              : { plan: e.id, quantity: e.quantity };
          });
        throw new Ie(
          "stripe.redirectToCheckout: You must provide either sku, plan, or items."
        );
      },
      Cu = function (e, t) {
        var n = Mt(
            Iu({}, Nu, {
              items: pt(
                ft(
                  Tt(Mt({ type: ht("plan"), quantity: St(0), id: bt })),
                  Tt(Mt({ type: ht("sku"), quantity: St(0), id: bt }))
                )
              ),
              successUrl: bt,
              cancelUrl: bt,
            })
          ),
          r = xt(n, t, "stripe.redirectToCheckout"),
          o = r.value,
          i = o.sku,
          a = o.plan,
          c = o.items,
          s = me(o, ["sku", "plan", "items"]),
          u = Mu(i, a, c);
        return Iu({ tag: "no-session", items: u }, s);
      },
      ju = function (e, t, n) {
        var r = Mt(
            Iu(
              {},
              Nu,
              {
                sessionId: pt(bt),
                successUrl: pt(bt),
                cancelUrl: pt(bt),
                mode: pt(ht("subscription", "payment")),
                items: pt(
                  ft(
                    Tt(Mt({ quantity: St(0), plan: bt })),
                    Tt(Mt({ quantity: St(0), sku: bt }))
                  )
                ),
                lineItems: pt(Tt(Mt({ quantity: St(0), price: bt }))),
              },
              -1 !== e.indexOf("checkout_beta_locales")
                ? {
                    locale: pt(
                      ht.apply(void 0, ["auto"].concat(ye(Tu), ye(Ru)))
                    ),
                  }
                : {}
            )
          ),
          o = xt(r, t, "stripe.redirectToCheckout"),
          i = o.value;
        if (i.sessionId) {
          var a = i.sessionId;
          if (Object.keys(i).length > 1)
            throw new Ie(
              "stripe.redirectToCheckout: Do not provide other parameters when providing sessionId. Specify all parameters on your server when creating the CheckoutSession."
            );
          if (!/^cs_/.test(a))
            throw new Ie(
              "stripe.redirectToCheckout: Invalid value for sessionId. You specified '" +
                a +
                "'."
            );
          if ("livemode" === n && /^cs_test_/.test(a))
            throw new Ie(
              "stripe.redirectToCheckout: the provided sessionId is for a test mode Checkout Session, whereas Stripe.js was initialized with a live mode publishable key."
            );
          if ("testmode" === n && /^cs_live_/.test(a))
            throw new Ie(
              "stripe.redirectToCheckout: the provided sessionId is for a live mode Checkout Session, whereas Stripe.js was initialized with a test mode publishable key."
            );
          return { tag: "session", sessionId: a };
        }
        var c = (i.sessionId, i.sku, i.plan, i.items),
          s = i.lineItems,
          u = i.successUrl,
          l = i.cancelUrl,
          p = i.mode,
          f = me(i, [
            "sessionId",
            "sku",
            "plan",
            "items",
            "lineItems",
            "successUrl",
            "cancelUrl",
            "mode",
          ]);
        if (!s && !c)
          throw new Ie(
            "stripe.redirectToCheckout: You must provide one of lineItems, items, or sessionId."
          );
        if (!u || !l)
          throw new Ie(
            "stripe.redirectToCheckout: You must provide successUrl and cancelUrl."
          );
        return Iu(
          {
            tag: "no-session",
            items: c,
            lineItems: s,
            successUrl: u,
            cancelUrl: l,
            mode: p,
          },
          f
        );
      },
      Lu = function (e, t, n) {
        var r = ju(e, t, n);
        if ("no-session" === r.tag) {
          var o = r.successUrl,
            i = r.cancelUrl;
          if (!tt(o))
            throw new Ie(
              "stripe.redirectToCheckout: successUrl must start with either http:// or https://."
            );
          if (!tt(i))
            throw new Ie(
              "stripe.redirectToCheckout: cancelUrl must start with either http:// or https://."
            );
          return r;
        }
        return r;
      },
      xu = function (e, t) {
        return "session" === t.tag ||
          null == e ||
          t.locale ||
          -1 === ["auto"].concat(ye(Tu)).indexOf(e)
          ? t
          : Iu({}, t, { locale: e });
      },
      qu = function (e, t, n) {
        var r = He(Pu, function (t) {
          return Co(e, t);
        });
        if (t && t.lineItems && r)
          throw new Ie("Prices cannot be used with " + r);
        switch (r) {
          case "checkout_beta_2":
            return Cu(0, t);
          case "checkout_beta_3":
            return ju(e, t, n);
          case "checkout_beta_4":
          default:
            return Lu(e, t, n);
        }
      },
      Du = function (e, t, n) {
        var r =
          arguments.length > 3 && void 0 !== arguments[3]
            ? arguments[3]
            : "unknown";
        return xu(t, qu(e, n, r));
      },
      Bu = Du,
      Fu =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Uu = function (e, t) {
        var n = function (t) {
          return us(e, "redirectToCheckout", t), { error: t.error };
        };
        return ss(t).then(n);
      },
      Hu = function (e, t, n, r) {
        return function (o) {
          e.report("redirect_to_checkout.options", {
            betas: t,
            options: o,
            globalLocale: r,
          });
          var i = Bu(t, r, o, e.livemode());
          if ("session" === i.tag) {
            var a = i,
              c = a.sessionId;
            return e.action
              .createPaymentPageWithSession({
                betas: t,
                mids: n(),
                sessionId: c,
              })
              .then(function (t) {
                if ("error" === t.type) return { error: t.error };
                var n = t.object.url;
                return Uu(e, n);
              });
          }
          var s = i,
            u = (s.tag, s.items),
            l = s.lineItems,
            p = s.mode,
            f = s.successUrl,
            d = s.cancelUrl,
            _ = s.clientReferenceId,
            h = s.customerEmail,
            m = s.billingAddressCollection,
            y = s.submitType,
            v = s.allowIncompleteSubscriptions,
            b = s.shippingAddressCollection,
            g = ve(s, [
              "tag",
              "items",
              "lineItems",
              "mode",
              "successUrl",
              "cancelUrl",
              "clientReferenceId",
              "customerEmail",
              "billingAddressCollection",
              "submitType",
              "allowIncompleteSubscriptions",
              "shippingAddressCollection",
            ]),
            E = [];
          if (l && u)
            throw new Error("Only one of items, lineItems can be passed in.");
          if (l) {
            if (!p) throw new Error("Expected `mode`");
            E = l.map(function (e) {
              if (e.price)
                return { type: "price", id: e.price, quantity: e.quantity };
              throw new Error("Unexpected item shape.");
            });
          } else {
            if (!u) throw new Error("An items field must be passed in.");
            E = u.map(function (e) {
              if (e.sku)
                return { type: "sku", id: e.sku, quantity: e.quantity };
              if (e.plan)
                return { type: "plan", id: e.plan, quantity: e.quantity };
              throw new Error("Unexpected item shape.");
            });
          }
          var w = He(Pu, function (e) {
            return Co(t, e);
          });
          return e.action
            .createPaymentPage(
              Fu(
                {
                  betas: t,
                  mids: n(),
                  items: E,
                  mode: p,
                  success_url: f,
                  cancel_url: d,
                  client_reference_id: _,
                  customer_email: h,
                  billing_address_collection: m,
                  submit_type: y,
                  use_payment_methods: !w,
                  allow_incomplete_subscriptions: v,
                  shipping_address_collection: b && {
                    allowed_countries: b.allowedCountries,
                  },
                },
                g
              )
            )
            .then(function (t) {
              if ("error" === t.type) return { error: t.error };
              var n = t.object.url;
              return Uu(e, n);
            });
        };
      },
      Gu =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      Wu = function (e) {
        switch (e.type) {
          case "object":
            return { token: e.object };
          case "error":
            return { error: e.error };
          default:
            return Ne(e);
        }
      },
      Yu = function (e) {
        return "object" === (void 0 === e ? "undefined" : Gu(e)) && null !== e
          ? e
          : {};
      },
      zu = function (e, t, n) {
        var r = tc(t);
        if (r && "cardCvc" === r._componentName) {
          var o = r._frame.id;
          return e.action.tokenizeCvcUpdate({ frameId: o, mids: n }).then(Wu);
        }
        throw new Ie(
          "You must provide a `cardCvc` Element to create a `cvc_update` token."
        );
      },
      Ku = function (e, t) {
        return function (n, r) {
          var o = tc(n);
          if (o) {
            var i = o._frame.id,
              a = o._componentName,
              c = Yu(r);
            return e.action
              .tokenizeWithElement({
                frameId: i,
                elementName: a,
                tokenData: c,
                mids: t,
              })
              .then(Wu);
          }
          if ("string" == typeof n) {
            var s = n,
              u = Yu(r);
            return e.action
              .tokenizeWithData({
                elementName: null,
                type: s,
                tokenData: u,
                mids: t,
              })
              .then(Wu);
          }
          throw new Ie(
            "You must provide a Stripe Element or a valid token type to create a Token."
          );
        };
      },
      Vu = function (e) {
        switch (e.type) {
          case "object":
            return { radarSession: e.object };
          case "error":
            return { error: e.error };
          default:
            return Ne(e);
        }
      },
      Ju = function (e, t) {
        return e.action.createRadarSession({ mids: t }).then(Vu);
      },
      Xu =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      Qu = (function () {
        function e(e, t) {
          for (var n = 0; n < t.length; n++) {
            var r = t[n];
            (r.enumerable = r.enumerable || !1),
              (r.configurable = !0),
              "value" in r && (r.writable = !0),
              Object.defineProperty(e, r.key, r);
          }
        }
        return function (t, n, r) {
          return n && e(t.prototype, n), r && e(t, r), t;
        };
      })(),
      $u = new Fe(),
      Zu = Ct({
        apiKey: bt,
        stripeAccount: pt(bt),
        locale: pt(bt),
        apiVersion: pt(bt),
        __privateApiUrl: pt(bt),
        __checkout: pt(Ct({ mids: Ct({ muid: bt, sid: bt }) })),
        __hosted3DS: pt(Et),
        canCreateRadarSession: pt(Et),
        betas: pt(Tt(mt.apply(void 0, ge(Mo)))),
      }),
      el = function (e) {
        return (
          "You have an in-flight " +
          e +
          "! Please be sure to disable your form submit button when " +
          e +
          " is called."
        );
      },
      tl = function (e) {
        return function () {
          throw new Ie(
            "You cannot call `stripe." +
              e +
              "` without supplying a PaymentIntents beta flag when initializing Stripe.js.    You can find more information including code snippets at https://www.stripe.com/docs/payments/payment-intents/quickstart."
          );
        };
      },
      nl = (function () {
        function e(t, n) {
          var r = this;
          be(this, e), rl.call(this);
          var o = xt(Zu, t || {}, "Stripe()"),
            i = o.value,
            a = o.warnings,
            c = i.apiKey,
            s = i.stripeAccount,
            u = i.apiVersion,
            l = i.locale,
            p = i.__privateApiUrl,
            f = i.__checkout,
            d = i.__hosted3DS,
            _ = i.canCreateRadarSession,
            h = i.betas;
          if ("" === c)
            throw new Ie(
              "Please call Stripe() with your publishable key. You used an empty string."
            );
          if (0 === c.indexOf("sk_"))
            throw new Ie(
              "You should not use your secret key with Stripe.js.\n        Please pass a publishable key instead."
            );
          f && f.mids && (e._ec = io({ checkoutIds: f.mids })),
            (this._apiKey = c.trim()),
            (this._keyMode = $e(this._apiKey)),
            (this._betas = h || []),
            (this._locale = Oa(l, this._betas) || null),
            (this._stripeAccount = s || null),
            (this._isCheckout = !!f),
            (this._controller = new To(
              Xu(
                {
                  apiKey: this._apiKey,
                  apiVersion: u,
                  __privateApiUrl: p,
                  stripeAccount: s,
                  betas: this._betas,
                  stripeJsId: e.stripeJsId,
                  startTimestamp: $u,
                  listenerRegistry: this._listenerRegistry,
                },
                this._locale ? { locale: this._locale } : {}
              )
            )),
            a.forEach(function (e) {
              return r._controller.warn(e);
            }),
            this._ensureHTTPS(),
            this._ensureStripeHosted(n),
            this._attachPaymentIntentMethods(this._betas, !!d),
            this._attachLegacyPaymentIntentMethods(this._betas),
            this._attachCheckoutMethods(this._betas),
            this._attachPrivateMethodsForCheckout(this._isCheckout),
            this._attachCreateRadarSession(_ || !1),
            this._attachGetters();
        }
        return (
          Qu(e, [
            {
              key: "_attachCreateRadarSession",
              value: function (e) {
                var t = this;
                e &&
                  (this.createRadarSession = En(function () {
                    var e = t._mids();
                    return Ju(t._controller, e);
                  }));
              },
            },
            {
              key: "_attachPaymentIntentMethods",
              value: function (e, t) {
                var n = this,
                  r = function () {
                    return n._mids();
                  };
                (this.createPaymentMethod = Pn(function () {
                  for (
                    var e = arguments.length, t = Array(e), o = 0;
                    o < e;
                    o++
                  )
                    t[o] = arguments[o];
                  return jc.apply(void 0, [n._controller, r()].concat(t));
                })),
                  (this._createPaymentMethod = this.createPaymentMethod),
                  (this.retrievePaymentIntent = wn(function (e) {
                    return Ds(e, n._controller);
                  })),
                  (this.retrieveSetupIntent = wn(function (e) {
                    return yu(e, n._controller);
                  }));
                var o = rr(Us, el("handleCardAction"));
                this.handleCardAction = wn(function (e) {
                  return o(e, n._controller);
                });
                var i = rr(Os, el("confirmCardPayment"));
                this.confirmCardPayment = Pn(function () {
                  for (
                    var e = arguments.length, t = Array(e), o = 0;
                    o < e;
                    o++
                  )
                    t[o] = arguments[o];
                  return i.apply(void 0, [n._controller, r()].concat(t));
                });
                var a = rr(uu, el("confirmCardSetup"));
                (this.confirmCardSetup = Pn(function () {
                  for (
                    var e = arguments.length, t = Array(e), o = 0;
                    o < e;
                    o++
                  )
                    t[o] = arguments[o];
                  return a.apply(void 0, [n._controller, r()].concat(t));
                })),
                  (this.confirmIdealPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Is.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmSepaDebitPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return js.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmSepaDebitSetup = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return lu.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmFpxPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return As.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmAlipayPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Ms.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmAlipaySetup = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return _u.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmAuBecsDebitPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Es.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmAuBecsDebitSetup = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return pu.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmBacsDebitPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return ws.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmBacsDebitSetup = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return fu.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmBancontactPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Ss.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmEpsPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return ks.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmGiropayPayment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Ts.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  (this.confirmP24Payment = Pn(function () {
                    for (
                      var e = arguments.length, t = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      t[o] = arguments[o];
                    return Cs.apply(void 0, [n._controller, r()].concat(t));
                  })),
                  Co(this._betas, No.acss_debit_beta_1) &&
                    ((this.confirmAcssDebitPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return bs.apply(void 0, [n._controller, r()].concat(t));
                    })),
                    (this.confirmAcssDebitSetup = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return su.apply(void 0, [n._controller, r()].concat(t));
                    })),
                    (this.verifyMicrodepositsForPayment = Sn(function () {
                      for (
                        var e = arguments.length, t = Array(e), r = 0;
                        r < e;
                        r++
                      )
                        t[r] = arguments[r];
                      return Bs.apply(void 0, [n._controller].concat(t));
                    })),
                    (this.verifyMicrodepositsForSetup = Sn(function () {
                      for (
                        var e = arguments.length, t = Array(e), r = 0;
                        r < e;
                        r++
                      )
                        t[r] = arguments[r];
                      return vu.apply(void 0, [n._controller].concat(t));
                    }))),
                  (this.confirmGrabPayPayment = tl("confirmGrabPayPayment")),
                  Co(this._betas, No.grabpay_pm_beta_1) &&
                    (this.confirmGrabPayPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return Rs.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmBoletoPilotPayment = tl(
                    "confirmBoletoPilotPayment"
                  )),
                  Co(this._betas, No.boleto_pilot_pm_beta_1) &&
                    (this.confirmBoletoPilotPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return Ps.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmOxxoPayment = tl("confirmOxxoPayment")),
                  Co(this._betas, No.oxxo_pm_beta_1) &&
                    (this.confirmOxxoPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return Ns.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmWechatPayPayment = tl(
                    "confirmWechatPayPayment"
                  )),
                  Co(this._betas, No.wechat_pay_pm_beta_1) &&
                    (this.confirmWechatPayPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return qs.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmSofortPayment = tl("confirmSofortPayment")),
                  Co(this._betas, No.sofort_pm_beta_1) &&
                    (this.confirmSofortPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return Ls.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmIdealSetup = tl("confirmIdealSetup")),
                  Co(this._betas, No.ideal_sepa_beta_1) &&
                    (this.confirmIdealSetup = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return du.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmSofortSetup = tl("confirmSofortSetup")),
                  Co(this._betas, No.sofort_sepa_beta_1) &&
                    (this.confirmSofortSetup = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return hu.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmBancontactSetup = tl("confirmBancontactSetup")),
                  Co(this._betas, No.bancontact_sepa_beta_1) &&
                    (this.confirmBancontactSetup = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return mu.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmAfterpayClearpayPayment = tl(
                    "confirmAfterpayClearpayPayment"
                  )),
                  Co(this._betas, No.afterpay_clearpay_pm_beta_1) &&
                    (this.confirmAfterpayClearpayPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return gs.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  (this.confirmUpiPayment = tl("confirmUpiPayment")),
                  Co(this._betas, No.upi_beta_1) &&
                    (this.confirmUpiPayment = Pn(function () {
                      for (
                        var e = arguments.length, t = Array(e), o = 0;
                        o < e;
                        o++
                      )
                        t[o] = arguments[o];
                      return xs.apply(void 0, [n._controller, r()].concat(t));
                    })),
                  t &&
                    ((this.handleHosted3DS2Payment = wn(function (e) {
                      return Fs(e, n._controller);
                    })),
                    (this.handleHosted3DS2Setup = wn(function (e) {
                      return bu(e, n._controller);
                    })));
              },
            },
            {
              key: "_attachLegacyPaymentIntentMethods",
              value: function (e) {
                var t = this,
                  n =
                    Co(this._betas, No.payment_intent_beta_1) ||
                    Co(this._betas, No.payment_intent_beta_2),
                  r = function () {
                    return t._mids();
                  },
                  o = Pn(function () {
                    for (
                      var e = arguments.length, n = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      n[o] = arguments[o];
                    return $s.apply(void 0, [!0, t._controller, r()].concat(n));
                  }),
                  i = Pn(function () {
                    for (
                      var e = arguments.length, n = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      n[o] = arguments[o];
                    return $s.apply(void 0, [!1, t._controller, r()].concat(n));
                  }),
                  a = rr(Zs, el("handleCardPayment")),
                  c = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return a.apply(
                      void 0,
                      [!0, t._controller, r(), n].concat(o)
                    );
                  }),
                  s = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return a.apply(
                      void 0,
                      [!1, t._controller, r(), n].concat(o)
                    );
                  }),
                  u = rr(Eu, el("handleCardSetup")),
                  l = Pn(function () {
                    for (
                      var e = arguments.length, n = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      n[o] = arguments[o];
                    return u.apply(void 0, [t._controller, r()].concat(n));
                  }),
                  p = Pn(function () {
                    for (
                      var e = arguments.length, n = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      n[o] = arguments[o];
                    return Su.apply(void 0, [t._controller, r()].concat(n));
                  }),
                  f = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return eu.apply(void 0, [t._controller, r(), n].concat(o));
                  }),
                  d = Pn(function () {
                    for (
                      var e = arguments.length, n = Array(e), o = 0;
                      o < e;
                      o++
                    )
                      n[o] = arguments[o];
                    return wu.apply(void 0, [t._controller, r()].concat(n));
                  }),
                  _ = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return tu.apply(
                      void 0,
                      [!0, t._controller, r(), n].concat(o)
                    );
                  }),
                  h = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return tu.apply(
                      void 0,
                      [!1, t._controller, r(), n].concat(o)
                    );
                  }),
                  m = Pn(function () {
                    for (
                      var e = arguments.length, o = Array(e), i = 0;
                      i < e;
                      i++
                    )
                      o[i] = arguments[i];
                    return nu.apply(void 0, [t._controller, r(), n].concat(o));
                  });
                (this.handleCardPayment = s),
                  (this.confirmPaymentIntent = i),
                  (this.handleCardSetup = l),
                  (this.confirmSetupIntent = p),
                  (this.fulfillPaymentIntent = tl("fulfillPaymentIntent")),
                  (this.handleSepaDebitPayment = tl("handleSepaDebitPayment")),
                  (this.handleSepaDebitSetup = tl("handleSepaDebitSetup")),
                  (this.handleIdealPayment = tl("handleIdealPayment")),
                  (this.handleFpxPayment = tl("handleFpxPayment")),
                  Co(this._betas, No.payment_intent_beta_1)
                    ? (this.fulfillPaymentIntent = c)
                    : (Co(this._betas, No.payment_intent_beta_3) ||
                        Co(this._betas, No.payment_intent_beta_2)) &&
                      (this.handleCardPayment = c),
                  Co(this._betas, No.payment_intent_beta_3) &&
                    ((this.confirmPaymentIntent = o),
                    (this.handleIdealPayment = _),
                    (this.handleSepaDebitPayment = f)),
                  Co(this._betas, No.fpx_bank_beta_1) &&
                    (this.handleFpxPayment = m),
                  Co(this._betas, No.ideal_pm_beta_1) &&
                    (this.handleIdealPayment = h),
                  Co(this._betas, No.sepa_pm_beta_1) &&
                    ((this.handleSepaDebitPayment = f),
                    (this.handleSepaDebitSetup = d));
              },
            },
            {
              key: "_attachPrivateMethodsForCheckout",
              value: function (e) {
                var t = this;
                e &&
                  ((this.sendInteractionEvent = so),
                  (this.tryNextAction = Sn(function (e, n) {
                    var r = xt(mc, e, "Payment Intent"),
                      o = r.value,
                      i = Object.keys(nc).map(function (e) {
                        return nc[e];
                      }),
                      a = xt(ht.apply(void 0, ge(i)), n, "Source type"),
                      c = a.value;
                    return "payment_intent" === o.object
                      ? hs(t._controller, o, c, "auto", !1)
                      : ou(t._controller, o, c, "auto", !1);
                  })));
              },
            },
            {
              key: "_attachCheckoutMethods",
              value: function (e) {
                var t = this,
                  n = function () {
                    return t._mids();
                  },
                  r = e.reduce(function (e, t) {
                    var n = He(Ou, function (e) {
                      return e === t;
                    });
                    return n ? [].concat(ge(e), [n]) : e;
                  }, []);
                this.redirectToCheckout = Hu(
                  this._controller,
                  r,
                  n,
                  this._locale
                );
              },
            },
            {
              key: "_attachGetters",
              value: function () {
                var e = this,
                  t = [
                    "elements",
                    "createToken",
                    "createSource",
                    "createPaymentMethod",
                  ],
                  n = new Oc(function (t) {
                    e._registerWrapper({ name: t, version: null });
                  });
                t.forEach(function (t) {
                  if (e.hasOwnProperty(t)) {
                    var r = e[t],
                      o = function () {
                        n.called(t);
                        for (
                          var e = arguments.length, o = Array(e), i = 0;
                          i < e;
                          i++
                        )
                          o[i] = arguments[i];
                        return r.apply(this, o);
                      };
                    Object.defineProperty(e, t, {
                      enumerable: !0,
                      get: function () {
                        return n.got(t), o;
                      },
                    });
                  }
                });
              },
            },
            {
              key: "_ensureHTTPS",
              value: function () {
                var e = window.location.protocol,
                  t =
                    -1 !==
                    [
                      "https:",
                      "file:",
                      "ionic:",
                      "chrome-extension:",
                      "moz-extension:",
                    ].indexOf(e),
                  n =
                    -1 !==
                    ["localhost", "127.0.0.1", "0.0.0.0"].indexOf(
                      window.location.hostname
                    ),
                  r = this._keyMode === Qe.live,
                  o =
                    "Live Stripe.js integrations must use HTTPS. For more information: https://stripe.com/docs/security#tls";
                if (!t) {
                  if (r && !n)
                    throw (
                      (this._controller.report("user_error.non_https_error", {
                        protocol: e,
                      }),
                      new Ie(o))
                    );
                  !r || n
                    ? window.console &&
                      console.warn(
                        "You may test your Stripe.js integration over HTTP. However, live Stripe.js integrations must use HTTPS."
                      )
                    : window.console && console.warn(o);
                }
              },
            },
            {
              key: "_ensureStripeHosted",
              value: function (e) {
                if (!e)
                  throw (
                    (this._controller.report("user_error.self_hosted"),
                    new Ie(
                      "Stripe.js must be loaded from js.stripe.com. For more information https://stripe.com/docs/stripe-js/reference#including-stripejs"
                    ))
                  );
              },
            },
            {
              key: "_mids",
              value: function () {
                return e._ec ? e._ec.ids() : null;
              },
            },
            {
              key: "_registerWrapper",
              value: function (e) {
                var t = Lt(Ec, e, "WrapperLibrary");
                if ("error" === t.type)
                  return void this._controller.report(
                    "register_wrapper.error",
                    { error: t.error.message }
                  );
                var n = t.value,
                  r = n.name,
                  o = n.version;
                this._controller.registerWrapper({ name: r, version: o });
              },
            },
          ]),
          e
        );
      })();
    (nl.version = 3),
      (nl.stripeJsId = rn()),
      (nl._ec = (function () {
        return "https://checkout.stripe.com/".match(
          new RegExp(document.location.protocol + "//" + document.location.host)
        )
          ? null
          : io();
      })());
    var rl = function () {
        var e = this;
        (this._listenerRegistry = Jr()),
          (this.elements = wn(function (t) {
            return new Xa(
              e._controller,
              e._listenerRegistry,
              Xu({}, e._locale ? { locale: e._locale } : {}, t, {
                betas: e._betas,
              })
            );
          })),
          (this.createToken = Sn(function (t, n) {
            var r = e._mids();
            if ("cvc_update" === t) {
              if (Co(e._betas, No.cvc_update_beta_1))
                return zu(e._controller, n, r);
              throw new Ie(
                "You cannot create a 'cvc_update' token without using the 'cvc_update_beta_1' beta flag."
              );
            }
            return Ku(e._controller, r)(t, n);
          })),
          (this.createSource = Sn(function (t, n) {
            var r = tc(t),
              o = Ac(r ? n : t),
              i = o || { type: null, data: {} },
              a = i.type,
              c = i.data;
            if (r) {
              var s = r._frame.id,
                u = r._componentName;
              return !o && oc(u)
                ? Le.reject(
                    new Ie(
                      "Please provide Source creation parameters to createSource."
                    )
                  )
                : e._controller.action
                    .createSourceWithElement({
                      frameId: s,
                      elementName: u,
                      type: a,
                      sourceData: c,
                      mids: e._mids(),
                    })
                    .then(Tc);
            }
            return o
              ? a
                ? e._controller.action
                    .createSourceWithData({
                      elementName: null,
                      type: a,
                      sourceData: c,
                      mids: e._mids(),
                    })
                    .then(Tc)
                : Le.reject(
                    new Ie("Please provide a source type to createSource.")
                  )
              : Le.reject(
                  new Ie(
                    "Please provide either an Element or Source creation parameters to createSource."
                  )
                );
          })),
          (this.retrieveSource = wn(function (t) {
            var n = xt(Ic, { source: t }, "retrieveSource"),
              r = n.value;
            return (
              n.warnings.forEach(function (t) {
                return e._controller.warn(t);
              }),
              e._controller.action.retrieveSource(r).then(Tc)
            );
          })),
          (this.paymentRequest = Sn(function (t, n) {
            Ze(e._keyMode);
            var r = e._isCheckout && n ? n : null;
            return $a(
              e._controller,
              { apiKey: e._apiKey, accountId: e._stripeAccount },
              e._mids(),
              t,
              e._betas,
              r,
              e._listenerRegistry
            );
          }));
      },
      ol = nl,
      il =
        "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e &&
                "function" == typeof Symbol &&
                e.constructor === Symbol &&
                e !== Symbol.prototype
                ? "symbol"
                : typeof e;
            },
      al =
        Object.assign ||
        function (e) {
          for (var t = 1; t < arguments.length; t++) {
            var n = arguments[t];
            for (var r in n)
              Object.prototype.hasOwnProperty.call(n, r) && (e[r] = n[r]);
          }
          return e;
        },
      cl = (function () {
        if (document.currentScript) {
          var e = nt(document.currentScript.src);
          return !e || Rr(e.origin);
        }
        return !0;
      })(),
      sl = function (e, t) {
        return new ol(
          al(
            { apiKey: e },
            t && "object" === (void 0 === t ? "undefined" : il(t)) ? t : {}
          ),
          cl
        );
      };
    (sl.version = ol.version),
      window.Stripe && 2 === window.Stripe.version && !window.Stripe.StripeV3
        ? (window.Stripe.StripeV3 = sl)
        : window.Stripe
        ? window.console &&
          console.warn(
            "It looks like Stripe.js was loaded more than one time. Please only load it once per page."
          )
        : (window.Stripe = sl);
    t.default = sl;
  },
  function (e, t, n) {
    "use strict";
    function r(e) {
      var t = new o(o._61);
      return (t._81 = 1), (t._65 = e), t;
    }
    var o = n(3);
    e.exports = o;
    var i = r(!0),
      a = r(!1),
      c = r(null),
      s = r(void 0),
      u = r(0),
      l = r("");
    (o.resolve = function (e) {
      if (e instanceof o) return e;
      if (null === e) return c;
      if (void 0 === e) return s;
      if (!0 === e) return i;
      if (!1 === e) return a;
      if (0 === e) return u;
      if ("" === e) return l;
      if ("object" == typeof e || "function" == typeof e)
        try {
          var t = e.then;
          if ("function" == typeof t) return new o(t.bind(e));
        } catch (e) {
          return new o(function (t, n) {
            n(e);
          });
        }
      return r(e);
    }),
      (o.all = function (e) {
        var t = Array.prototype.slice.call(e);
        return new o(function (e, n) {
          function r(a, c) {
            if (c && ("object" == typeof c || "function" == typeof c)) {
              if (c instanceof o && c.then === o.prototype.then) {
                for (; 3 === c._81; ) c = c._65;
                return 1 === c._81
                  ? r(a, c._65)
                  : (2 === c._81 && n(c._65),
                    void c.then(function (e) {
                      r(a, e);
                    }, n));
              }
              var s = c.then;
              if ("function" == typeof s) {
                return void new o(s.bind(c)).then(function (e) {
                  r(a, e);
                }, n);
              }
            }
            (t[a] = c), 0 == --i && e(t);
          }
          if (0 === t.length) return e([]);
          for (var i = t.length, a = 0; a < t.length; a++) r(a, t[a]);
        });
      }),
      (o.reject = function (e) {
        return new o(function (t, n) {
          n(e);
        });
      }),
      (o.race = function (e) {
        return new o(function (t, n) {
          e.forEach(function (e) {
            o.resolve(e).then(t, n);
          });
        });
      }),
      (o.prototype.catch = function (e) {
        return this.then(null, e);
      });
  },
  function (e, t, n) {
    "use strict";
    function r() {}
    function o(e) {
      try {
        return e.then;
      } catch (e) {
        return (y = e), v;
      }
    }
    function i(e, t) {
      try {
        return e(t);
      } catch (e) {
        return (y = e), v;
      }
    }
    function a(e, t, n) {
      try {
        e(t, n);
      } catch (e) {
        return (y = e), v;
      }
    }
    function c(e) {
      if ("object" != typeof this)
        throw new TypeError("Promises must be constructed via new");
      if ("function" != typeof e) throw new TypeError("not a function");
      (this._45 = 0),
        (this._81 = 0),
        (this._65 = null),
        (this._54 = null),
        e !== r && h(e, this);
    }
    function s(e, t, n) {
      return new e.constructor(function (o, i) {
        var a = new c(r);
        a.then(o, i), u(e, new _(t, n, a));
      });
    }
    function u(e, t) {
      for (; 3 === e._81; ) e = e._65;
      if ((c._10 && c._10(e), 0 === e._81))
        return 0 === e._45
          ? ((e._45 = 1), void (e._54 = t))
          : 1 === e._45
          ? ((e._45 = 2), void (e._54 = [e._54, t]))
          : void e._54.push(t);
      l(e, t);
    }
    function l(e, t) {
      m(function () {
        var n = 1 === e._81 ? t.onFulfilled : t.onRejected;
        if (null === n)
          return void (1 === e._81 ? p(t.promise, e._65) : f(t.promise, e._65));
        var r = i(n, e._65);
        r === v ? f(t.promise, y) : p(t.promise, r);
      });
    }
    function p(e, t) {
      if (t === e)
        return f(e, new TypeError("A promise cannot be resolved with itself."));
      if (t && ("object" == typeof t || "function" == typeof t)) {
        var n = o(t);
        if (n === v) return f(e, y);
        if (n === e.then && t instanceof c)
          return (e._81 = 3), (e._65 = t), void d(e);
        if ("function" == typeof n) return void h(n.bind(t), e);
      }
      (e._81 = 1), (e._65 = t), d(e);
    }
    function f(e, t) {
      (e._81 = 2), (e._65 = t), c._97 && c._97(e, t), d(e);
    }
    function d(e) {
      if ((1 === e._45 && (u(e, e._54), (e._54 = null)), 2 === e._45)) {
        for (var t = 0; t < e._54.length; t++) u(e, e._54[t]);
        e._54 = null;
      }
    }
    function _(e, t, n) {
      (this.onFulfilled = "function" == typeof e ? e : null),
        (this.onRejected = "function" == typeof t ? t : null),
        (this.promise = n);
    }
    function h(e, t) {
      var n = !1,
        r = a(
          e,
          function (e) {
            n || ((n = !0), p(t, e));
          },
          function (e) {
            n || ((n = !0), f(t, e));
          }
        );
      n || r !== v || ((n = !0), f(t, y));
    }
    var m = n(4),
      y = null,
      v = {};
    (e.exports = c),
      (c._10 = null),
      (c._97 = null),
      (c._61 = r),
      (c.prototype.then = function (e, t) {
        if (this.constructor !== c) return s(this, e, t);
        var n = new c(r);
        return u(this, new _(e, t, n)), n;
      });
  },
  function (e, t, n) {
    "use strict";
    (function (t) {
      function n(e) {
        a.length || (i(), (c = !0)), (a[a.length] = e);
      }
      function r() {
        for (; s < a.length; ) {
          var e = s;
          if (((s += 1), a[e].call(), s > u)) {
            for (var t = 0, n = a.length - s; t < n; t++) a[t] = a[t + s];
            (a.length -= s), (s = 0);
          }
        }
        (a.length = 0), (s = 0), (c = !1);
      }
      function o(e) {
        return function () {
          function t() {
            clearTimeout(n), clearInterval(r), e();
          }
          var n = setTimeout(t, 0),
            r = setInterval(t, 50);
        };
      }
      e.exports = n;
      var i,
        a = [],
        c = !1,
        s = 0,
        u = 1024,
        l = void 0 !== t ? t : self,
        p = l.MutationObserver || l.WebKitMutationObserver;
      (i =
        "function" == typeof p
          ? (function (e) {
              var t = 1,
                n = new p(e),
                r = document.createTextNode("");
              return (
                n.observe(r, { characterData: !0 }),
                function () {
                  (t = -t), (r.data = t);
                }
              );
            })(r)
          : o(r)),
        (n.requestFlush = i),
        (n.makeRequestCallFromTimer = o);
    }.call(t, n(5)));
  },
  function (e, t) {
    var n;
    n = (function () {
      return this;
    })();
    try {
      n = n || Function("return this")() || (0, eval)("this");
    } catch (e) {
      "object" == typeof window && (n = window);
    }
    e.exports = n;
  },
  function (e, t, n) {
    var r, o;
    !(function () {
      "use strict";
      var n = (function () {
        function e() {}
        function t(e, t) {
          for (var n = t.length, r = 0; r < n; ++r) i(e, t[r]);
        }
        function n(e, t) {
          e[t] = !0;
        }
        function r(e, t) {
          for (var n in t) c.call(t, n) && (e[n] = !!t[n]);
        }
        function o(e, t) {
          for (var n = t.split(s), r = n.length, o = 0; o < r; ++o)
            e[n[o]] = !0;
        }
        function i(e, i) {
          if (i) {
            var a = typeof i;
            "string" === a
              ? o(e, i)
              : Array.isArray(i)
              ? t(e, i)
              : "object" === a
              ? r(e, i)
              : "number" === a && n(e, i);
          }
        }
        function a() {
          for (var n = arguments.length, r = Array(n), o = 0; o < n; o++)
            r[o] = arguments[o];
          var i = new e();
          t(i, r);
          var a = [];
          for (var c in i) i[c] && a.push(c);
          return a.join(" ");
        }
        e.prototype = Object.create(null);
        var c = {}.hasOwnProperty,
          s = /\s+/;
        return a;
      })();
      void 0 !== e && e.exports
        ? (e.exports = n)
        : ((r = []),
          void 0 !==
            (o = function () {
              return n;
            }.apply(t, r)) && (e.exports = o));
    })();
  },
  function (e, t) {},
  function (e, t) {
    var n = function (e) {
      return (
        "_" +
        e
          .split("")
          .map(function (e) {
            return e.charCodeAt(0);
          })
          .reduce(function (e, t) {
            return ((e << 5) - e + t) & ((e << 5) - e + t);
          }, 0)
          .toString()
          .replace(/[-.]/g, "_")
      );
    };
    e.exports = n;
  },
]);
