var mysql = require('mysql');
var config = require('./config');

module.exports = {
	query: async function(sql, params, callback) {
		return new Promise(function(resolve, reject) {
			var connection = mysql.createConnection(config.database);
			connection.connect(function(err) {
				if (err) {
					console.log('Failed to open database');
					throw err;
				}

				connection.query(sql, params, function(err, results, fields) {
					if (err) {
						console.log('Failed to query database');
						throw err;
					}

					callback && callback(results, fields);

					connection.end(function(err) {
						if (err) {
							console.log('Failed to close database');
							throw err;
						}
					});					
					
					resolve(results);					
				});
			});
		});
	}
};
