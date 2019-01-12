#-*- coding: utf-8 -*-
import httplib
import urllib2
import json
import sys
class dnspod:
    '''
    id 为dnspod 生成token 对应的id
    token 为dnspod token
    domain_id 为dnspod 对应的域名id
    record_id 为主机记录id
    sub_domain 为主机明
    value 为 值
    record_type 为域名类型
    record_line_id 线路id
    '''
    def __init__(self,id,token,domain_id=None,record_id=None,sub_domain=None,value=None,record_type=None,record_line_id=None):
        self.id = id
        self.token = token
        self.domain_id=domain_id
        self.record_id=record_id
        self.sub_domain=sub_domain
        self.value=value
        self.record_type=record_type
        self.record_line_id=record_line_id
    ###获取主域名
    def get_domain_name_list(self):
        url='https://dnsapi.cn/Domain.List'
        post_data='login_token=%s,%s&format=json' %(self.id,self.token)
        req = urllib2.urlopen(url, post_data)
        content = req.read()
        dict = json.loads(content)
        return dict
    ####获取域名详细信息
    def get_domian_info_detail(self):
        url='https://dnsapi.cn/Record.List'
        post_data='login_token=%s,%s&format=json&domain_id=%s' %(self.id,self.token,self.domain_id)
        req = urllib2.urlopen(url, post_data)
        content = req.read()
        dict = json.loads(content)
        return  dict
    def update_domain_info_for_detail(self):
        url='https://dnsapi.cn/Record.Modify'
        post_data='login_token=%s,%s&format=json&domain_id=%s&record_id=%s&sub_domain=%s&value=%s&record_type=%s&record_line_id=%s' \
                  %(self.id,self.token,self.domain_id,self.record_id,self.sub_domain,self.value,self.record_type,self.record_line_id)
        req = urllib2.urlopen(url, post_data)
        content = req.read()
        dict = json.loads(content)
        return dict
    def create_domain(self):
        url='https://dnsapi.cn/Record.Create'
        post_data='login_token=%s,%s&format=json&domain_id=%s&sub_domain=%s&record_type=%s&record_line_id=%s&value=%s' \
                 %(self.id,self.token,self.domain_id,self.sub_domain,self.record_type,self.record_line_id,self.value)
        req = urllib2.urlopen(url, post_data)
        content = req.read()
        dict = json.loads(content)
        return dict
if __name__=='__main__':
    id=    ###添加dnspod账号id
    token=''  ###添加dnspod token
    domain_dict=dnspod(id,token).get_domain_name_list()
    i = 0
    sub_domain_dict={}
    
    while (i < len(domain_dict['domains'])):
         sub_domain_dict[str(domain_dict['domains'][i]['name'])]=domain_dict['domains'][i]['id']
         i += 1
    ####取得域名对应ID
    print sys.argv[1]
    print sub_domain_dict
    domain_id=sub_domain_dict[sys.argv[1]]
    ####获取对应域名下面的子域名
    domain_detail_records=dnspod(id,token,domain_id=domain_id).get_domian_info_detail()
    f=0
    res=''
    txt_tag=0 ###txt 记录tag
    while(f < len(domain_detail_records['records'])):
         print domain_detail_records['records'][f]['type']
         print (domain_detail_records['records'][f]['type'] in "TXT")
         if domain_detail_records['records'][f]['type'] in "TXT":
            if domain_detail_records['records'][f]['name'] == "_acme-challenge":
                 record_id=domain_detail_records['records'][f]['id']
                 sub_domain='_acme-challenge'
                 record_type='TXT'
                 record_line_id=0
                 value=sys.argv[2]
                 print record_id,domain_id
                 res=dnspod(id,token,domain_id=domain_id,record_id=record_id,sub_domain=sub_domain,record_type=record_type,record_line_id=record_line_id,value=value).update_domain_info_for_detail()
                 print res
                 txt_tag=1
      
         f +=1 
    print txt_tag
    if txt_tag == 0:
       ####新增TXT记录
       print "新增TXT 记录"
       sub_domain='_acme-challenge'
       record_type='TXT'
       record_line_id=0
       value=sys.argv[2]
       res=dnspod(id,token,domain_id=domain_id,sub_domain=sub_domain,record_type=record_type,record_line_id=record_line_id,value=value).create_domain()
       print res 
