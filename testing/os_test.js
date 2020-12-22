const { v4: uuidv4 } = require('uuid');

var eventId = function() {
    var lastAction = new Date().getTime()
    var session = function() {
        return {
            id: uuidv4(),
            creation: new Date().getTime(),
            lastAction: lastAction,
        };
    }
    return session()
}

var appId = function() {
    return 'live1-offspring_uk'
}

var anId = function() {
    return '1zq87h23spsq1piqndkgle5v317ptwxa16dx1xuk1z3cx'
}

var sessionId = function() {

    var lastAction = new Date().getTime()
    var session = function() {
        return {
            id: uuidv4(),
            creation: new Date().getTime(),
            lastAction: lastAction,
        };
    }
    return session()
}

var version = function() {
    return '20.1.0'
}


var b = {
    eventId: eventId().id, //f.v4()
    appId: appId(), //this.appId
    anId: anId(), //this.anIdProvider.getAnId().id
    sessionId: sessionId().id, //this.session.getId(),
    version: version(), //h.version
    previousOrigin: {
        originQuery: "?fh_secondid=4077324616"
    },
    productId: 4077324616,
    quantity: 1,
};

console.log(b)

// {
    // "eventId":"d84671d0-e3e9-46e6-bd8b-5292f09c294c",
    // "appId":"live1-offspring_uk",
    // "anId":"1zq87h23spsq1piqndkgle5v317ptwxa16dx1xuk1z3cx",
    // "sessionId":"c6e8fdc8-0234-4746-a844-d6ddcf987205",
    // "version":"20.1.0",
    // "previousOrigin":{
        // "originQuery":"?fh_secondid=" + self.pid
    // },
    // "productId":self.pid,
    // "quantity":1,
    // "originQuery":"?fh_secondid=" + self.pid
// }

