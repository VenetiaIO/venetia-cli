/* ------------------------------------------------------------------------------- */

const {CookieJar} = require('tough-cookie');
const ffi = require('ffi-napi');
const got = require('got');
const path = require('path');

/* ------------------------------------------------------------------------------- */

const helheim = init_helheim();

/* ------------------------------------------------------------------------------- */

function init_helheim() {
    let __dirname = path.resolve();
    return ffi.Library(
        path.join(__dirname, 'helheim_cffi.so'),
        {
            'getURL': ['string', ['string']]
        },
        ffi.DynamicLibrary(
        path.join(__dirname, 'helheim_cffi.so'),
        ffi.DynamicLibrary.FLAGS.RTLD_NOW | ffi.DynamicLibrary.FLAGS.RTLD_GLOBAL)
    );
}

/* ------------------------------------------------------------------------------- */

function solve(url) {
    let response = JSON.parse(helheim.getURL(url));
    
    cookieJar = new CookieJar();
    
    for (var cookie in response.cookies) {
        if (cookie) {
            cookieJar.setCookieSync(`${cookie}=${response.cookies[cookie]}`, url);
        }
    }
    
    let client = got.extend({
        cookieJar:  cookieJar,
        headers: response.headers
    });
    
    return client;
}

/* ------------------------------------------------------------------------------- */

module.exports = {
    solve: solve
}

