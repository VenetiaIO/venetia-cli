/* ------------------------------------------------------------------------------- */

const helheim = require('./helheim');

/* ------------------------------------------------------------------------------- */

(async () => {
    try {
        let url = "https://www.gen-x.co.nz/iuam/";
        let gotClient = helheim.solve(url);
        let response = await gotClient.get(url);
        console.log(response.headers);
        console.log(response.body);
    } catch (error) {
        console.log(error, "error!!!");
    }
})();

/* ------------------------------------------------------------------------------- */
