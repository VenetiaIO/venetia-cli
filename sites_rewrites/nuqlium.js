var nq = new nqClass();
nq.nqDateTimeStamp = "17/02/2021 11:23:43";
nq.nqTriggered = false;
nq.nqIncludeJquery = false;
try {
    if (!window.jQuery) {
        nq.nqIncludeJquery = true
    }
} catch (err) {}
if (nq.nqIncludeJquery === true) {
    (function() {
        var a = document.createElement("SCRIPT");
        a.src = "https://code.jquery.com/jquery-3.3.1.min.js";
        a.type = "text/javascript";
        a.onload = function() {
            var b = window.jQuery;
            nqStart(nq)
        }
        ;
        document.getElementsByTagName("head")[0].appendChild(a)
    }
    )()
} else {
    nqStart(nq)
}
function nqStart(a) {
    var b = null;
    if (!!window.performance && window.performance.navigation.type === 2) {
        b = "1";
        a.nqLog("Back Button - Condition A (window.performance.navigation)")
    }
    window.onload = function() {
        a.nqTriggered = true;
        a.nqLog("Back Button - Condition B (onload - no action taken) ");
        setTimeout(function() {
            a.nqTriggered = false
        }, 100)
    }
    ;
    window.addEventListener("popstate", function() {
        if (!a.nqTriggered) {
            a.nqStartNuqlium("2");
            a.nqLog("Back Button - Condition C (no onload, then popstate) ")
        }
    });
    $(window).bind("pageshow", function(c) {
        if (c.originalEvent.persisted) {
            a.nqTriggered = true;
            setTimeout(function() {
                a.nqTriggered = false
            }, 100);
            a.nqLog("Back Button - Condition D (pageshow) ")
        }
    });
    a.nqSettings = {
        nqClient: "dfd62026-1477-48b5-ac33-d04ec326968b",
        nqApiUrl: "https://api-e03.nuqlium.com/api/2.0/",
        nqFailoverUrl: "https://api-f02.nuqlium.com/api/2.0/",
        nqPluginsUrl: "https://plugins.nuqlium.com/api/2.0/",
        nqStagingUrl: "https://staging-api-e03.nuqlium.com/api/2.0/",
        nqCSS: "https://api-e03.nuqlium.com/api/2.0/stylesheet.css?channel=dfd62026-1477-48b5-ac33-d04ec326968b&version=637523120881030000",
        nqUniversal: "",
        nqPredictiveInput: "#nuqlium-predictive-element",
        nqSearchId: "#nuqlium-container",
        nqNoRecentSearches: "No recent searches",
        nqPredictivePrevMax: 5,
        nqQueryStrings: "",
        nqColumns: 0,
        nqPaging: "paging",
        nqDynamicFiltering: false,
        nqFilterFavourites: false,
        nqBreakPoints: null,
        nqDataIndexes: [{
            Index: 100029,
            QueryStrings: "sessionid,src,sessionID",
            PredictiveInput: "#nq-searchINPUT",
            DefaultPaging: "paging",
            SearchUrl: "/page/search/?term={0}&nq.params",
            BreakPoints: [{
                MinWidth: 0,
                MaxWidth: 340,
                DefaultColumns: 2,
                AllowedColumns: "1,2"
            }, {
                MinWidth: 341,
                MaxWidth: 768,
                DefaultColumns: 2,
                AllowedColumns: "2,4"
            }, {
                MinWidth: 769,
                MaxWidth: 1440,
                DefaultColumns: 4,
                AllowedColumns: "4,5"
            }, {
                MinWidth: 1441,
                MaxWidth: 9999,
                DefaultColumns: 5,
                AllowedColumns: "4,5"
            }],
            DynamicPlacements: [{
                DataIndex: 100029,
                Key: "zone",
                Value: "nsr-categories-mens"
            }, {
                DataIndex: 100029,
                Key: "zone",
                Value: "nsr-categories-womens"
            }, {
                DataIndex: 100029,
                Key: "zone",
                Value: "nsr-categories-kids"
            }]
        }],
        nqDynamicPlacements: {},
        nqCookieDomain: document.domain,
        nqPredictiveTimeout: 300,
        nqInstance: 0
    };
    a.nqSendSources = true;
    a.nqDebug = a.nqIsDebug("nqxray");
    a.nqPerf = a.nqIsDebug("nqperformance");
    a.nqGetDataIndexSettings();
    a.nqAddDynamicPlacements();
    a.nqColumns = a.nqGetColumns();
    a.nqVariation = null;
    a.nqCampaign = null;
    a.nqAllowedKeys = ["search", "category", "feed", "set", "predictive", "recommendations", "product", "basket", "purchase", "group", "zone", "pages", "inset", "page", "elements"];
    a.nqLastAction = "";
    a.nqLastActionValue = "";
    a.nqPaging = a.nqSettings.nqPaging;
    a.nqActions = {};
    a.nqInit();
    a.nqLastManifest = null;
    a.nqLastTracking = null;
    a.nqLastUserFilters = null;
    a.nqInternals = {
        nqDidScroll: false,
        nqWindowHeight: $(window).height(),
        nqWindowWidth: $(window).width(),
        nqWindowBuffer: 200,
        nqInterval: null,
        nqIsRequesting: false
    };
    a.nqStartNuqlium(b);
    $(window).resize(function() {
        if (a.nqInternals.nqWindowWidth !== $(window).width()) {
            a.nqCheckResize();
            a.nqInternals.nqWindowWidth = $(window).width()
        }
    })
}
function nqClass(a) {
    this.nqInit = function() {
        if (nq.nqSettings.nqCSS !== "") {
            nq.nqSettings.nqCSS = nq.nqCheckDataIndex(nq.nqSettings.nqCSS, nq.nqDataIndex);
            loadcss = document.createElement("link");
            loadcss.setAttribute("rel", "stylesheet");
            loadcss.setAttribute("type", "text/css");
            loadcss.setAttribute("href", nq.nqSettings.nqCSS);
            document.getElementsByTagName("head")[0].appendChild(loadcss)
        }
    }
    ;
    this.nqStartNuqlium = function(b) {
        if (nq.nqRunBespokeFunctions("_StartNuqlium", b)) {
            nq.nqLog("Invoke Nuqlium");
            if (b == "1") {
                nq.nqLog("Different Page Browser Back Button Invoked");
                var d = false;
                var e = window.localStorage.getItem("nuqlium");
                if (e !== undefined && e !== "" && e !== null) {
                    try {
                        var f = JSON.parse(e);
                        if (f.type == nqDataLayer.pageType && f.key == nqDataLayer.pageKey && f.value == nqDataLayer.pageValue) {
                            if (f.html !== undefined && f.html !== "" && f.html !== null) {
                                d = true;
                                nq.nqLog("Consume from local storage");
                                nq.nqSettings.nqPageInstance = f.pageInstance;
                                $(function() {
                                    $("#nuqlium-container").replaceWith(f.html);
                                    var g = {};
                                    g.html = $("#nuqlium-container").html();
                                    g.manifest = f.manifest;
                                    g.tracking = f.tracking;
                                    g.userfilters = f.userfilters;
                                    nq.nqProcessData(g, f.type, f.key, null, false, false);
                                    if (f.scroll !== undefined && isNaN(f.scroll) == false) {
                                        $("html, body").animate({
                                            scrollTop: (f.scroll)
                                        }, 0)
                                    } else {
                                        if (f.position !== undefined && f.position !== "" && f.position !== null) {
                                            setTimeout(function() {
                                                var h = f.position;
                                                $nqHashListingPosition = $("[data-nq-listing-position='" + h + "']");
                                                if ($nqHashListingPosition.length > 0) {
                                                    nq.nqInternals.nqIsRequesting = true;
                                                    $("html, body").animate({
                                                        scrollTop: ($nqHashListingPosition.first().offset().top - nq.nqInternals.nqWindowBuffer)
                                                    }, 0, function() {
                                                        nq.nqInternals.nqIsRequesting = false
                                                    });
                                                    $nqHashListingPosition.addClass("nq-selected-product");
                                                    setTimeout(function() {
                                                        $("[data-nq-listing-position='" + h + "']").removeClass("nq-selected-product")
                                                    }, 3000)
                                                }
                                            }, 300)
                                        }
                                    }
                                })
                            }
                        }
                    } catch (c) {
                        d = false
                    }
                }
                if (d == false) {
                    nq.nqLog("Not in local storage, make call");
                    nq.nqSettings.nqPageInstance = nq.nqGenerateGuid();
                    nq.nqSearchApi(null, true, false)
                }
                nq.nqPreLoadApis();
                $(function() {
                    $(nq.nqSettings.nqPredictiveInput).keyup(function(g) {
                        nq.nqPredictApi($(this).val(), this, g)
                    }).click(function(g) {
                        nq.nqPredictApi($(this).val(), this, g)
                    });
                    nq.nqFeedsApi();
                    nq.nqBindEvents()
                })
            } else {
                if (b == "2") {
                    nq.nqLog("Same Page Browser Back Button Invoked");
                    nq.nqInternals.nqIsRequesting = true;
                    $("html, body").animate({
                        scrollTop: 0
                    }, 0, function() {
                        nq.nqInternals.nqIsRequesting = false
                    });
                    nq.nqSearchApi(null, true, false)
                } else {
                    nq.nqSettings.nqPageInstance = nq.nqGenerateGuid();
                    nq.nqSearchApi();
                    nq.nqPreLoadApis();
                    $(function() {
                        $(nq.nqSettings.nqPredictiveInput).keyup(function(g) {
                            nq.nqPredictApi($(this).val(), this, g)
                        }).click(function(g) {
                            nq.nqPredictApi($(this).val(), this, g)
                        });
                        nq.nqFeedsApi();
                        nq.nqBindEvents()
                    })
                }
            }
        }
        nq.nqSetCurrentPageNumberInfinite()
    }
    ;
    this.nqPredictApi = function(f, c, b) {
        nq.nqLog("predict");
        var d = true;
        if ($(c).attr("data-nq-suppress") !== undefined) {
            d = false
        }
        if (d) {
            if (b.keyCode === 27) {
                nq.nqHidePredictive()
            } else {
                if (nq.nqPredictiveLastClick === undefined) {
                    nq.nqPredictiveLastClick = Date.now();
                    nq.nqPredictiveGuid = nq.nqGenerateGuid()
                }
                if (Date.now() - nq.nqPredictiveLastClick > 2000) {
                    nq.nqPredictiveGuid = nq.nqGenerateGuid()
                }
                nq.nqPredictiveLastClick = Date.now();
                if (this.nqLastSearch == "" && f.length > 0) {
                    nq.nqLog("Predictive Search - Immediate");
                    nq.nqPredictApiLightBox("predictive", "", f, nq)
                } else {
                    nq.nqLog("Predictive Search - Timer Based on " + nq.nqSettings.nqPredictiveTimeout + "ms");
                    if (typeof nqSetTimeout !== "undefined") {
                        clearTimeout(nqSetTimeout)
                    }
                    nqSetTimeout = setTimeout(function() {
                        nq.nqPredictApiLightBox("predictive", "", f, nq)
                    }, nq.nqSettings.nqPredictiveTimeout)
                }
            }
        }
    }
    ;
    this.nqLastSearch = "";
    this.nqPredictApiLightBox = function(b, c, e, d) {
        if (e.length > 0) {
            nq.nqLog("nqPredictApi " + e);
            if ($("#nq-predictive-search").length === 0) {
                nq.nqAppendPredictiveHolders();
                $("#nq-predictive-search").attr("data-nq-predictive", e);
                $(document.body).on("click", "#nq-overlay-search", function() {
                    nq.nqHidePredictive()
                })
            }
            if (e !== nq.nqLastSearch) {
                nq.nqLastSearch = e;
                nq.nqInitApi("predictive", "", e)
            } else {
                nq.nqShowPredictive()
            }
        } else {
            nq.nqLastSearch = e;
            nq.nqHidePredictive()
        }
    }
    ;
    this.nqAppendPredictiveHolders = function() {
        $("body").append('<div style="display:none;" id="nq-predictive-search"></div>');
        $("body").append('<div style="display:none;" id="nq-overlay-search"></div>')
    }
    ;
    this.nqSearchApi = function(c, d, b) {
        nq.nqInitApi(null, c, "", null, d, null, b)
    }
    ;
    this.nqPreLoadApis = function() {
        if (typeof nqDataLayer !== "undefined" && nqDataLayer !== null) {
            if (typeof nqDataLayer.preloads !== "undefined" && nqDataLayer.preloads !== null) {
                for (var b = 0; b < nqDataLayer.preloads.length; b++) {
                    var c = nqDataLayer.preloads[b];
                    if (c.key != "" && c.value != "") {
                        var d = "[data-nq-" + c.key + '="' + c.value + '"]';
                        nq.nqInitApi(c.key, "", c.value, d)
                    }
                }
            }
        }
    }
    ;
    this.nqRunApi = function(c, e, b) {
        if (b === undefined) {
            var b = {};
            b.output = "json"
        }
        var d = 0;
        return nq.nqInitApi(c, "", e, d, false, b)
    }
    ;
    this.nqFeedsApi = function(d, e, c) {
        if (d !== undefined && e !== undefined && d !== null && e !== null) {
            $("[data-nq-" + d + "='" + e + "']").each(function() {
                $(this).attr("data-nq-instance", nq.nqSettings.nqPageInstance);
                var m = $(this);
                if ($(m).attr("data-nq-complete") !== "true") {
                    $(m).attr("data-nq-complete", "true");
                    var l = $(m).attr("data-nq-template");
                    var h = $(m).attr("data-nq-identifier");
                    var j = $(m).attr("data-nq-layout");
                    var k = $(m).attr("data-nq-meta");
                    var f = {};
                    if (l !== undefined) {
                        f.template = l
                    }
                    if (h !== undefined) {
                        f.identifier = h
                    }
                    if (j !== undefined) {
                        f.layout = j
                    }
                    try {
                        if (k !== undefined) {
                            k = k.replace(/'/g, '"');
                            f.meta = JSON.parse(k)
                        }
                    } catch (g) {
                        nq.nqLog(k);
                        nq.nqLog("Unable to parse JSON for meta data on feed");
                        nq.nqLog(g)
                    }
                    nq.nqInitApi(d, "", e, m, false, f)
                }
            })
        } else {
            var b = ["feed", "recommendations", "pages", "elements", "zone"];
            if (c !== undefined && c !== null) {
                b = c
            }
            for (i = 0; i < b.length; i++) {
                $("[data-nq-" + b[i] + "]").each(function() {
                    $(this).attr("data-nq-instance", nq.nqSettings.nqPageInstance);
                    if ($(this).attr("data-nq-postload") !== "true" && $(this).attr("data-nq-postload") !== "scroll" && $(this).attr("data-nq-preload") !== "true") {
                        var m = $(this).attr("data-nq-" + b[i] + "");
                        var n = $(this);
                        if ($(n).attr("data-nq-complete") !== "true") {
                            $(n).attr("data-nq-complete", "true");
                            var l = $(n).attr("data-nq-template");
                            var j = $(n).attr("data-nq-layout");
                            var h = $(n).attr("data-nq-identifier");
                            var k = $(n).attr("data-nq-meta");
                            var f = {};
                            if (l !== undefined) {
                                f.template = l
                            }
                            if (h !== undefined) {
                                f.identifier = h
                            }
                            if (j !== undefined) {
                                f.layout = j
                            }
                            try {
                                if (k !== undefined) {
                                    k = k.replace(/'/g, '"');
                                    f.meta = JSON.parse(k)
                                }
                            } catch (g) {
                                nq.nqLog(k);
                                nq.nqLog("Unable to parse JSON for meta data on feed");
                                nq.nqLog(g)
                            }
                            nq.nqInitApi(b[i], "", m, n, false, f)
                        }
                    }
                })
            }
        }
    }
    ;
    this.nqInitApi = function(j, aa, ae, Y, ad, c, h) {
        var L = false;
        var R = [];
        var s = false;
        var B = null;
        var ac = true;
        if (ad === true) {
            ac = false
        }
        var n = nq.nqDataIndex;
        var N = [];
        var F = "";
        var D = "";
        var G = "";
        var W = "";
        var O = "";
        var P = "";
        var E = "";
        var C = nq.nqSettings.nqPageInstance;
        var o = {};
        var A = {};
        var q = {};
        var y;
        var S;
        var t = false;
        var p;
        var Q;
        var J;
        var w;
        var X = false;
        var U;
        var x;
        var z = {};
        var I;
        var K;
        if (typeof nqDataLayer !== "undefined") {
            if (nqDataLayer !== null) {
                F = nqDataLayer.pageType;
                D = nqDataLayer.pageKey;
                G = nqDataLayer.pageValue;
                A = nqDataLayer.order;
                o = nqDataLayer.basket;
                E = nqDataLayer.pageType;
                if (typeof nqDataLayer.dataindex !== "undefined" && nqDataLayer.dataindex !== null) {
                    n = nqDataLayer.dataindex
                }
                if (typeof nqDataLayer.context !== "undefined" && nqDataLayer.context !== null) {
                    q = nqDataLayer.context
                }
                if (typeof nqDataLayer.template !== "undefined" && nqDataLayer.template !== null) {
                    S = nqDataLayer.template
                }
                if (typeof nqDataLayer.layout !== "undefined" && nqDataLayer.layout !== null) {
                    y = nqDataLayer.layout
                }
                if (typeof nqDataLayer.identifier !== "undefined" && nqDataLayer.identifier !== null) {
                    w = nqDataLayer.identifier
                }
                if (typeof nqDataLayer.display !== "undefined" && nqDataLayer.display !== null) {
                    t = nqDataLayer.display
                }
                if (typeof nqDataLayer.catalogue !== "undefined" && nqDataLayer.catalogue !== null) {
                    p = nqDataLayer.catalogue
                }
                if (typeof nqDataLayer.site !== "undefined" && nqDataLayer.site !== null) {
                    Q = nqDataLayer.site
                }
                if (typeof nqDataLayer.products !== "undefined" && nqDataLayer.products !== null) {
                    J = nqDataLayer.products
                }
                if (typeof nqDataLayer.items !== "undefined" && nqDataLayer.items !== null) {
                    x = nqDataLayer.items
                }
                if (typeof nqDataLayer.staging !== "undefined" && nqDataLayer.staging !== null) {
                    X = nqDataLayer.staging
                }
                if (typeof nqDataLayer.token !== "undefined" && nqDataLayer.token !== null) {
                    U = nqDataLayer.token
                }
                if (typeof nqDataLayer.meta !== "undefined" && nqDataLayer.meta !== null) {
                    z = nqDataLayer.meta
                }
                if (typeof nqDataLayer.pricelist !== "undefined" && nqDataLayer.pricelist !== null) {
                    I = nqDataLayer.pricelist
                }
                if (typeof nqDataLayer.region !== "undefined" && nqDataLayer.region !== null) {
                    K = nqDataLayer.region
                }
                if (typeof nqDataLayer.output !== "undefined" && nqDataLayer.output !== null) {
                    B = nqDataLayer.output
                }
                if (j === null || (j !== null && j.length == 0)) {
                    j = F
                }
                if (ae === null || (ae !== null && ae.length == 0)) {
                    ae = D
                }
            }
        }
        if (nq.nqRunBespokeFunctions("_InitApiPre", j, aa, ae, Y, ad, c)) {
            if (nq.nqAllowedKeys.indexOf(j) !== -1) {
                nq.nqSettings.nqInstance++;
                var H = null;
                if (Y !== undefined && Y !== null && Y != 0) {
                    if ($(Y).attr("data-nq-products") !== undefined) {
                        J = $(Y).attr("data-nq-products").split(",")
                    }
                    if ($(Y).attr("data-nq-items") !== undefined) {
                        x = $(Y).attr("data-nq-items").split(",")
                    }
                    if ($(Y).attr("data-nq-page-value") !== undefined) {
                        H = $(Y).attr("data-nq-page-value")
                    }
                    C = $(Y).attr("data-nq-instance")
                } else {
                    if (Y !== undefined && Y !== null && Y == 0) {
                        L = true
                    }
                }
                if (j === "predictive" || j === "feed" || j === "elements" || j === "zone" || (j === "pages" && Y !== undefined && Y !== null)) {
                    G = D;
                    F = j;
                    D = ae;
                    S = null;
                    w = null
                }
                if (j === "recommendations") {
                    G = D;
                    F = j;
                    D = ae;
                    if (H !== null) {
                        G = H
                    }
                    S = null;
                    w = null
                }
                if (j === "group") {
                    G = "";
                    F = j;
                    D = ae;
                    S = null;
                    w = null
                }
                if (c !== undefined && c !== null) {
                    if (c.template !== undefined) {
                        S = c.template
                    }
                    if (c.layout !== undefined) {
                        y = c.layout
                    }
                    if (c.identifier !== undefined) {
                        w = c.identifier
                    }
                    if (c.output !== undefined) {
                        B = c.output
                    }
                    if (c.meta !== undefined) {
                        for (var j in c.meta) {
                            var l = false;
                            for (var f in z) {
                                if (z[f].key == j) {
                                    l = true;
                                    z[f].value = c.meta[j]
                                }
                            }
                            if (l == false) {
                                var k = {};
                                k.key = j;
                                k.value = c.meta[j];
                                z.push(k)
                            }
                        }
                    }
                }
                cookieRead = nq.nqReadCookie("nqcore");
                if (cookieRead !== null && cookieRead !== "" && cookieRead !== "undefined") {
                    try {
                        nqCookie = JSON.parse(cookieRead);
                        W = nqCookie.userid;
                        O = nqCookie.session;
                        P = nqCookie.sessiondate;
                        if (typeof (nqCookie.debug) != "undefined") {
                            if (nqCookie.debug == "true") {
                                s = true
                            }
                        }
                    } catch (g) {
                        nq.nqLog("Unable to read core cookie");
                        nq.nqLog(cookieRead)
                    }
                }
                var d = nq.nqReadCookie("nqproducts");
                if (d !== null && d !== "" && d !== "undefined") {
                    try {
                        nqCookieProducts = JSON.parse(d);
                        if (typeof nqCookieProducts.products !== "undefined") {
                            N = nqCookieProducts.products
                        }
                    } catch (g) {
                        nq.nqLog("Unable to read products cookie");
                        nq.nqLog(d)
                    }
                }
                if (F == "product") {
                    d = {};
                    nq.nqRemoveFromArray(N, D);
                    N.unshift(D);
                    N = N.slice(0, 20);
                    d.products = N;
                    nq.nqCreateCookie("nqproducts", JSON.stringify(d), 31)
                }
                var e = nq.nqReadCookie("nqsources");
                if (e !== null && e !== "" && e !== "undefined") {
                    try {
                        nqCookieSources = JSON.parse(e);
                        if (typeof nqCookieProducts.products !== "undefined") {
                            R = nqCookieSources
                        }
                    } catch (g) {
                        nq.nqLog("Unable to read sources cookie");
                        nq.nqLog(d)
                    }
                }
                if (F === "search" && D.indexOf("[image:") > -1) {
                    F = "visual"
                }
                var r = {
                    clientid: nq.nqSettings.nqClient,
                    pagetype: F,
                    pagekey: D,
                    pagevalue: G,
                    dataindex: n,
                    token: U,
                    meta: z,
                    settings: {},
                    tracking: {
                        clientid: nq.nqSettings.nqClient,
                        userid: W,
                        live: t,
                        session: O,
                        sessiondate: P,
                        screenwidth: window.screen.width,
                        screenheight: window.screen.height,
                        pageinstance: C
                    },
                    context: nq.nqProcessContext(q)
                };
                if (F != E) {
                    r.pageorigin = E
                }
                if (B != null) {
                    r.output = B
                }
                nq.AddToObjectIfDataExists(r, "settings", "campaign", nq.nqGetData("campaign", null, "number"));
                nq.AddToObjectIfDataExists(r, "settings", "catalogue", p);
                nq.AddToObjectIfDataExists(r, "settings", "columns", nq.nqGetColumns());
                nq.AddToObjectIfDataExists(r, "settings", "collection", nq.getQuerystringAsString(aa));
                nq.AddToObjectIfDataExists(r, "settings", "date", nq.nqGetData("date"));
                nq.AddToObjectIfDataExists(r, "settings", "domain", document.domain);
                nq.AddToObjectIfDataExists(r, "settings", "identifier", w);
                nq.AddToObjectIfDataExists(r, "settings", "image", nq.nqGetData("image", null, "number"));
                nq.AddToObjectIfDataExists(r, "settings", "instance", nq.nqSettings.nqInstance);
                nq.AddToObjectIfDataExists(r, "settings", "ip", nq.nqGetData("ipaddress"));
                nq.AddToObjectIfDataExists(r, "settings", "page", nq.nqGetData("page", j, "number"));
                nq.AddToObjectIfDataExists(r, "settings", "paging", nq.nqGetData("paging"));
                nq.AddToObjectIfDataExists(r, "settings", "pricelist", I);
                nq.AddToObjectIfDataExists(r, "settings", "products", J);
                nq.AddToObjectIfDataExists(r, "settings", "region", K);
                nq.AddToObjectIfDataExists(r, "settings", "site", Q);
                nq.AddToObjectIfDataExists(r, "settings", "sort", nq.nqGetData("sort", null, "number"));
                nq.AddToObjectIfDataExists(r, "settings", "template", S);
                nq.AddToObjectIfDataExists(r, "settings", "layout", y);
                nq.AddToObjectIfDataExists(r, "settings", "variation", nq.nqGetData("variation", null, "number"));
                if (nq.nqSendSources) {
                    r.sources = R;
                    nq.nqSendSources = false
                }
                if (j === "predictive" && nq.nqPredictiveGuid !== undefined) {
                    r.searchtoken = nq.nqPredictiveGuid
                }
                if (nq.nqDebug) {
                    r.settings.debug = true
                }
                if (nq.nqPerf) {
                    r.settings.performance = true
                }
                if (typeof N != undefined) {
                    r.rvp = N
                }
                if (A !== "" && F == "purchase") {
                    r.tracking.order = A
                }
                if (o !== "" && F == "basket") {
                    r.tracking.basket = o
                }
                if (ac && j !== "predictive" && j !== "feed" && j !== "group" && j !== "recommendations" && Object.keys(nq.nqActions).length > 0) {
                    $.each(nq.nqActions, function(af, ag) {
                        r.settings[af] = ag
                    })
                }
                var M = true;
                if (W === undefined || W === "") {
                    M = false
                }
                var T = 2000;
                var u = false;
                if (t === true) {
                    u = true;
                    T = 5000
                }
                var V = false;
                if (nq.nqDebug) {
                    T = T * 2
                }
                if (nq.nqGetData("_failover") === "true") {
                    V = true
                }
                var v = "event";
                switch (F) {
                case "pages":
                    v = "pages";
                    break;
                case "product":
                    v = "product";
                    break;
                case "purchase":
                    v = "purchase";
                    break;
                case "basket":
                    v = "basket";
                    break;
                case "zone":
                    v = "zones";
                    break;
                case "elements":
                    v = "elements";
                    break;
                case "feed":
                    v = "feeds";
                    break;
                case "set":
                    v = "collections";
                    break;
                case "recommendations":
                    v = "recommendations";
                    break;
                case "category":
                    v = "listings";
                    break;
                case "predictive":
                case "search":
                    v = "search";
                    break;
                case "visual":
                    v = "visual";
                    break;
                case "group":
                    v = "group";
                    break
                }
                var Z = nq.nqSettings.nqApiUrl;
                var ab = nq.nqSettings.nqFailoverUrl;
                if (X) {
                    Z = nq.nqSettings.nqStagingUrl
                }
                if (V) {
                    Z = nq.nqSettings.nqFailoverUrl;
                    ab = nq.nqSettings.nqApiUrl;
                    r.failover = true
                }
                var b = {
                    method: "post",
                    type: "post",
                    url: Z + v + "/",
                    contentType: "application/x-www-form-urlencoded",
                    data: r,
                    async: M,
                    timeout: T
                };
                if (L) {
                    b.async = false
                }
                var m = $.ajax(b).done(function(ag) {
                    if (u && L == false) {
                        nq.nqProcessData(ag, j, ae, Y, h, true)
                    }
                    var af = nq.nqClone(ag.tracking);
                    delete af.campaign;
                    delete af.variation;
                    nq.nqCreateCookie("nqcore", JSON.stringify(af), 31);
                    nq.nqCreateCookie("nqsources", null, -1)
                }).fail(function() {
                    b.data.failover = true;
                    b.url = ab + v + "/";
                    b.timeout = T * 2;
                    $.ajax(b).done(function(ag) {
                        if (u && L == false) {
                            nq.nqProcessData(ag, j, ae, Y, h, true)
                        }
                        var af = nq.nqClone(ag.tracking);
                        delete af.campaign;
                        delete af.variation;
                        nq.nqCreateCookie("nqcore", JSON.stringify(af), 31);
                        nq.nqCreateCookie("nqsources", null, -1)
                    })
                });
                if (L) {
                    try {
                        return JSON.parse(m.responseText)
                    } catch (g) {
                        return null
                    }
                }
            }
        }
        nq.nqRunBespokeFunctions("_InitApi", j, aa, ae, Y, ad, c)
    }
    ;
    this.AddToObjectIfDataExists = function(c, d, b, e) {
        if (typeof e != "undefined" && e != "" && e != null) {
            switch (d) {
            case "settings":
                c[d][b] = e;
                break
            }
        }
        return c
    }
    ;
    this.nqProcessData = function(b, e, g, f, c, d) {
        nq.nqLastManifest = b.manifest;
        nq.nqLastTracking = b.tracking;
        nq.nqLastUserFilters = b.userfilters;
        $(function() {
            if (nq.nqRunBespokeFunctions("_ProcessDataPre", b, e, g, f, c, d)) {
                if (b !== undefined) {
                    var o = b.tracking.campaign;
                    var p = b.tracking.variation;
                    var k = b.html;
                    if (k === undefined) {
                        k = b.Html
                    }
                    k = nq.nqProcessGlobal(k, self);
                    switch (e) {
                    case "predictive":
                        k = nq.nqProcessPredictiveData(k);
                        $("#nq-predictive-search").html(k);
                        $("#nq-predictive-search").attr("data-nq-campaign", o);
                        $("#nq-predictive-search").attr("data-nq-variation", p);
                        nq.nqShowPredictive();
                        break;
                    case "group":
                        $(f)[0].outerHTML = k;
                        break;
                    default:
                        if (f !== undefined && f !== null) {
                            $(f).html(k);
                            $(f).attr("data-nq-campaign", o);
                            $(f).attr("data-nq-variation", p)
                        } else {
                            if (b.redirect !== undefined) {
                                var m = nq.nqProcessGlobal(b.redirect, self);
                                document.location.href = m;
                                break
                            }
                            nq.nqAppendHtml(k, c);
                            if ($(nq.nqSettings.nqSearchId).length > 0) {
                                $(nq.nqSettings.nqSearchId).attr("data-nq-campaign", o)
                            }
                            if ($(nq.nqSettings.nqSearchId).length > 0) {
                                $(nq.nqSettings.nqSearchId).attr("data-nq-variation", p)
                            }
                            nq.nqVariation = p;
                            nq.nqCampaign = o;
                            nq.nqInitialiseSliders();
                            nq.nqInternals.nqIsRequesting = false;
                            nq.nqInfiniteScroll();
                            if (e == "search" && b.bounds !== undefined) {
                                nq.nqProcessVisualSearch(b.bounds, b.bound)
                            }
                        }
                        break
                    }
                    var h = ["feed", "recommendations", "pages", "elements", "zone"];
                    var j = h.indexOf(e);
                    if (j > -1) {
                        h.splice(j, 1)
                    }
                    nq.nqFeedsApi(null, null, h)
                }
            }
            nq.nqRunBespokeFunctions("_ProcessData", b, e, g, f, c, d);
            if (typeof (b.xray) != "undefined") {
                var l;
                if (nq.nqSettings.nqDebugModeIsOn == "true") {
                    l.nqxProcess(b, e, g)
                } else {
                    loadcss = document.createElement("link");
                    loadcss.setAttribute("rel", "stylesheet");
                    loadcss.setAttribute("type", "text/css");
                    loadcss.setAttribute("href", nq.nqSettings.nqApiUrl + "xray.css");
                    document.getElementsByTagName("head")[0].appendChild(loadcss);
                    var n = document.createElement("SCRIPT");
                    n.src = nq.nqSettings.nqApiUrl + "xray.js";
                    n.type = "text/javascript";
                    n.onload = function() {
                        l = new nqxClass();
                        l.nqxStart();
                        l.nqxProcess(b, e, g)
                    }
                    ;
                    document.getElementsByTagName("head")[0].appendChild(n);
                    nq.nqSettings.nqDebugModeIsOn == "true"
                }
            }
        })
    }
    ;
    this.nqBindEvents = function() {
        if (nq.nqRunBespokeFunctions("_nqBindEvents")) {
            $(document.body).on("mouseenter", "[data-nq-page]", function() {
                nq.nqPageNumber($(this))
            });
            $(document.body).on("click", "[data-nq-group]", function(b) {
                nq.InitGroup($(this));
                b.stopPropagation()
            });
            $(document.body).on("click", "[data-nq-filter]", function() {
                nq.nqFilter($(this))
            });
            $(document.body).on("click", "[data-nq-filter-clear]", function() {
                nq.nqFilterClear($(this))
            });
            $(document.body).on("click", "[data-nq-filter-mimic]", function() {
                nq.nqFilterSelected($(this))
            });
            $(document.body).on("click", "[data-nq-action]:not(select)", function() {
                nq.nqDataAction($(this))
            });
            $(document.body).on("change", "select[data-nq-action]", function() {
                nq.nqDataAction($(this), "select")
            });
            $(document.body).on("click", "[data-nq-product]", function() {
                nq.nqProductClick($(this))
            });
            $(document.body).on("click", "[data-nq-camera]", function() {
                nq.nqImageCapture($(this))
            });
            $(document.body).on("click", "[data-nq-image-search]", function() {
                nq.nqImageCaptureSend(null, $(this).attr("data-nq-image-search"))
            });
            $(document.body).on("drag dragstart dragend dragover dragenter dragleave drop", "[data-nq-camera]", function(b) {
                nq.nqImageCaptureDragDrop($(this), b)
            })
        }
    }
    ;
    this.nqSetCurrentPageNumberInfinite = function() {
        var c = nq.nqGetUrlVars();
        try {
            nq.nqSettings.nqCurrentPageNumberInfinite = c.page;
            if (nq.nqSettings.nqCurrentPageNumberInfinite == undefined) {
                nq.nqSettings.nqCurrentPageNumberInfinite = 1
            }
        } catch (b) {}
    }
    ;
    this.nqPageNumber = function(c) {
        var b = $(c).attr("data-nq-page");
        nq.nqSettings.nqCurrentPageNumberInfinite = b;
        nq.UpdatePageInURL(b)
    }
    ;
    this.nqRunBespokeFunctions = function(b, e, f, g, h, j, k, l, m) {
        if (typeof nq["nqDataIndex" + nq.nqDataIndex] === "function") {
            var c = new nq["nqDataIndex" + nq.nqDataIndex]();
            if (typeof c[b] === "function") {
                var d = c[b](e, f, g, h, j, k, l, m);
                if (d === false) {
                    return false
                }
            }
        }
        return true
    }
    ;
    this.nqAppendHtml = function(e, f) {
        if (nq.nqRunBespokeFunctions("_AppendHtmlPre", e)) {
            var b = true;
            var j = false;
            if (f !== undefined && f !== null && f == true) {
                b = true
            } else {
                if (nq.nqLastAction === "page") {
                    var g = $(e).find("[data-nq-paging]").attr("data-nq-paging");
                    if (g !== undefined) {
                        nq.nqPaging = g
                    }
                    if (nq.nqPaging === "more" || nq.nqPaging === "infinite") {
                        $lastPage = $(nq.nqSettings.nqSearchId + " [data-nq-page]:last");
                        $firstPage = $(nq.nqSettings.nqSearchId + " [data-nq-page]:first");
                        $currentPage = $(e).find("[data-nq-page]");
                        var c = $currentPage.attr("data-nq-page");
                        $existingPage = $('[data-nq-page="' + c + '"]');
                        if ($existingPage.length == 0) {
                            if (nq.nqLastActionValue < parseInt($firstPage.attr("data-nq-page"))) {
                                $('[data-nq-paging-more="prev"]').remove();
                                $currentPage.find('[data-nq-paging-more="next"]').remove();
                                $firstPage.before($currentPage);
                                b = false
                            } else {
                                $('[data-nq-paging-more="next"]').remove();
                                $currentPage.find('[data-nq-paging-more="prev"]').remove();
                                $lastPage.after($currentPage);
                                b = false
                            }
                        } else {
                            b = false;
                            setTimeout(function() {
                                nq.nqInternals.nqIsRequesting = true;
                                j = true;
                                $("html, body").animate({
                                    scrollTop: ($existingPage.offset().top - nq.nqInternals.nqWindowBuffer)
                                }, 0, function() {
                                    nq.nqInternals.nqIsRequesting = false
                                })
                            }, 300)
                        }
                    }
                }
            }
            if (b) {
                if ($(nq.nqSettings.nqSearchId).length > 0) {
                    var h = nq.nqSettings.nqSearchId.replace("#", "");
                    document.getElementById(h).innerHTML = e
                }
            }
            var d = window.location.hash;
            if (d !== "" && j == false) {
                setTimeout(function() {
                    d = d.replace(new RegExp("#","g"), "");
                    $nqHashListingPosition = $("[data-nq-listing-position='" + d + "']");
                    if ($nqHashListingPosition.length > 0) {
                        nq.nqInternals.nqIsRequesting = true;
                        $("html, body").animate({
                            scrollTop: ($nqHashListingPosition.first().offset().top - nq.nqInternals.nqWindowBuffer)
                        }, 0, function() {
                            nq.nqInternals.nqIsRequesting = false
                        });
                        $nqHashListingPosition.addClass("nq-selected-product");
                        setTimeout(function() {
                            $("[data-nq-listing-position='" + d + "']").removeClass("nq-selected-product")
                        }, 3000)
                    }
                }, 300)
            }
        }
        nq.nqRunBespokeFunctions("_AppendHtml", e)
    }
    ;
    this.nqInitialiseSliders = function() {
        if (nq.nqRunBespokeFunctions("_InitialiseSlidersPre")) {
            $("[data-nq-filtergroup] .irs-hidden-input").remove();
            $("[data-nq-filtergroup] .irs").remove();
            $("input[data-slider]").each(function(c) {
                $nqSliderInput = $(this);
                $nqSliderId = $nqSliderInput.attr("data-slider");
                $nqDefaultSliderValue = "";
                if ($nqSliderInput.attr("data-slider-filter-min") !== "" && $nqSliderInput.attr("data-slider-filter-max") !== "") {
                    $nqDefaultSliderValue = $nqSliderInput.attr("data-slider-filter-min") + "-" + $nqSliderInput.attr("data-slider-filter-max")
                }
                $nqSliderStep = nq.nqSliderRules("step", $nqSliderInput);
                $nqSliderInput.after('<div id="nq-div-' + $nqSliderId + '" data-nq-property="' + $nqSliderId + '"  data-nq-property-value="' + $nqDefaultSliderValue + '"></div>');
                $("#nq-div-" + $nqSliderId).ionRangeSlider({
                    prettify: function(e) {
                        return nq.nqSliderNumberFormat(e, $nqSliderInput.attr("data-slider-rule"))
                    },
                    type: "double",
                    min: $nqSliderInput.attr("data-slider-min"),
                    max: $nqSliderInput.attr("data-slider-max"),
                    prefix: $nqSliderInput.attr("data-slider-prefix"),
                    postfix: $nqSliderInput.attr("data-slider-suffix"),
                    from_min: $nqSliderInput.attr("data-slider-value-min"),
                    step: $nqSliderStep,
                    to_max: $nqSliderInput.attr("data-slider-value-max"),
                    onFinish: function(e) {
                        if (isNaN(e.from)) {
                            e.from = 0
                        }
                        if ((e.from === $(e.input.context).attr("data-slider-min") && e.to === $(e.input.context).attr("data-slider-max"))) {
                            $("#nq-div-" + $nqSliderId).attr("data-nq-property-value", "")
                        } else {
                            $("#nq-div-" + $nqSliderId).attr("data-nq-property-value", e.from + "-" + e.to)
                        }
                        nq.nqLastAction = $("#nq-div-" + $nqSliderId).attr("data-nq-property");
                        nq.nqLastActionValue = $("#nq-div-" + $nqSliderId).attr("data-nq-property-value");
                        $("[data-nq-property='page']").attr("data-nq-property-value", 1);
                        nq.nqApplyFilters(true)
                    },
                });
                var b = $nqSliderInput.attr("data-slider-filter-min");
                if (b !== "") {
                    $("#nq-div-" + $nqSliderId).data("ionRangeSlider").update({
                        from: b
                    })
                }
                var d = $nqSliderInput.attr("data-slider-filter-max");
                if (d !== "") {
                    $("#nq-div-" + $nqSliderId).data("ionRangeSlider").update({
                        to: d
                    })
                }
                $("[data-nq-slider-text]").each(function() {
                    $(this).html(nq.nqSliderNumberFormat($(this).html(), $(this).attr("nq-slider-text")))
                })
            })
        }
        nq.nqRunBespokeFunctions("_InitialiseSliders")
    }
    ;
    this.nqSliderRules = function(c, b) {
        returnValue = 1;
        switch (c) {
        default:
            break
        }
        return returnValue
    }
    ;
    this.nqSliderNumberFormat = function(b, d) {
        var c = b;
        return c
    }
    ;
    this.nqProcessPredictiveData = function(b) {
        var c = $(b).find("[data-nq-recent-searches]").html();
        if (c !== "undefined" && c !== undefined) {
            cookieRead = nq.nqReadCookie("nqPreviousSearches");
            if (cookieRead !== null && cookieRead !== "") {
                var e = JSON.parse(cookieRead);
                var d = "";
                for (i = 0; i < e.length; i++) {
                    d = d + c.replace(new RegExp("nq.search","g"), e[i])
                }
                $dataUpdated = $(b).find("[data-nq-recent-searches]").html(d).end()
            } else {
                $dataUpdated = $(b).find("[data-nq-recent-searches]").html(nq.nqSettings.nqNoRecentSearches).end()
            }
        }
        nq.nqRunBespokeFunctions("_ProcessPredictiveData", $dataUpdated);
        return $dataUpdated
    }
    ;
    this.nqInfiniteScroll = function() {
        if (nq.nqPaging === "infinite" || $('[data-nq-postload="scroll"]:not([data-nq-complete="true"])').length > 0) {
            $(window).scroll(function() {
                nq.nqInternals.nqDidScroll = true
            });
            nq.nqInternals.nqInterval = setInterval(function() {
                nq.nqHandleScroll()
            }, 250)
        } else {
            if (nq.nqInternals.nqInterval !== undefined) {
                clearInterval(nq.nqInternals.nqInterval)
            }
        }
    }
    ;
    this.nqHandleScroll = function() {
        if (nq.nqInternals.nqDidScroll && nq.nqInternals.nqIsRequesting === false) {
            nq.nqInternals.nqDidScroll = false;
            if (nq.nqPaging === "infinite") {
                $nqNextObject = $("[data-nq-paging-more='next']");
                nq.nqLog($nqNextObject);
                if ($nqNextObject.length > 0) {
                    if ($(window).scrollTop() > $nqNextObject.position().top - (nq.nqInternals.nqWindowHeight * 2)) {
                        nq.nqInternals.nqIsRequesting = true;
                        $nqNextObject.find("[data-nq-action='page']").click();
                        $nqNextObject.remove();
                        nq.nqLog("Requesting next page ")
                    }
                }
            }
            $nqPostLoads = $('[data-nq-postload="scroll"]:not([data-nq-complete="true"])');
            if ($nqPostLoads.length > 0) {
                var b = ["feed", "recommendations", "zone", "elements"];
                $nqPostLoads.each(function() {
                    $selfPostLoad = $(this);
                    for (nqCnter = 0; nqCnter < b.length; nqCnter++) {
                        var d = "";
                        var c = "";
                        if (typeof ($selfPostLoad.attr("data-nq-" + b[nqCnter])) != "undefined") {
                            d = b[nqCnter];
                            c = $selfPostLoad.attr("data-nq-" + b[nqCnter]);
                            if ($(window).scrollTop() > ($selfPostLoad.position().top - (nq.nqInternals.nqWindowHeight * 2))) {
                                nq.nqFeedsApi(d, c);
                                nq.nqLog(d + " ==> " + c)
                            }
                        }
                    }
                });
                if (nq.nqInternals.nqInterval !== undefined) {
                    clearInterval(nq.nqInternals.nqInterval)
                }
                nq.nqInfiniteScroll()
            }
        }
    }
    ;
    this.nqProcessFilters = function(b, e) {
        var c = $(b);
        if (e !== "undefined" && e !== undefined) {
            var d = 0;
            $.each(e, function(f, g) {
                d += 1;
                if (nq.nqSettings.nqDynamicFiltering === "True" || nq.nqSettings.nqDynamicFiltering === true) {
                    c.find("[data-nq-filtergroup='" + f + "']").css("order", d.toString())
                }
                if (nq.nqSettings.nqFilterFavourites === "True" || nq.nqSettings.nqFilterFavourites === true) {
                    c.find("[data-nq-filter-favourites='" + f + "']").each(function() {
                        $block = $(this);
                        var h = false;
                        for (i = 0; i < g.length; i++) {
                            if (g[i] !== "") {
                                var j = c.find("[data-nq-filter][data-nq-key='" + f + "'][data-nq-value='" + g[i] + "']");
                                if (j.length > 0) {
                                    var k = j.clone();
                                    k.removeAttr("data-nq-filter");
                                    k.attr("data-nq-filter-mimic", "true");
                                    $block.append(k);
                                    h = true
                                }
                            }
                            if ($block.find("[data-nq-filter-mimic]").length === 5) {
                                break
                            }
                        }
                        if (h) {
                            $block.removeClass("hidden")
                        }
                    })
                }
            })
        }
        return c
    }
    ;
    this.nqSaveSearch = function(e) {
        var c = [];
        cookieRead = nq.nqReadCookie("nqPreviousSearches");
        if (cookieRead !== null && cookieRead !== "") {
            var d = JSON.parse(cookieRead);
            var b = d.indexOf(e);
            if (b >= 0) {
                d.splice(b, 1)
            }
            c.push(e);
            for (i = 0; i < d.length; i++) {
                c.push(d[i]);
                if (i === (nq.nqSettings.nqPredictivePrevMax - 2)) {
                    break
                }
            }
        } else {
            c.push(e)
        }
        nq.nqCreateCookie("nqPreviousSearches", JSON.stringify(c), 31)
    }
    ;
    this.nqIsDebug = function(c) {
        if (c == "nqxray") {
            cookieRead = nq.nqReadCookie("nqcore");
            if (cookieRead !== null && cookieRead !== "" && cookieRead !== "undefined") {
                try {
                    nqCookie = JSON.parse(cookieRead);
                    if (typeof (nqCookie.debug) != "undefined") {
                        if (nqCookie.debug == true || nqCookie.debug == "true") {
                            return true
                        }
                    }
                } catch (b) {}
            }
        }
        var d = window.location.href;
        if (d.indexOf("?" + c + "=") === -1 && d.indexOf("&" + c + "=") === -1) {
            return false
        } else {
            return true
        }
    }
    ;
    this.nqGetData = function(c, b, d) {
        if (b !== undefined && b !== null) {
            switch (b) {
            case "group":
                if (c === "page") {
                    return 1
                }
                break
            }
        }
        dataValue = nq.nqGetUrlVars()[c];
        if (typeof dataValue === "function") {
            dataValue = ""
        }
        switch (c) {
        case "paging":
            if (dataValue === null || dataValue === undefined || dataValue === "undefined") {
                if (nq.nqPaging !== null) {
                    dataValue = nq.nqPaging
                }
            }
            break;
        case "variation":
            if (dataValue === null || dataValue === undefined || dataValue === "undefined") {
                if (nq.nqVariation !== null) {
                    dataValue = nq.nqVariation
                }
            }
            break;
        case "campaign":
            if (dataValue === null || dataValue === undefined || dataValue === "undefined") {
                if (nq.nqCampaign !== null) {
                    dataValue = nq.nqCampaign
                }
            }
            break
        }
        switch (d) {
        case "number":
            if (isNaN(dataValue)) {
                dataValue = null
            }
            break
        }
        if (typeof dataValue == "undefined") {
            dataValue = null
        }
        return dataValue
    }
    ;
    this.nqIsValueValid = function(b) {
        return b
    }
    ;
    this.nqFilterSelected = function(c) {
        var b = $(c).attr("data-nq-key");
        var d = $(c).attr("data-nq-value");
        $('[data-nq-filter][data-nq-key="' + b + '"][data-nq-value="' + d + '"]').click()
    }
    ;
    this.nqFilterClear = function(c) {
        var b = $(c).attr("data-nq-filter-clear");
        if (b !== "" && b !== "true") {
            $(".nuqlium [data-nq-key='" + b + "'][data-nq-filter][data-nq-selected=true]").attr("data-nq-selected", false);
            $("[data-nq-property='page']").attr("data-nq-property-value", 1);
            nq.nqLastAction = "filter";
            nq.nqLastActionValue = "clear";
            nq.nqApplyFilters(true)
        } else {
            $('[data-nq-property="price"]').attr("data-nq-property-value", "");
            $(".nuqlium [data-nq-filter][data-nq-selected=true]").attr("data-nq-selected", false);
            $("[data-nq-property='page']").attr("data-nq-property-value", 1);
            nq.nqLastAction = "filter";
            nq.nqLastActionValue = "clear";
            nq.nqApplyFilters(true)
        }
        nq.nqRunBespokeFunctions("_FilterClear", c)
    }
    ;
    this.nqFilter = function(c) {
        var b = "true";
        if ($(c).attr("data-nq-selected") !== undefined) {
            if ($(c).attr("data-nq-selected") === "true") {
                b = "false"
            }
        }
        $(c).attr("data-nq-selected", b);
        $("[data-nq-property='page']").attr("data-nq-property-value", 1);
        nq.nqSettings.nqCurrentPageNumberInfinite = "1";
        nq.nqLastAction = "filter";
        nq.nqLastActionValue = $(c).attr("data-nq-key");
        nq.nqRunBespokeFunctions("_Filter", c);
        nq.nqApplyFilters(true)
    }
    ;
    this.nqDataAction = function(h, g) {
        var f = true;
        var c = $(h).attr("data-nq-action");
        var k = $(h).attr("data-nq-value");
        var d = c.split("|");
        var l = k.split("|");
        var e = d.length;
        if (d.length !== l.length) {
            e = 1
        }
        if (d.indexOf("image") > -1) {
            f = false
        }
        for (actionsCount = 0; actionsCount < e; actionsCount++) {
            var b = d[actionsCount];
            var j = l[actionsCount];
            if (g === "select") {
                $(".nuqlium [data-nq-property='" + b + "']").attr("data-nq-property-value", $(h).val())
            } else {
                $(".nuqlium [data-nq-property='" + b + "']").attr("data-nq-property-value", j)
            }
            if (e === 1 && b !== "paging" && b !== "page" && b !== "template" && b !== "columns") {
                $("[data-nq-property='page']").attr("data-nq-property-value", 1);
                nq.nqSettings.nqCurrentPageNumberInfinite = "1"
            }
        }
        nq.nqLastAction = b;
        nq.nqLastActionValue = j;
        nq.nqRunBespokeFunctions("_DataAction", h, g);
        nq.nqApplyFilters(f)
    }
    ;
    this.nqApplyFilters = function(b) {
        nq.nqRunBespokeFunctions("_ApplyFiltersPre");
        nq.nqActions = {};
        var e = "";
        if (b) {
            $(".nuqlium [data-nq-filter][data-nq-selected=true]").each(function() {
                e = e + "&" + ($(this).attr("data-nq-key") + "=" + encodeURIComponent($(this).attr("data-nq-value").toLowerCase()))
            })
        }
        $(".nuqlium [data-nq-property]").each(function() {
            if ($(this).attr("data-nq-property") != "page") {
                if ($(this).attr("data-nq-property-value") !== "") {
                    if ($(this).attr("data-nq-property-value") !== "0") {
                        if ($(this).attr("data-nq-property-value") !== $(this).attr("data-nq-property-default")) {
                            e = e + "&" + ($(this).attr("data-nq-property") + "=" + encodeURIComponent($(this).attr("data-nq-property-value").toLowerCase()))
                        }
                    }
                }
                nq.nqActions[$(this).attr("data-nq-property")] = $(this).attr("data-nq-property-value").toLowerCase()
            }
        });
        $pageProperty = $(".nuqlium [data-nq-property='page']");
        if ($pageProperty.length > 0) {
            var d = $pageProperty.attr("data-nq-property-value");
            if (nq.nqPaging != "paging" && nq.nqSettings.nqCurrentPageNumberInfinite !== undefined) {
                d = nq.nqSettings.nqCurrentPageNumberInfinite
            }
            if (d != "1") {
                e = e + "&page=" + d
            }
            nq.nqActions.page = $pageProperty.attr("data-nq-property-value")
        }
        var c = document.location.href;
        $(".nuqlium [data-nq-filtergroup]").each(function() {
            c = nq.nqRemoveURLParameter(c, $(this).attr("data-nq-filtergroup"))
        });
        $(".nuqlium [data-nq-property]").each(function() {
            c = nq.nqRemoveURLParameter(c, $(this).attr("data-nq-property"))
        });
        $(".nuqlium [data-nq-legacy]").each(function() {
            c = nq.nqRemoveURLParameter(c, $(this).attr("data-nq-legacy"))
        });
        nq.nqSettings.nqInstance = 0;
        nq.nqSearchApi(e);
        nq.nqUpdateURL(c + e);
        nq.nqRunBespokeFunctions("_ApplyFilters")
    }
    ;
    this.nqUpdateURL = function(b) {
        if (b != window.location.href) {
            if (b.indexOf("/&") > -1) {
                b = b.replace("/&", "/?")
            }
            if (b.indexOf("/?&") > -1) {
                b = b.replace("/?&", "/?")
            }
            nq.nqPausePopStateWatcher();
            try {
                window.history.pushState({
                    html: "",
                    pageTitle: ""
                }, "", nq.nqCleanURL(b))
            } catch (c) {
                nq.nqLog("Unable to push state");
                nq.nqLog(nq.nqCleanURL(b))
            }
            nq.nqResumePopStateWatcher()
        }
    }
    ;
    this.nqCleanURL = function(b) {
        return b
    }
    ;
    this.nqCheckResize = function() {
        var d = false;
        if (typeof nqDataLayer !== "undefined") {
            if (nqDataLayer !== null) {
                if (nqDataLayer.pageType == "category" || nqDataLayer.pageType == "search" || nqDataLayer.pageType == "set") {
                    d = true
                }
            }
        }
        nq.nqRunBespokeFunctions("_CheckResizePre");
        if (d) {
            var b = nq.nqColumns;
            var c = nq.nqGetColumns();
            if (b !== c) {
                nq.nqColumns = c;
                nq.nqSearchApi("", "", true)
            }
        }
        nq.nqRunBespokeFunctions("_CheckResize")
    }
    ;
    this.nqGetColumns = function() {
        var c = nq.nqSettings.nqColumns;
        var d = nq.nqGetData("columns");
        if (d !== "" && d !== undefined) {
            c = d
        }
        if (nq.nqSettings.nqBreakPoints !== undefined) {
            var b = "";
            $.each(nq.nqSettings.nqBreakPoints, function(f, e) {
                if (e.MaxWidth !== undefined) {
                    if (e.MinWidth <= $(window).width() && $(window).width() < e.MaxWidth) {
                        b = e
                    }
                } else {
                    if (e.MinWidth <= $(window).width()) {
                        b = e
                    }
                }
            });
            if (c == null) {
                c = ""
            }
            if (b !== "") {
                if (b.AllowedColumns !== undefined) {
                    allowedColumnsArray = b.AllowedColumns.split(",");
                    if (allowedColumnsArray.indexOf(c.toString()) === -1) {
                        c = b.DefaultColumns
                    }
                }
            }
        }
        nq.nqSettings.nqColumns = c;
        return c
    }
    ;
    this.getQuerystringAsString = function(b) {
        if (b !== null && b !== undefined) {
            return b
        }
        return window.location.search
    }
    ;
    this.nqCreateCookie = function(e, f, c) {
        var d = "";
        if (c) {
            var b = new Date();
            b.setTime(b.getTime() + (c * 24 * 60 * 60 * 1000));
            d = "; expires=" + b.toGMTString()
        }
        f = window.btoa(f);
        document.cookie = e + "=" + f + d + "; path=/;domain=" + nq.nqSettings.nqCookieDomain + ""
    }
    ;
    this.nqReadCookie = function(h, b) {
        var j = h + "=";
        var e = document.cookie.split(";");
        for (var g = 0; g < e.length; g++) {
            var d = e[g];
            while (d.charAt(0) === " ") {
                d = d.substring(1, d.length)
            }
            if (d.indexOf(j) === 0) {
                var f = d.substring(j.length, d.length);
                if (f !== null && f !== "" && f !== undefined) {
                    if (b == true) {
                        f = f
                    } else {
                        f = window.atob(f)
                    }
                    return f
                }
            }
        }
        return null
    }
    ;
    this.nqProductClick = function(e) {
        if (nq.nqRunBespokeFunctions("_ProductClick", e)) {
            $nqProductPosition = $(e).attr("data-nq-listing-position");
            var d = $(e).attr("data-nq-product");
            $inObject = $(e).parents(".nuqlium").parent();
            if (typeof $inObject !== "undefined") {
                var f = {};
                if ($inObject.attr("id") == "nuqlium-container") {
                    if (typeof nqDataLayer !== "undefined") {
                        if (nqDataLayer !== null) {
                            f.type = nqDataLayer.pageType;
                            f.key = nqDataLayer.pageKey;
                            if (nqDataLayer.pageType === "search" && nqDataLayer.pageKey.indexOf("[image:") > -1) {
                                f.type = "visual"
                            }
                            f.value = nqDataLayer.pageValue;
                            f.campaign = $inObject.attr("data-nq-campaign");
                            f.variation = $inObject.attr("data-nq-variation");
                            f.productid = d;
                            if (typeof $nqProductPosition !== "undefined") {
                                f.position = $nqProductPosition
                            }
                        }
                    }
                    var c = $("#nuqlium-container").prop("outerHTML");
                    var b = {};
                    b.pageInstance = nq.nqSettings.nqPageInstance;
                    b.html = c;
                    b.type = nqDataLayer.pageType;
                    b.key = nqDataLayer.pageKey;
                    b.value = nqDataLayer.pageValue;
                    if (typeof $nqProductPosition !== "undefined") {
                        b.position = $nqProductPosition
                    }
                    b.scroll = window.pageYOffset;
                    b.manifest = nq.nqLastManifest;
                    b.tracking = nq.nqLastTracking;
                    b.userfilters = nq.nqLastUserFilters;
                    window.localStorage.setItem("nuqlium", JSON.stringify(b))
                } else {
                    if ($inObject.attr("id") == "nq-predictive-search") {
                        f.type = "predictive";
                        f.key = $inObject.attr("data-nq-predictive");
                        f.campaign = $inObject.attr("data-nq-campaign");
                        f.variation = $inObject.attr("data-nq-variation");
                        f.productid = d;
                        if (typeof $nqProductPosition !== "undefined") {
                            f.position = $nqProductPosition
                        }
                    } else {
                        if (typeof $inObject.attr("data-nq-recommendations") !== "undefined") {
                            f.type = "recommendations";
                            f.key = $inObject.attr("data-nq-recommendations")
                        }
                        if (typeof $inObject.attr("data-nq-feed") !== "undefined") {
                            f.type = "feed";
                            f.key = $inObject.attr("data-nq-feed")
                        }
                        f.productid = d;
                        f.campaign = $inObject.attr("data-nq-campaign");
                        f.variation = $inObject.attr("data-nq-variation");
                        if (typeof $nqProductPosition !== "undefined") {
                            f.position = $nqProductPosition
                        }
                    }
                }
            }
            cookieReadSources = nq.nqReadCookie("nqsources");
            if (cookieReadSources !== null && cookieReadSources !== "" && cookieReadSources !== "undefined") {
                nqCookieSources = JSON.parse(cookieReadSources);
                nqCookieSources.unshift(f);
                nq.nqCreateCookie("nqsources", JSON.stringify(nqCookieSources), 31)
            } else {
                nqCookieSources = [];
                nqCookieSources.push(f);
                nq.nqCreateCookie("nqsources", JSON.stringify(nqCookieSources), 31)
            }
            $nqProductPositionPage = $(e).parents("[data-nq-page]").attr("data-nq-page");
            if (typeof $nqProductPositionPage !== "undefined") {
                nq.UpdatePageInURL($nqProductPositionPage)
            }
        }
    }
    ;
    this.nqPausePopStateWatcher = function() {
        nq.nqTriggered = true
    }
    ;
    this.nqResumePopStateWatcher = function() {
        nq.nqTriggered = false
    }
    ;
    this.InitGroup = function(e) {
        var f = $(e).closest("[data-nq-product]");
        if (f.attr("data-nq-product") !== $(e).attr("data-nq-group-productid")) {
            var d = $(e).attr("data-nq-group-template");
            var c = $(e).attr("data-nq-group-identifier");
            var b = {};
            if (d !== undefined) {
                b.template = d
            }
            if (c !== undefined) {
                b.identifier = c
            }
            nq.nqInitApi("group", "", $(e).attr("data-nq-group-productid"), f, false, b)
        }
    }
    ;
    this.nqGroupSwitch = function(b) {
        productGroup = $(b).attr("data-nq-group");
        $container = $(b).closest(".nuqlium");
        $.each($(b).get(0).attributes, function(d, c) {
            if (c.name.substring(0, 14) === "data-nq-group-") {
                $element = $container.find("[data-nq-product='" + productGroup + "'] [" + c.name.replace("-group-", "-product-") + "]");
                if ($element.length > 0) {
                    switch ($element.prop("tagName").toLowerCase()) {
                    case "img":
                        $element.attr("src", c.value);
                        break;
                    case "a":
                        $element.attr("href", c.value);
                        break;
                    default:
                        $element.html(c.value);
                        break
                    }
                }
            }
        });
        nq.nqRunBespokeFunctions("_GroupSwitch")
    }
    ;
    this.nqGetUrlVars = function() {
        var e = [], b;
        if (window.location.href.indexOf("?") > -1) {
            var c = window.location.href.slice(window.location.href.indexOf("?") + 1).split("&");
            for (var d = 0; d < c.length; d++) {
                b = c[d].split("=");
                urlKey = b[0];
                urlValue = nq.nqStripAnchorTag(b[1]);
                e.push(urlKey);
                e[urlKey] = urlValue
            }
        }
        return e
    }
    ;
    this.nqCookieKeys = function(e) {
        var f = [], b;
        var c = e.split("&");
        for (var d = 0; d < c.length; d++) {
            b = c[d].split("=");
            urlKey = b[0];
            urlValue = b[1];
            f.push(urlKey);
            f[urlKey] = urlValue
        }
        return f
    }
    ;
    this.nqStripAnchorTag = function(b) {
        if (typeof b !== "undefined") {
            if (b.indexOf("#") > -1) {
                valArray = b.split("#");
                return valArray[0]
            }
        }
        return b
    }
    ;
    this.UpdatePageInURL = function(c) {
        if (c !== undefined) {
            var b = document.location.href;
            if (b.indexOf("page=") > -1) {
                b = nq.nqRemoveURLParameter(b, "page")
            }
            var d = "";
            if (c != 1 && c != "1") {
                d = "&page=" + c
            }
            nq.nqUpdateURL(b + d)
        }
    }
    ;
    this.nqGetQSParams = function(c) {
        var f = "";
        var e = nq.nqGetUrlVars();
        var d = c.split(",");
        for (var b = 0; b < d.length; b++) {
            if (e[d[b]] !== "" && e[d[b]] !== undefined) {
                if (f !== "") {
                    f = f + "&"
                }
                f = f + d[b] + "=" + e[d[b]]
            }
        }
        return f
    }
    ;
    this.nqGetDataIndexSettings = function() {
        nq.nqDataIndex = nq.nqSettings.nqDataIndexes[0].Index;
        var b = 0;
        if (nq.nqSettings.nqDataIndexes[b].QueryStrings !== undefined) {
            nq.nqSettings.nqQueryStrings = nq.nqSettings.nqDataIndexes[b].QueryStrings
        }
        if (nq.nqSettings.nqDataIndexes[b].PredictiveInput !== undefined) {
            nq.nqSettings.nqPredictiveInput = nq.nqSettings.nqDataIndexes[b].PredictiveInput
        }
        if (nq.nqSettings.nqDataIndexes[b].DefaultPaging !== undefined) {
            nq.nqSettings.nqPaging = nq.nqSettings.nqDataIndexes[b].DefaultPaging
        }
        if (nq.nqSettings.nqDataIndexes[b].DynamicFiltering !== undefined) {
            nq.nqSettings.nqDynamicFiltering = nq.nqSettings.nqDataIndexes[b].DynamicFiltering
        }
        if (nq.nqSettings.nqDataIndexes[b].FilterFavourites !== undefined) {
            nq.nqSettings.nqFilterFavourites = nq.nqSettings.nqDataIndexes[b].FilterFavourites
        }
        if (nq.nqSettings.nqDataIndexes[b].SearchUrl !== undefined) {
            nq.nqSettings.nqSearchUrl = nq.nqSettings.nqDataIndexes[b].SearchUrl
        }
        if (nq.nqSettings.nqDataIndexes[b].BreakPoints !== undefined) {
            nq.nqSettings.nqBreakPoints = nq.nqSettings.nqDataIndexes[b].BreakPoints
        }
        if (nq.nqSettings.nqDataIndexes[b].Universal !== undefined) {
            nq.nqSettings.nqUniversal = nq.nqSettings.nqDataIndexes[b].Universal
        }
        if (nq.nqSettings.nqDataIndexes[b].CookeDomain !== undefined) {
            nq.nqSettings.nqCookieDomain = nq.nqSettings.nqDataIndexes[b].CookeDomain
        }
        if (nq.nqSettings.nqDataIndexes[b].DynamicPlacements !== undefined) {
            nq.nqSettings.nqDynamicPlacements = nq.nqSettings.nqDataIndexes[b].DynamicPlacements
        }
        if (nq.nqSettings.nqDataIndexes[b].PredictiveTimeout !== undefined) {
            nq.nqSettings.nqPredictiveTimeout = nq.nqSettings.nqDataIndexes[b].PredictiveTimeout
        }
    }
    ;
    this.nqCheckDataIndex = function(c, b) {
        if (b !== "") {
            c += "&dataindex=" + b
        }
        return c
    }
    ;
    this.nqRemoveURLParameter = function(f, c) {
        var g = f.split("?");
        if (g.length >= 2) {
            var e = encodeURIComponent(c) + "=";
            var d = g[1].split(/[&;]/g);
            for (var b = d.length; b-- > 0; ) {
                if (d[b].lastIndexOf(e, 0) !== -1) {
                    d.splice(b, 1)
                }
            }
            f = g[0] + (d.length > 0 ? "?" + d.join("&") : "");
            return f
        } else {
            return f
        }
    }
    ;
    this.nqHidePredictive = function() {
        if (nq.nqRunBespokeFunctions("_nqHidePredictive")) {
            $("#nq-predictive-search").fadeOut();
            $("#nq-overlay-search").fadeOut()
        }
    }
    ;
    this.nqShowPredictive = function() {
        if (nq.nqRunBespokeFunctions("_nqShowPredictive")) {
            $("#nq-overlay-search").fadeIn();
            $("#nq-predictive-search").fadeIn()
        }
    }
    ;
    this.nqProcessGlobal = function(b, d, c) {
        nqQSParams = nq.nqGetQSParams(nq.nqSettings.nqQueryStrings);
        if (b === undefined) {
            $dataUpdated = b
        } else {
            if (nqQSParams !== "") {
                $dataUpdated = b.replace(new RegExp("\\?nq.params","g"), "?" + nqQSParams);
                $dataUpdated = $dataUpdated.replace(new RegExp("\\&nq.params","g"), "&" + nqQSParams)
            } else {
                $dataUpdated = b.replace(new RegExp("\\?nq.params","g"), "");
                $dataUpdated = $dataUpdated.replace(new RegExp("\\&nq.params","g"), "")
            }
        }
        return $dataUpdated
    }
    ;
    this.nqProcessContext = function(b) {
        b.timewindow = nq.nqProcessContext_TimeWindow();
        if (nq.nqSettings.nqUniversal != "") {
            var n = nq.nqSettings.nqUniversal;
            var m = "";
            var o = "";
            if (n.indexOf("[") > -1) {
                universalCookieNameArray = n.split("[");
                n = universalCookieNameArray[0];
                m = universalCookieNameArray[1].replace("]", "")
            }
            try {
                o = nq.nqReadCookie(n, true)
            } catch (c) {
                nq.nqLog("Unable to read universal cookie")
            }
            if (o != "") {
                if (m != "") {
                    try {
                        var p = nq.nqCookieKeys(o);
                        o = p[m]
                    } catch (c) {
                        o = ""
                    }
                }
            }
            if (typeof o != "undefined" && o != "" && o != null) {
                b.id = o.toLowerCase()
            }
        }
        var e = window.localStorage.getItem("nuqlium.variables");
        if (e !== undefined && e !== "" && e !== null) {
            try {
                var f = JSON.parse(e);
                if (f != null) {
                    if (b.variables == undefined) {
                        b.variables = []
                    }
                    for (var g in f) {
                        var l = false;
                        for (var d in b.variables) {
                            if (b.variables[d].key == g) {
                                l = true;
                                b.variables[d].value = f[g]
                            }
                        }
                        if (l == false) {
                            var h = {};
                            h.key = g;
                            h.value = f[g];
                            b.variables.push(h)
                        }
                    }
                }
            } catch (c) {
                nq.nqLog("Unable to read local storage for nuqlium.variables")
            }
        }
        var j = window.localStorage.getItem("nuqlium.segments");
        if (j !== undefined && j !== "" && j !== null) {
            try {
                var k = JSON.parse(j);
                if (k != null) {
                    if (b.segments == undefined) {
                        b.segments = []
                    }
                    for (var g in k) {
                        var l = false;
                        for (var d in b.segments) {
                            if (b.segments[d] == k[g]) {
                                l = true
                            }
                        }
                        if (l == false) {
                            b.segments.push(k[g])
                        }
                    }
                }
            } catch (c) {
                nq.nqLog("Unable to read local storage for nuqlium.segments")
            }
        }
        return b
    }
    ;
    this.nqClone = function(b) {
        if (b !== null && b !== undefined) {
            return JSON.parse(JSON.stringify(b))
        }
        return null
    }
    ;
    this.nqGenerateGuid = function() {
        var b = new Date().getTime();
        var c = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(d) {
            var e = (b + Math.random() * 16) % 16 | 0;
            b = Math.floor(b / 16);
            return (d == "x" ? e : (e & 3 | 8)).toString(16)
        });
        return c
    }
    ;
    this.nqReturnNullIfBlank = function(b) {
        if (b == undefined || b == null) {
            return null
        }
        return b
    }
    ;
    this.nqImageCapture = function() {
        var b = document.createElement("input");
        b.type = "file";
        b.id = "nq-camera-input";
        b.setAttribute("class", "hidden");
        document.body.appendChild(b);
        var c = document.querySelector("#nq-camera-input");
        c.addEventListener("change", function() {
            var d = b.files[0];
            if (d.size > 10000000) {
                alert("Maximum file size is 10MB, please choose a smaller image or reduce your camera resolution")
            } else {
                nq.nqImageCaptureApi(d)
            }
        });
        c.click()
    }
    ;
    this.nqImageCaptureDragDrop = function(c, b) {
        if (nq.nqRunBespokeFunctions("_nqImageCaptureDragDrop", c, b)) {
            b.preventDefault();
            b.stopPropagation();
            switch (b.type) {
            case "dragover":
            case "dragenter":
                $(c).addClass("nq-camera-drag");
                break;
            case "dragleave":
            case "dragend":
                $(c).removeClass("nq-camera-drag");
                break;
            case "drop":
                $(c).removeClass("nq-camera-drag");
                droppedFiles = b.originalEvent.dataTransfer.files;
                nq.nqImageCaptureApi(droppedFiles[0]);
                break
            }
        }
    }
    ;
    this.nqImageCaptureApi = function(b) {
        if (nq.nqRunBespokeFunctions("_nqImageCaptureApi", b)) {
            if (b.type.match(/image.*/)) {
                var c = new FileReader();
                c.onload = function(e) {
                    var d = new Image();
                    d.onload = function(h) {
                        var j = d;
                        var f = document.createElement("canvas");
                        var l = 3000;
                        var k = 3000;
                        if (j.height > k && d.width > l) {
                            var m = Math.min(l / j.width, k / j.height);
                            var n = j.width * m + 0.5 | 0;
                            var g = j.height * m + 0.5 | 0;
                            f.width = n;
                            f.height = g;
                            f.getContext("2d").drawImage(j, 0, 0, n, g);
                            f.toBlob(function(o) {
                                var p = new File([o],b.name,b);
                                nq.nqImageCaptureSend(p)
                            })
                        } else {
                            nq.nqImageCaptureSend(b)
                        }
                    }
                    ;
                    d.src = e.target.result
                }
                ;
                c.readAsDataURL(b)
            }
        }
    }
    ;
    this.nqImageCaptureSend = function(b, d) {
        if (nq.nqRunBespokeFunctions("_nqImageCaptureSend", b, d)) {
            var e = nq.nqDataIndex;
            if (typeof nqDataLayer.dataindex !== "undefined" && nqDataLayer.dataindex !== null) {
                e = nqDataLayer.dataindex
            }
            var f;
            if (typeof nqDataLayer.meta !== "undefined" && nqDataLayer.meta !== null) {
                f = JSON.stringify(nqDataLayer.meta)
            }
            var c = new FormData();
            if (b !== null && typeof (b) !== "undefined") {
                c.append("file", b)
            }
            if (d !== null && typeof (d) !== "undefined") {
                c.append("imageurl", d)
            }
            c.append("clientid", nq.nqSettings.nqClient);
            c.append("dataindex", e);
            c.append("meta", f);
            if (nq.nqDebug) {
                c.append("debug", "true")
            }
            $.ajax({
                type: "POST",
                url: nq.nqSettings.nqPluginsUrl + "vision/",
                data: c,
                cache: false,
                contentType: false,
                processData: false,
                success: function(g) {
                    nq.nqImageCaptureProcess(g)
                },
                error: function(g) {
                    nq.nqRunBespokeFunctions("_nqImageCaptureSend_Error", g)
                }
            })
        }
    }
    ;
    this.nqRemoveFromArray = function(b, c) {
        removedIndx = b.indexOf(c);
        while (removedIndx > -1) {
            b.splice(removedIndx, 1);
            removedIndx = b.indexOf(c)
        }
        return b
    }
    ;
    this.nqImageCaptureProcess = function(b) {
        nq.nqLog(b);
        if (b.redirect !== undefined) {
            var c = b.redirect;
            c = nq.nqProcessGlobal(c);
            window.location.href = c
        } else {
            nq.nqRunBespokeFunctions("_nqImageCaptureSend_Error", b)
        }
    }
    ;
    this.nqProcessVisualSearch = function(d, c) {
        if (d !== undefined && d !== null) {
            if (Object.keys(d).length > 0) {
                for (var b in d) {
                    var e = " bounds";
                    if (b == c) {
                        e = "bounds-selected"
                    }
                    $("[data-nq-visual-search]").prepend('<div data-nq-action="image" data-nq-value="' + b + '" class="nq-visual-search-bounds ' + e + '" style="left:' + d[b][0] + "%;top:" + d[b][1] + "%;width:" + d[b][2] + "%;height:" + d[b][3] + '%;"></div>')
                }
            }
        }
    }
    ;
    this.nqAddDynamicPlacements = function() {
        $(function() {
            if (typeof nq.nqSettings.nqDynamicPlacements !== undefined) {
                for (var b in nq.nqSettings.nqDynamicPlacements) {
                    var c = nq.nqSettings.nqDynamicPlacements[b];
                    switch (c.Key) {
                    case "zone":
                        divPlacement = '<div data-nq-zone="' + c.Value + '"></div>';
                        break
                    }
                    switch (c.Action) {
                    case "after":
                        $(c.Target).after(divPlacement);
                        break;
                    case "before":
                        $(c.Target).before(divPlacement);
                        break;
                    case "firstchild":
                        $(c.Target).prepend(divPlacement);
                        break;
                    case "lastchild":
                        $(c.Target).append(divPlacement);
                        break;
                    case "replace":
                        $(c.Target).replaceWith(divPlacement);
                        break
                    }
                }
            }
        })
    }
    ;
    this.nqLog = function(b, c) {
        if (nq.nqDebug) {
            console.log(b)
        }
    }
    ;
    this.nqProcessContext_TimeWindow = function(b) {
        var d = new Date();
        var c = d.getHours();
        var e = "";
        switch (c) {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            e = "night";
            break;
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
        case 11:
            e = "morning";
            break;
        case 12:
        case 13:
        case 14:
        case 15:
        case 16:
        case 17:
            e = "afternoon";
            break;
        case 18:
        case 19:
        case 20:
        case 21:
        case 22:
        case 23:
            e = "evening";
            break
        }
        return e
    }
    ;
    this.nqDataIndex100029 = function() {
        this._ProductClick = function(b) {
            if ($(b) !== undefined && $(b).attr("data-ga-track-clicks") == "true") {
                nqGoogleAnalyticsProductClickCallBack(b)
            }
        }
        ;
        this._nqBindEvents = function() {
            if ($('[data-page="product"]').length > 0) {
                console.log("THIS IS PRODUCT PAGE- NO NEED SCROLL")
            } else {
                $(window).scroll(function() {
                    nqGoogleAnalyticsProductsInView()
                })
            }
            $("[data-size-add-to-bag]").off("click").on("click", function(b) {
                b.stopPropagation();
                $sizeObj = $(this).prev().find("span.size-selected");
                if ($sizeObj.length == 0) {
                    $(this).next("[data-error]").fadeIn(100, function() {
                        $(this).text("Please select a size")
                    })
                } else {
                    if ($sizeObj.hasClass("outofstock")) {
                        $(this).next("[data-error]").fadeIn(100, function() {
                            $(this).text("Sorry, Out of stock")
                        })
                    } else {
                        $(this).next("[data-error]").fadeOut(100, function() {
                            $(this).text("")
                        });
                        $productId = $(this).parents("[data-nq-product]").attr("data-nq-product");
                        ajaxAddToBasketSimple($sizeObj.attr("data-size-sku"))
                    }
                }
            });
            $("[data-size-sku]").off("click").on("click", function(b) {
                b.stopPropagation();
                $(this).closest(".sizelist").find("[data-size-sku]").removeClass("size-selected");
                $(this).addClass("size-selected");
                if ($(this).hasClass("outofstock")) {} else {
                    $("[data-error]").fadeOut(100, function() {
                        $(this).text("")
                    })
                }
            });
            $("[data-nq-filtergroup]").off("click").on("click", function() {
                var b = $(this).find("div.subcatfacet").attr("id");
                $("#" + b).addClass("facetopen")
            });
            $('[id^="productDataNav"]>span a, a[data-mobile-next], a[data-mobile-prev]').off("click").on("click", function(b) {
                b.preventDefault()
            })
        }
        ;
        this._AppendHtml = function() {
            nogaps();
            $("#nuqlium-container").addClass("fade-in");
            $("[data-nq-product-image]").addClass("fade-in");
            if ($("#bar-sortfilter").length == 1) {
                if ($(".main").hasClass("withBanner")) {
                    $("#bar-sortfilter").css("top", $(".mastheader").height() + $(".headerBanner").height());
                    $(".main").css("paddingTop", $(".mastheader").height());
                    $(".headerBanner").css("margin-bottom", $("#bar-sortfilter").height())
                } else {
                    $("#bar-sortfilter").css("top", $(".mastheader").height());
                    $(".main").css("paddingTop", $(".mastheader").height() + $("#bar-sortfilter").height())
                }
                if ($(".mastheader").height() + $("#bar-sortfilter").height() == 0) {
                    $(".main").css("paddingTop", "calc(7.5vw + 20px)")
                }
            }
            var b = setTimeout(function() {
                nqGoogleAnalyticsProductsInView()
            }, 1000)
        }
        ;
        this._ProcessData = function(d, f, n, g) {
            nogaps();
            if (d !== undefined && d.html !== undefined) {
                $("[data-size-add-to-bag]").off("click").on("click", function(o) {
                    o.stopPropagation();
                    $sizeObj = $(this).prev().find("span.size-selected");
                    if ($sizeObj.length == 0) {
                        $(this).next("[data-error]").fadeIn(100, function() {
                            $(this).text("Please select a size")
                        })
                    } else {
                        if ($sizeObj.hasClass("outofstock")) {
                            $(this).next("[data-error]").fadeIn(100, function() {
                                $(this).text("Sorry, Out of stock")
                            })
                        } else {
                            $(this).next("[data-error]").fadeOut(100, function() {
                                $(this).text("")
                            });
                            $productId = $(this).parents("[data-nq-product]").attr("data-nq-product");
                            ajaxAddToBasketSimple($sizeObj.attr("data-size-sku"))
                        }
                    }
                });
                $("[data-size-sku]").off("click").on("click", function(o) {
                    o.stopPropagation();
                    $(this).closest(".sizelist").find("[data-size-sku]").removeClass("size-selected");
                    $(this).addClass("size-selected");
                    if ($(this).hasClass("outofstock")) {} else {
                        $("[data-error]").fadeOut(100, function() {
                            $(this).text("")
                        })
                    }
                });
                if ($(".pdp-page .nuqlium").length > 0) {
                    $("#nqSlider1Parent .nuqlium:not(.slick-initialized)").slick({
                        slidesToShow: 2.5,
                        slidesToScroll: 2,
                        speed: 500,
                        prevArrow: "#nqSlider1Parent .left",
                        nextArrow: "#nqSlider1Parent .right"
                    })
                }
                $(".nq-slider:not(.slick-initialized)").each(function(q) {
                    var p = $(this).data("slidecount");
                    if (p == null || p == "") {
                        p = 6
                    }
                    var o = $(this).data("autoslide");
                    if (o == null || o == "") {
                        o = true
                    }
                    $(this).slick({
                        slidesToShow: p,
                        slidesToScroll: p,
                        speed: 1500,
                        autoplay: false,
                        autoplaySpeed: 4000,
                        responsive: [{
                            breakpoint: 1025,
                            settings: {
                                slidesToShow: 4,
                                slidesToScroll: 4
                            }
                        }, {
                            breakpoint: 769,
                            settings: {
                                slidesToShow: 3,
                                slidesToScroll: 3
                            }
                        }, {
                            breakpoint: 737,
                            settings: {
                                slidesToShow: 4,
                                slidesToScroll: 4
                            }
                        }, {
                            breakpoint: 481,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 2
                            }
                        }]
                    })
                });
                $("[data-appslideshow] > div:not(.slick-initialized)").each(function(o) {
                    var q = $(this).parent("div").data("appslideshow");
                    var p = $(this).parent("div").data("apppagenation");
                    if (p == "" || p == null) {
                        p = "false"
                    }
                    $(this).slick({
                        slidesToShow: q,
                        slidesToScroll: 1,
                        speed: 1500,
                        autoplay: false,
                        dots: p
                    })
                });
                if ($("[data-appnav]").length > 0) {
                    appcoverflow()
                }
                if ($(".linkloc-before-nuqlium").length == 1 && $(".linkloc-before-nuqlium").attr("data-nq-link-loc-before-nuqlium") != "true") {
                    $(".linkloc-before-nuqlium").removeClass("hidden").prependTo($("#listing-list"));
                    $(".linkloc-before-nuqlium").attr("data-nq-link-loc-before-nuqlium", "true")
                }
                $("#sitebody").removeClass("mobilemenu");
                $("#nq-overlay-search").off("click").on("click", function() {
                    nq.hidePredictive()
                });
                if ($(".searchdisplaytext").length > 0) {
                    $(".searchdisplaytext").each(function() {
                        var p = $(this).text();
                        var q = document.getElementById("nq-searchINPUT").value.trim();
                        var o = p.toLowerCase().indexOf(q.toLowerCase());
                        if (o >= 0) {
                            $(this).html(p.substr(0, o) + '<span class="fc-brightgreen">' + p.substr(o, q.length) + "</span>" + p.substr(o + q.length, 999))
                        }
                    })
                }
                if (f == "category") {
                    $(document).on("touchend", '[data-nq-action="sort"]', function() {
                        $("html, body").animate({
                            scrollTop: 0
                        }, 500)
                    })
                }
                if (f == "predictive") {
                    hidesearchtextlinks();
                    $(".seach-close").off("click").on("click", function() {
                        $("#nq-predictive-search").hide()
                    })
                }
                if (f == "group") {
                    if (nq._itemContainer !== undefined) {
                        $(" [data-nq-product-image]").css("min-height", nq._itemContainer);
                        $(" [data-nq-product-image]").css("background-color", "#efefef")
                    }
                }
                if (f == "search" && d.manifest.total == 0) {
                    $("#nqSearch").css("min-height", "0");
                    if (IS_MOBILE_SITE) {
                        nq.nqFeedsApi("recommendations", "nq-recommendation-no-search-result-bestseller-mobile")
                    } else {
                        nq.nqFeedsApi("recommendations", "nq-recommendation-no-search-result-bestseller");
                        nq.nqFeedsApi("recommendations", "nq-recommendation-recently-viewed")
                    }
                    if (h != "infinite") {
                        if (!IS_MOBILE_SITE) {
                            $("html,body").animate({
                                scrollTop: $("body").offset().top - 70
                            }, "100")
                        }
                    }
                }
                if (f == "predictive" && d.manifest.total == 0) {
                    nq.nqFeedsApi("recommendations", "nq-recommendation-predictive-search-no-results")
                }
                if (f == "search") {
                    if (h != "infinite") {
                        if (!IS_MOBILE_SITE) {
                            $("html,body").animate({
                                scrollTop: $("body").offset().top - 70
                            }, "100")
                        }
                    }
                }
                if (f == "category") {
                    var m = window.location.href;
                    var l = new URL(m);
                    var h = l.searchParams.get("paging");
                    if (h != "infinite") {
                        if (!IS_MOBILE_SITE) {
                            $("html,body").animate({
                                scrollTop: $("body").offset().top - 70
                            }, "100")
                        }
                    }
                    if (d.manifest.total == 0) {
                        nq.nqFeedsApi("recommendations", "nq-recommendation-no-category-result-bestsellers")
                    }
                    if (IS_MOBILE_SITE) {
                        initListJS()
                    }
                }
                if (f == "pages" || f == "zone") {
                    if ($("#nuqlium-container [data-getnqfeed]").length > 0) {
                        $("#nuqlium-container [data-getnqfeed]").each(function(p) {
                            var o = $(this).data("getnqfeed");
                            nq.nqFeedsApi("feed", o)
                        })
                    }
                }
                if (f == "search" || f == "category") {
                    nqGoogleAnalyticsProductsInView();
                    if (nq.nqLastAction == "" || nq.nqLastAction == "page") {
                        $nqCurrentPage = $(d.html).find("[data-nq-page]");
                        $nqMaxPages = $(d.html).find("[data-nq-maxpages]");
                        if ($nqCurrentPage.length > 0 && $nqMaxPages.length > 0) {
                            nqGooglePLPCallBackScrollDepth($nqCurrentPage.attr("data-nq-page"), $nqMaxPages.attr("data-nq-maxpages"))
                        }
                    }
                }
                $("[data-slideshow]:not(.slick-initialized)").each(function(o) {
                    var p = $(this).data("slideCount");
                    $(this).slick({
                        slidesToShow: p,
                        slidesToScroll: p,
                        speed: 1500,
                        autoplay: true,
                        autoplaySpeed: 4000,
                        responsive: [{
                            breakpoint: 768,
                            settings: {
                                slidesToShow: 3,
                                slidesToScroll: 3
                            }
                        }, {
                            breakpoint: 480,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 2
                            }
                        }]
                    })
                });
                if ($("#bar-sortfilter").length > 0) {
                    stickyElementGap()
                }
                if (nq._filterDivState !== undefined) {
                    $("#waFacetPopup").attr("style", nq._filterDivState)
                }
                if (nq._filterLastSelectID !== undefined) {
                    if ($("#" + nq._filterLastSelectID).find("div.nq-filter").hasClass("checked")) {
                        $("#" + nq._filterLastSelectID).addClass("facetopen")
                    }
                    $("#" + nq._filterLastSelectID).attr("style", nq._filterLastSelected)
                }
            }
            $("[data-nq-filtergroup]").off("click").on("click", function() {
                var o = $(this).find("div.subcatfacet").attr("id");
                $("#" + o).addClass("facetopen")
            });
            $('[id^="productDataNav"]>span a, a[data-mobile-next], a[data-mobile-prev]').off("click").on("click", function(o) {
                o.preventDefault()
            });
            if ($(".app-tabfeed").length) {
                $(document).on("click", ".app-tab-header > [data-tab]", function() {
                    var o = $(this).data("tab");
                    $(this).addClass("selected").siblings("div").removeClass("selected");
                    $('[data-tabcontent="' + o + '"]').removeClass("hidden").siblings("div").addClass("hidden")
                })
            }
            try {
                function j() {
                    $("[data-tabcontent] .nq-sliderx").each(function(o) {
                        $(this).slick("unslick");
                        $(this).slick({
                            slidesToShow: 4,
                            slidesToScroll: 1,
                            speed: 1500,
                            autoplay: false,
                            responsive: [{
                                breakpoint: 1025,
                                settings: {
                                    slidesToShow: 4,
                                    slidesToScroll: 4
                                }
                            }, {
                                breakpoint: 769,
                                settings: {
                                    slidesToShow: 3,
                                    slidesToScroll: 3
                                }
                            }, {
                                breakpoint: 737,
                                settings: {
                                    slidesToShow: 4,
                                    slidesToScroll: 4
                                }
                            }, {
                                breakpoint: 481,
                                settings: {
                                    slidesToShow: 2,
                                    slidesToScroll: 2
                                }
                            }]
                        })
                    })
                }
                $(function() {
                    if ($(".tabfeed").length) {
                        j()
                    }
                });
                if ($(".tabfeed").length) {
                    $(document).on("click", ".tab-item > [data-tab]", function() {
                        var o = $(this).data("tab");
                        $(this).addClass("selected").siblings("div").removeClass("selected");
                        $('[data-tabcontent="' + o + '"]').removeClass("hidden").siblings("div").addClass("hidden");
                        j()
                    })
                }
            } catch (e) {
                console.log("Slick Slider :", e)
            }
            var b = dataLayer[0].eliteURL;
            var k = true;
            if (window.location.pathname === "/brands/nike/" || window.location.pathname === "/brands/adidas/") {
                $("#nq-category-header-content").hide()
            }
            function c() {
                if (sessionStorage.getItem("plp") === b) {
                    $("#nq-category-header-content").css("height", "250px");
                    $("#nq-category-header-content").css("overflow", "hidden");
                    $("#nq-category-header-content").css("position", "relative");
                    $(".view-creative").css("display", "block")
                } else {
                    $("#nq-category-header-content").css("height", "100%");
                    $(".view-creative").css("display", "none")
                }
            }
            if (k) {
                $("#nq-category-header-content").append("<style>#nq-category-header-content .view-creative{display: none;position: absolute;z-index: 20;bottom: 0px;left: 0px;width: 100%;padding: 30px;text-decoration: underline;background: rgb(255,255,255);background: linear-gradient(0deg, rgba(255,255,255,1) 14%, rgba(255,255,255,0.7637429971988796) 59%, rgba(255,255,255,0) 100%);	}</style>");
                $("#nq-category-header-content").append('<span class="view-creative">View More</span>');
                c();
                k = false
            }
            $(".nq-filter").on("click", function() {
                sessionStorage.setItem("plp", b);
                c()
            });
            $(".view-creative").on("click", function() {
                sessionStorage.setItem("plp", "active");
                console.log("click");
                c()
            });
            if ($(".nqnosearchresultfeeds").length > 0) {
                $(document).on("click", "[data-nsrtabheading]", function() {
                    var o = $(this).data("nsrtabheading");
                    $(this).addClass("selected").siblings("span").removeClass("selected");
                    $(this).parent().parent().next().find('[data-nsrtab="' + o + '"]').removeClass("invisible").siblings("div").addClass("invisible")
                })
            }
        }
        ;
        this._InitApiPre = function() {
            nq._filterDivState = $("#waFacetPopup").attr("style");
            var b = $(".subcatfacet.facetopen").attr("id");
            nq._filterLastSelected = $(".subcatfacet.facetopen").attr("style");
            nq._filterLastSelectID = b;
            nq._itemContainer = $("[data-nq-product] [data-nq-product-image]").height()
        }
        ;
        this._nqImageCaptureBound = function() {
            showVisualSearchLightbox()
        }
        ;
        this._nqImageCaptureApi = function() {
            imageSearchRunning()
        }
        ;
        this._nqImageCaptureSend = function(b, c) {
            if (c !== null && typeof (c) !== "undefined") {
                imageSearchRunning()
            }
        }
        ;
        this._nqImageCaptureSend_Error = function(b) {
            $(".camera-text").html(b.responseJSON)
        }
    }
}
;