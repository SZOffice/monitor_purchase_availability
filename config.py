slack = {
    "token": '****',
    "channel": "CAF8QRX4N"     #rc_monitor: C80G17TM1;     test-api: CAF8QRX4N
}

email = {'from_addr': '****', 'receivers': ['****']}


path_katalon_report = r"./logs/TS_RC_AvailabilityOfPackageSelection/{1}/report.csv"

path_nginx_paymentgateway_log = r"./logs/{0}/paymentgateway.access.log"
validate_nginx_paymentgateway_log = r"./logs/log_validate_nginx_paymentgateway_log.json"

nginx_server = {
    "Preview": {
        "HK": [],
        "ID": [],
        "TH": []
    },
    "Production": {
        "HK": ["hknginx3", "hknginx4", "hknginx5"],
        "ID": ["idnginx3", "idnginx4"],
        "TH": ["thnginx3", "thnginx4"]
    }
}

jobsdb_mssql = {'Production': {'HK': {'host': '****', 'user': '****', 'pwd': '****', 'db': '****'}, 'ID': {'host': '****', 'user': '****', 'pwd': '****', 'db': '****'}, 'TH': {'host': '****', 'user': '****', 'pwd': '****', 'db': '****'}}}

aws_sycee_monitor_mysql = {'host': '****', 'user': '****', 'pwd': '****', 'db': '****'}

# step: [category, case_name]
autotest_category = {
    "normal purchase": {
        '1': ['2', 'Test Cases/RC/Purchase/TC_PackageSelection'],
        '2': ['3', 'Test Cases/RC/Purchase/TC_CheckOut']
    }
}
'''
autotest_category["post ad with credit"] = {
    '1': ['1', 'Test Cases/RC/Login/TC_Login'],
    '2': ['1', 'Test Cases/RC/Billing/TC_Purchase_NormalFlow']
}
'''