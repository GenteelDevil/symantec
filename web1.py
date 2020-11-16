#!/usr/bin/python

import requests
import urllib
import time
import sys
import re
from bs4 import BeautifulSoup

#login_url="https://"+ +"/console/apps/sepm"
#login_url_default="https://"+ +":8443/console/apps/sepm"
login_username=""
login_password=""


#default setting
server_ip = "172.16.226.20"
default_url_local="https://%s:8443/console/apps/sepm?do" % (server_ip)
default_url_local_2="https://%s:8443/console/apps/sepm" % (server_ip)


s = requests.Session()
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate',
    'Content-Type':'application/x-www-form-urlencoded',
}
cookies = {
    'cookieTest':'true',
}
proxies = {
     'http': 'http://127.0.0.1:8080',
     'https': 'http://127.0.0.1:8080',
}


def get_login_sessions():
    #1 get csrfToken and cookies
    req_1= s.get(default_url_local,proxies=proxies,cookies=cookies,headers=headers,verify=False)
    soup = BeautifulSoup(req_1.text, 'html.parser')
    csrfToken = soup.find('input', {'id':'csrfToken'})["value"]
    csrfToken=csrfToken.encode("utf-8")
    #2 get init_js
    init_js_url="https://192.168.20.1:8443/console/scripts/ajaxswing/AjaxSwing_init.js"
    req_2 = s.get(init_js_url,proxies=proxies,headers=headers,verify=False)
    for i in req_1.headers["Set-Cookie"].split(";"):
        if "JSESSIONID"  in i :
            JSESSIONID=i
            JSESSIONID=JSESSIONID.encode("utf-8")
            print JSESSIONID

    #3 get calibrate
    calibrate_data={
        'calibrate':'true',
        'AjaxSwingInitData':'864,969,480,480,480,0,0',
    }
    calibrate_data["csrfToken"]=csrfToken
    req_3=s.post(default_url_local,proxies=proxies,data=calibrate_data,headers=headers,verify=False)
    req_3_2=s.post(default_url_local,proxies=proxies,data=calibrate_data,headers=headers,verify=False)

    #4 get FontCalibrationData
    FontCalibrationData={
        'AjaxSwingInitData':'864,969,480,480,480,0,0',
        'FontCalibrationData':'couriernew,16,1;couriernew,12,1.5741;couriernew,12,1.2593;couriernew,12,1.2593;couriernew,12,1.0494;couriernew,12,1;couriernew,12,1;couriernew,13,1;couriernew,14,1;couriernew,15,1;arial,16,1.0191;arial,12,1.6667;arial,12,1.6162;arial,12,1.2698;arial,12,1.1348;arial,12,1.1429;arial,12,1;arial,13,1;arial,14,1;arial,15,1.0309;timesnewroman,16,1.2682;timesnewroman,12,1.9101;timesnewroman,12,1.7;timesnewroman,12,1.4655;timesnewroman,12,1.405;timesnewroman,12,1.2143;timesnewroman,12,1.1888;timesnewroman,13,1.172;timesnewroman,14,1.1786;timesnewroman,15,1.2102;::couriernew,16,1.0279;couriernew,12,1.9302;couriernew,12,1.5442;couriernew,12,1.5442;couriernew,12,1.2868;couriernew,12,1.103;couriernew,12,1.103;couriernew,13,1.0436;couriernew,14,1.125;couriernew,15,1.0724;arial,16,1.0116;arial,12,1.7031;arial,12,1.5139;arial,12,1.2925;arial,12,1.1474;arial,12,1.1848;arial,12,1.0219;arial,13,1;arial,14,1.0133;arial,15,1.0225;timesnewroman,16,1.0425;timesnewroman,12,1.7754;timesnewroman,12,1.5091;timesnewroman,12,1.302;timesnewroman,12,1.2251;timesnewroman,12,1.0885;timesnewroman,12,1;timesnewroman,13,1.0497;timesnewroman,14,1.0459;timesnewroman,15,1.0197;'
    }
    FontCalibrationData["csrfToken"]=csrfToken
    req_4=s.post(default_url_local,proxies=proxies,data=FontCalibrationData,headers=headers,verify=False)


    #5 login
    # get componentId
    login_data_1={
        'actionString':'/resize/global/1374_932',
        '__Action':'v4',
        '__FastSubmit':'true',
    }
    login_data_1["__csrfToken"]=csrfToken
    req_login_1=s.post(default_url_local_2,data=login_data_1,proxies=proxies,headers=headers,verify=False)
    

    if "componentId" in req_login_1.text:
        result = re.findall("componentId(.*)parentId",req_login_1.text)
        for i in result:
            for j in i.split("\""):
                if "_" in j :
                    componentId=j
                    componentId=componentId.encode("utf-8")
                    print componentId
    else :
        print "not find componentId"
    # get componentId
    login_data_2={
        '__Action':'v4',
        '__FastSubmit':'true',
    }
    login_data_2["__csrfToken"]=csrfToken
    login_data_2["actionString"]="/noupdate/"+componentId+"/"
    login_data_2["storedActions[]"]="/type/"+componentId+"/a"
    req_login_2=s.post(default_url_local_2,data=login_data_2,proxies=proxies,headers=headers,verify=False)
    time.sleep(2)
    #get focusedComponentId and SEPMPasswordField
    if "focusedComponentId" in req_login_2.text:
        for i in req_login_2.text.split(","):
            if "focusedComponentId" in i:
                for j in i.split("\""):
                    if "JTextField" in j:
                        JTextField=j
                        JTextField=JTextField.encode("utf-8")
                        print JTextField
            if "SEPMPasswordField" in i:
                for j in i.split("'"):
                    if "SEPMPasswordField" in j:
                        SEPMPasswordField=j
                        SEPMPasswordField=SEPMPasswordField.encode("utf-8")
                        print SEPMPasswordField
    else:
        print "not find focusedComponentId"

    #just post 
    login_data_3={
    '__Action':'v4',
    '__FastSubmit':'true',
    }
    login_data_3["__csrfToken"]=csrfToken
    login_data_3["actionString"]="/keydown/"+JTextField+"/n_9_1"
    login_data_3["storedActions[]"]="/type/"+JTextField+"/admin"
    req_login_3=s.post(default_url_local_2,data=login_data_3,proxies=proxies,headers=headers,verify=False)
    time.sleep(2)

    login_data_4={
    '__Action':'v4',
    '__FastSubmit':'true',
    }
    login_data_4["__csrfToken"]=csrfToken
    login_data_4["actionString"]="/keydown/"+SEPMPasswordField+"/n_13_1"
    login_data_4["storedActions[]"]="/type/"+SEPMPasswordField+"/Admin@123"
    login_data_4=s.post(default_url_local_2,data=login_data_4,proxies=proxies,headers=headers,verify=False)
    time.sleep(10)

    login_data_5= s.get(default_url_local_2,proxies=proxies,headers=headers,verify=False)
    if "PHPSESSID" in login_data_5.text:
        soup = BeautifulSoup(login_data_5.text, 'html.parser')
        PHPSESSID_url = soup.find('iframe')["src"]
        for i in PHPSESSID_url.split("?"):
            for j in i.split("&"):
                if "PHPSESSID" in j :
                    PHPSESSID=j
                    PHPSESSID=PHPSESSID.encode("utf-8")
    else :
        print "not find PHPSESSID!"
    
    login_data_6=s.get(PHPSESSID_url,proxies=proxies,headers=headers,verify=False)

    print "cookieTest=true;%s;ssc=1;%s"%(JSESSIONID,PHPSESSID)
    return csrfToken,componentId
'''
def init_do():
    post_url_local="https://192.168.20.1:8443/console/apps/sepm?do" 
    data={
        'calibrate':'true',
        'AjaxSwingInitData':'864%2C969%2C480%2C480%2C480%2C0%2C0',
        'csrfToken':'%s',
    }%csrfToken
'''
'''
def upload_packages(csrfToken,componentId):
    #
    csrfToken=csrfToken
    componentId=componentId 
    POST https://192.168.20.1:8443/console/apps/sepm HTTP/1.1
    actionString=%2Fcontext%2FMainFrame_371810894%2F520_437%23n&__Action=v4&__FastSubmit=true&__csrfToken=9MHpxqAKrWBsqKmvNtpe
    '''

    
if __name__ == '__main__':
    csrfToken,componentId=get_login_sessions()
    #upload_packages(csrfToken,componentId)
    


