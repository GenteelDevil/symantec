#!/usr/bin/python

from re import match
import requests
import urllib
import time
import sys
import re
import json
from bs4 import BeautifulSoup

#login_url="https://"+ +"/console/apps/sepm"
#login_url_default="https://"+ +":8443/console/apps/sepm"
login_username=""
login_password=""

main_frame = ""
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
    req_1= s.get(default_url_local,proxies={}, cookies=cookies,headers=headers,verify=False)
    soup = BeautifulSoup(req_1.text, 'html.parser')
    csrfToken = soup.find('input', {'id':'csrfToken'})["value"]
    csrfToken=csrfToken.encode("utf-8")
    #2 get init_js
    init_js_url="https://%s:8443/console/scripts/ajaxswing/AjaxSwing_init.js" % server_ip
    req_2 = s.get(init_js_url,proxies={},headers=headers,verify=False)
    for i in req_1.headers["Set-Cookie"].split(";"):
        if "JSESSIONID"  in i :
            JSESSIONID=i
            JSESSIONID=JSESSIONID.encode("utf-8")
            #print JSESSIONID

    #3 get calibrate
    calibrate_data={
        'calibrate':'true',
        'AjaxSwingInitData':'864,969,480,480,480,0,0',
    }
    calibrate_data["csrfToken"]=csrfToken
    req_3=s.post(default_url_local,proxies={},data=calibrate_data,headers=headers,verify=False)
    req_3_2=s.post(default_url_local,proxies={},data=calibrate_data,headers=headers,verify=False)

    #4 get FontCalibrationData
    FontCalibrationData={
        'AjaxSwingInitData':'864,969,480,480,480,0,0',
        'FontCalibrationData':'couriernew,16,1;couriernew,12,1.5741;couriernew,12,1.2593;couriernew,12,1.2593;couriernew,12,1.0494;couriernew,12,1;couriernew,12,1;couriernew,13,1;couriernew,14,1;couriernew,15,1;arial,16,1.0191;arial,12,1.6667;arial,12,1.6162;arial,12,1.2698;arial,12,1.1348;arial,12,1.1429;arial,12,1;arial,13,1;arial,14,1;arial,15,1.0309;timesnewroman,16,1.2682;timesnewroman,12,1.9101;timesnewroman,12,1.7;timesnewroman,12,1.4655;timesnewroman,12,1.405;timesnewroman,12,1.2143;timesnewroman,12,1.1888;timesnewroman,13,1.172;timesnewroman,14,1.1786;timesnewroman,15,1.2102;::couriernew,16,1.0279;couriernew,12,1.9302;couriernew,12,1.5442;couriernew,12,1.5442;couriernew,12,1.2868;couriernew,12,1.103;couriernew,12,1.103;couriernew,13,1.0436;couriernew,14,1.125;couriernew,15,1.0724;arial,16,1.0116;arial,12,1.7031;arial,12,1.5139;arial,12,1.2925;arial,12,1.1474;arial,12,1.1848;arial,12,1.0219;arial,13,1;arial,14,1.0133;arial,15,1.0225;timesnewroman,16,1.0425;timesnewroman,12,1.7754;timesnewroman,12,1.5091;timesnewroman,12,1.302;timesnewroman,12,1.2251;timesnewroman,12,1.0885;timesnewroman,12,1;timesnewroman,13,1.0497;timesnewroman,14,1.0459;timesnewroman,15,1.0197;'
    }
    FontCalibrationData["csrfToken"]=csrfToken
    req_4=s.post(default_url_local,proxies={},data=FontCalibrationData,headers=headers,verify=False)


    #5 login
    # get componentId
    login_data_1={
        'actionString':'/resize/global/1374_932',
        '__Action':'v4',
        '__FastSubmit':'true',
    }
    login_data_1["__csrfToken"]=csrfToken
    req_login_1=s.post(default_url_local_2,data=login_data_1,proxies={},headers=headers,verify=False)
    

    if "componentId" in req_login_1.text:
        result = re.findall("componentId(.*)parentId",req_login_1.text)
        for i in result:
            for j in i.split("\""):
                if "_" in j :
                    componentId=j
                    componentId=componentId.encode("utf-8")
                    main_frame = componentId
                    # print componentId
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
    req_login_2=s.post(default_url_local_2,data=login_data_2,proxies={},headers=headers,verify=False)
    time.sleep(2)
    #get focusedComponentId and SEPMPasswordField
    if "focusedComponentId" in req_login_2.text:
        for i in req_login_2.text.split(","):
            if "focusedComponentId" in i:
                for j in i.split("\""):
                    if "JTextField" in j:
                        JTextField=j
                        JTextField=JTextField.encode("utf-8")
                        # print JTextField
            if "SEPMPasswordField" in i:
                for j in i.split("'"):
                    if "SEPMPasswordField" in j:
                        SEPMPasswordField=j
                        SEPMPasswordField=SEPMPasswordField.encode("utf-8")
                        # print SEPMPasswordField
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
    req_login_3=s.post(default_url_local_2,data=login_data_3,proxies={},headers=headers,verify=False)
    time.sleep(2)

    login_data_4={
    '__Action':'v4',
    '__FastSubmit':'true',
    }
    login_data_4["__csrfToken"]=csrfToken
    login_data_4["actionString"]="/keydown/"+SEPMPasswordField+"/n_13_1"
    login_data_4["storedActions[]"]="/type/"+SEPMPasswordField+"/Admin@123"
    login_data_4=s.post(default_url_local_2,data=login_data_4,proxies={},headers=headers,verify=False)
    time.sleep(10)

    login_data_5= s.get(default_url_local_2,headers=headers,verify=False)
    #print login_data_5.text
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
    
    login_data_6=s.get(PHPSESSID_url,headers=headers,verify=False)
    print "cookies info:"
    print "  cookieTest=true;%s;ssc=1;%s"%(JSESSIONID,PHPSESSID)
    print "BodyInfo:"
    print "  csrfToken=%s" % csrfToken
    print "  MainFrameID=%s" % main_frame
    return csrfToken,componentId

def keep_alive(csrfToken):
    post_url = "https://%s:8443/console/apps/sepm" % server_ip
    data = {
        'keepSessionAlive' : 'true',
        '__Action' : 'ping',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    s.post(post_url, data=data, headers=headers, verify=False)

def upload_file(csrfToken):
    post_url = "https://%s:8443/console/apps/sepm" % server_ip
    # get QuickStart window ID

    data = {
        'actionString' : '/click/QuickStartDialog_1305348633/562_707#n',
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    response_json = s.post(post_url, data=data, headers=headers, verify=False).text
    quick_start_dialog_id = json.loads(response_json)['activeWindowId']
    print quick_start_dialog_id

    # 0. close start window
    print "0. close start window"
    data = {
        'actionString' : '/click/%s/562_707#n' % quick_start_dialog_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    response_json = s.post(post_url, data=data, headers=headers, verify=False).text
    main_frame_id = json.loads(response_json)["activeWindowId"]

    # 1. click admin
    print "1. click Admin"
    # print main_frame_id
    body_data1 = {
        'actionString' : '/click/%s/31_453#n' % main_frame_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : '%s' % csrfToken
    }
    s.post(post_url, data=body_data1, headers=headers, verify=False)

    print "2. click install package"
    data = {
        'actionString' : '/click/%s/113_897#n' % main_frame_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    s.post(post_url, data=data, proxies=proxies, headers=headers, verify=False)
    time.sleep(2)

    print "3. click add package"

    data = {
        'actionString' : '/click/%s/164_615#n' % main_frame_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }

    data_init = {
        'actionString' : '/context/%s/1_1#n' % main_frame_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    s.post(post_url, data=data, proxies=proxies, headers=headers, verify=False).text
    response_json = s.post(post_url, data=data_init, proxies=proxies, headers=headers, verify=False).text
    creat_new_software_dlg_id = json.loads(response_json)['activeWindowId']
    jtext_field_id = json.loads(response_json)['focusedComponentId']


    print jtext_field_id
    print creat_new_software_dlg_id

    '''
    print "4. input package name"
    # click input box
    data = {
        'actionString' : '/click/%s/62_78#n' % creat_new_software_dlg_id,
        'postActions[]' : '/caret/%s/0' % jtext_field_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }

    # input package name
    data = {
        'actionString' : '/noupdate/%s/' % jtext_field_id,
        'storedActions[]' : '/type/%s/thisisatestpackage' % jtext_field_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    s.post(post_url, data=data, proxies=proxies, headers=headers, verify=False)

    print "5. create select file windows"
    data = {
        'actionString' : '/click/%s/293_132#n' % jtext_field_id,
        'storedActions[]' : '/type/%s/thisisatestpackage' % jtext_field_id,
        '__Action' : 'v4',
        '__FastSubmit' : 'true',
        '__csrfToken' : csrfToken
    }
    s.post(post_url, data=data, proxies=proxies, headers=headers, verify=False)




'''
    
if __name__ == '__main__':
    csrfToken,componentId=get_login_sessions()
    upload_file(csrfToken=csrfToken)
    while True:
        time.sleep(1)
        keep_alive(csrfToken=csrfToken)
    
