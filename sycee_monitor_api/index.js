
exports.handler = async (event, context, callback) => {
    console.log('Received event:', JSON.stringify(event, null, 2));
    console.log('Received context:', JSON.stringify(context, null, 2));

    const done = (err, res) => callback(null, res);

    var logs = require('./getLogs');
    var result = await logs.getLogs(event);
    if (result == null) {
        done(false, { "success": false, "message": 'Invalid feature_type' });
    }
    else {
        done(false, { "success": true, "result": result });
    }

};
