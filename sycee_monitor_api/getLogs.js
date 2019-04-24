exports.getLogs = function(params) {
    async function getRecord(params) {
		var mysqlHelper = require('./mysqlHelper');
		var sql = "CALL `get_purchase_detail`()";
		var record = await mysqlHelper.query(sql, null, null);
		var result = {
			last_status: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
			statistics: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
		};
		
		for (var i = 0; i < record[2].length; i++) {
			console.log(record[2][i]);
			result["last_status"][record[2][i]["user_journey"]-1] = record[2][i];
		} 
		
		for (var i = 0; i < record[3].length; i++) {
			console.log(record[3][i]);
			result["statistics"][record[3][i]["user_journey"]-1] = record[3][i];
		} 
		
		return result;
	}
 
	var result = getRecord(params);
	return result;
};
