 

::call plink.exe -ssh -pw **** -l idc\agentservice hknginx3 cd /tmp;vi 3.TalentSearch.jobsdb.com.access.log;cd /var/log/nginx;cat jobsdb.com.access.log | grep TalentSearch >> .TalentSearch.jobsdb.com.access.log; 

set pscp="D:\Program Files\PuTTY\pscp.exe"
set base=D:\Sycee\ci_jenkins\payment-log\
set confirm="%base%confirm.txt"

call %pscp% -pw **** -l idc\agentservice hknginx3:/var/log/nginx/paymentgateway.access.log %base%hknginx3\  < %confirm%
call %pscp% -pw **** -l idc\agentservice hknginx4:/var/log/nginx/paymentgateway.access.log %base%hknginx4\  < %confirm%
call %pscp% -pw **** -l idc\agentservice hknginx5:/var/log/nginx/paymentgateway.access.log %base%hknginx5\  < %confirm%

call %pscp% -pw **** -l jobsdbid\agentservice idnginx3:/var/log/nginx/paymentgateway.access.log %base%idnginx3/  < %confirm%
call %pscp% -pw **** -l jobsdbid\agentservice idnginx4:/var/log/nginx/paymentgateway.access.log %base%idnginx4/  < %confirm%

call %pscp% -pw **** -l jobsdbth\agentservice thnginx3:/var/log/nginx/paymentgateway.access.log %base%thnginx3/  < %confirm%
call %pscp% -pw **** -l jobsdbth\agentservice thnginx4:/var/log/nginx/paymentgateway.access.log %base%thnginx4/  < %confirm%


::pause & exit