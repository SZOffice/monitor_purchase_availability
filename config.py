slack = {
    "token": '********',
    "channel": "*******"     #rc_monitor: C80G17TM1;     test-api: CAF8QRX4N
}

email_receiver = ["******"]

nginx_server = {
    "HK": ["hknginx3", "hknginx4", "hknginx5"],
    "ID": ["idnginx3", "idnginx4"],
    "TH": ["thnginx3", "thnginx4"]
}

aws_mysql = {
    "host": "**********",
    "user": "root",
    "pwd": "****",
    "db": "monitor"
}

# step: [category, case_name]
autotest_category = {
    "normal purchase": {
        '1': ['2', 'Test Cases/RC/Login/TC_Login'],
        '2': ['3', 'Test Cases/RC/Billing/TC_Purchase_NormalFlow']
    },
    "post ad with credit": {
        '1': ['1', 'Test Cases/RC/Login/TC_Login'],
        '2': ['1', 'Test Cases/RC/Billing/TC_Purchase_NormalFlow']
    }
}