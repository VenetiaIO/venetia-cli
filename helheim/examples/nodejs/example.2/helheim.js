const got = require("got");
const {exec} = require("child_process");
const {CookieJar} = require('tough-cookie');

/* ------------------------------------------------------------------------------- */

function getHelheim(url) {
    let helheim = JSON.parse(
    require('child_process').execSync(
        `python3 getCloudflare.py -u "${url}"`).toString()
    );

    helheim.headers['Accept-Encoding'] = helheim.headers['Accept-Encoding'].replace(', br', '');

    let cookieJar = new CookieJar();
    for (var cookie in helheim.cookies) {
        if (cookie) {
            cookieJar.setCookieSync(`${cookie}=${helheim.cookies[cookie]}`, url);
        }
    }

    let client = got.extend({
        cookieJar:  cookieJar,
        headers: response.headers
    });


    return client;
}
