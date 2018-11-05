#!/usr/bin/env python
# -*- coding:utf-8 _*_
#----------------------------------
# 2014-6-19 1.�����������sug��־�������old_mapper.py; 2.�����ֶ�num,��¼sugʵ��չ������; 3.�޸�sugչ����Ŀ��˳��bug,�ֵ�ĳ�list
# 2014-6-21 1.uidǿ�ƴ�д(��������������Դƥ�䲻��) 2.Ǩ��old_mapper.py�ı���ת������
# 2014-6-22 �쳣����ͳ��(2014-6-19):������ count!=num��830/18407380=0.0045%,sug�޽�� num=0��4058585/18407380=22%
# 2014-6-26 sugչ��list��category���ܰ���|,&,��ǰ����,������ָ�������
# 2014-9-13 sugչ����־��������(2014.9.11,type=hivenew),�����¾�������־:��������¼�����ǰ������ӹ�ϵ�Ķ���ϵ������sug��־�汾�ֶ�response['version']��ÿ��չ��������3���ֶ�:pos(˳��),display_info(������Ϣ),column(�ڼ���)�ܿ�ֵУ��(-)
# 2014-10-28 sug�������:9.10-9.24,ȫ��gb2312;9.25,gb2312,utf8����;9.26-10.27,utf8Ϊ��,�������ӹ�ϵ������gb2312����
#----------------------------------


import sys
#sys.path.append('../chardet')
import re
import func
import os
#import chardet
import zipimport

# local test
#importer = zipimport.zipimporter('chardet.zip')
# hadoop
importer = zipimport.zipimporter('lib/chardet.zip')
chardet = importer.load_module('chardet')

reload(sys)
sys.setdefaultencoding( "utf-8" )



#if __name__ == '__main__':
def main(input):
    # һ���ֶηָ���\t type=hive|hivenew
    format_list = ['time','log_server','tid','type','sysinfo','req1','req2','resp','dt']
    # ע��hive����Ϊ��ʱ���ǲ������ݡ�orlando��2014-5-20
    format_len = len(format_list)
    # �����ֶηָ���\001(��4���ֶ�)
    sub_list = ('sysinfo','req1','req2','resp')
    sysinfo_list = ['aos_version','spend_time']
    req1_list = ['adcode','keyword','keyword_py','keyword_en','query_src','query_type','data_type','geoobj','clientpage','clientfield','category']
    req2_list = ['user_info','diu','user_loc','user_city','language','sessionid','stepid','div','platform']
    # resp ������count��ͷ,����sug�����չʾ�����ֶ�
    resp_list_1_0 = ['name','district','adcode','category','rank','poiid','address','x','y','distance'] 
    # 2014-6-26 ��С��:Sug�ķ��ؽ����������һ��checked�����ֶ�type�����ֶε�ֵ��1,2,3,4,5����ʾpoi�����Ŷȣ�3,4,5��ʾpoi������������,0��ʾδ֪�����Ŷ�, ��6.6�����ߵ�
    resp_list_1_1 = ['name','district','adcode','category','rank','poiid','address','x','y','type','distance'] 
    # 2014-9-12 ������:���Ӹ��ӹ�ϵ �����ֶΣ�pos(���λ��),display_info(������Ϣ),column(��poi��ʾ����)
    resp_list_2_0_father = ['pos','name','district','adcode','category','rank','poiid','address','x','y','type','distance','terminals','ignore_district','display_info','column'] 
    resp_list_2_0_son = ['pos','poiid','shortname','name','x','y','adcode'] # �Ӽ���poi��Ϣչʾ��ʽ 
    resp_list_2_0_son_new = ['pos','name','shortname','adcode','poiid','x','y'] # У������Ӽ����ʽ
    #������վ(����վ)(����վ)|�ӱ�ʡ�����в���|130921|150700|0.327211|BV13D01412|16·;31·;402·|116.769901|38.305694|7667.79
    #resp_list = ['name','district','adcode','category','rank','poiid','address','x','y','x_entr','y_entr','distance']
    resp_len_old = len(resp_list_1_0)
    resp_len_new = len(resp_list_1_1)
    resp_len_father = len(resp_list_2_0_father)
    resp_len_son = len(resp_list_2_0_son)

    out_dict = {'uid':'-','sessionid':'-','stepid':'-','time':'-','position':'-','source':'SUG','action':'-','request':'-','response':'-','cellphone':'-','other':'-'}
    out_list = ['uid','sessionid','stepid','time','position','source','action','request','response','cellphone','other']
    pattern_uid = re.compile(r'^[\w-]+$',re.I)
    pattern_gb = re.compile(r'gb',re.I)
    for line in input:
        # ��ʼ������ṹ 
        position_dict = {}
        request_dict = {}
        response_dict = {}
        cellphone_dict = {}
        other_dict = {}

        arr = [i.strip() for i in line.strip().split('\t')]
        line_len = len(arr)
        if line_len not in (format_len,format_len -1):
            continue
        # chardet 
        new_line = line
        # 2014-10-28 
        coding_result = {}
        coding_name = '-'
        try:
            coding_result = chardet.detect(line)
            coding_name = coding_result['encoding']
            #if coding_name not in ('ascii','utf-8'):
            if pattern_gb.match(coding_name):
                print >>sys.stderr,'coding_name='+coding_name  # GB2312
                new_line = line.decode(coding_name).encode('utf-8')
        except Exception,err:
            print >>sys.stderr,"coding transform error ! (%s => %s) continue" %(str(coding_name),'utf-8')
            coding_name = '-'
            #continue
        # ����ǰ��¼
        '''
        # old_mapper.py�д�
        try:
            line = line.decode('gbk').encode('utf8')
        except Exception,err:
            print >>sys.stderr,'line encoding error(%s) !'%(err)
            continue
        '''
        #arr = [i.strip() for i in line.strip().split('\t')]
        arr = [i.strip() for i in new_line.strip().split('\t')]
        line_len = len(arr)
        # ����������־
        if line_len not in (format_len,format_len -1):
            #func.counter('Count','line length pass',1)
            #print >>sys.stderr,'element number(%s) of line != format_len(%s)\nline=%s'%(line_len,format_len,line)
            continue
        # sug��־�Ϸ�����֤:8���ֶ��ҵ�4����'hive',����hivenew  2014-9-12
        if arr[3] not in ( 'hive', 'hivenew'):
            print >>sys.stderr,'%s not hive or hivenew !\n\t%s'%(arr[3],line)
            continue
        in_dict = dict(zip(format_list,arr))
        version = '-'
        for k in sub_list:
            tmp_list = in_dict[k].split('\001')
            # ͳһ��ֵ'-'
            for i,v in enumerate(tmp_list):
                if v == '':
                    tmp_list[i] = '-'
            tmp_len = len(tmp_list)
            if k == 'resp':
                if in_dict['type'] == 'hive':
	                # 2014-6-26 �����¾�����sug��־(6.7,��С��������type�ֶ�,ÿ��չ�����Դ�10�����ӵ�11��)
	                resp_len = 0
	                if tmp_len % resp_len_new == 1:
	                    version = '1_0' # 2014.5 ��һ��淶����sug��־ 1.0
	                    resp_len = resp_len_new # �°�sug��־ 
	                elif tmp_len % resp_len_old == 1:
	                    version = '1_1' # 2014.6 �ڶ���sug��־(�����ֶ�) 1.1
	                    resp_len = resp_len_old # �ɰ�sug��־ 
	                else: # ������־
	                    print >>sys.stderr,'resp len error ! tmp_len=%s\tin_dict[resp]=%s'%(tmp_len,in_dict['resp'])
	                    func.counter('Count','resp length pass',1)
	                    continue
	                tmp_num = tmp_len / resp_len;
	                response_dict['count'] = tmp_list[0]  # ��һ���ֶ���sug�����
	                response_dict['num'] = tmp_num # 2014-6-19 sugʵ��չ������,�����д���count!=num������:num=0,count������
                        response_dict['version'] = version
	                if tmp_num == 0:
	                    # 2014-6-26 �����޽������
	                    response_dict['result'] = '-'
	                else:
	                    result_list = []
	                    for j in range(1,tmp_len,resp_len):
	                        tmp_seg_list = tmp_list[j:j+resp_len]
	                        # 2014-6-26 sugչ��list��category���ܰ���|,&,��ǰ����,������ָ�������
	                        for i,v in enumerate(tmp_seg_list):
                                    if v == '': # 2014.9.13 ����У��
                                        tmp_seg_list[i] = '-'
                                    else:
	                                tmp_seg_list[i] = v.replace('|','$').replace('&','#') 
	                        tmp_seg_list.insert(0,str(j/resp_len+1))
	                        result_list.append('|'.join(tmp_seg_list))
	                        #result_list.append('\003'.join(tmp_seg_list))
	                    response_dict['result'] = '&'.join(result_list)
	                    #response_dict['result'] = '\002'.join(result_list)
	                in_dict[k] = dict(zip(eval(k+'_list'+'_'+version),tmp_list))
                elif in_dict['type'] == 'hivenew':
                    # 2014-9-12 ������,type=hivenew 9.11 ���ߵ�����־��ʽ(�������ӹ�ϵ)
                    response_len = len(tmp_list)
                    response_dict['count'] = tmp_list[0]
                    response_dict['num'] = response_len - 1 # ʵ��չ����Ŀ(�����ӽڵ�)
                    response_dict['version'] = '2_0'
                    if response_len < 2: # sug�޽��
                        #print >>sys.stderr,'resp string length(%s) error ! --> as no result\n\t%s'%(response_len,repr(in_dict))
                        response_dict['result'] = '-'
                    else: # sug�н��
                        result_list = []
                        # ----------- ��һ��չ�ּ�¼���⴦��(���ܰ������ӹ�ϵ):T1=F[^BS1^CS2^C��^CSm],F������-
                        tmp_f_list = tmp_list[1].split('\002')
			# �����µĸ��ӹ�ϵ�����ֶ����������θ��ӹ�ϵ���ֶ�����1 add by hm.z 20141118
			tmp_clm_list = tmp_f_list[0].split('\004')
			if len(tmp_clm_list)==17:
			    #tmp_clm_list = (tmp_f_list[0].split('\004')[0:12] + tmp_f_list[0].split('\004')[15:2])
			    tmp_clm_list = tmp_clm_list[0:16] 
			    result_list.append('\004'.join(tmp_clm_list))
#			elif len(tmp_clm_list)==16:
#			    tmp_clm_list = tmp_clm_list[0:15]
#			    result_list.append('\004'.join(tmp_clm_list))
			else:
                            result_list.append(tmp_f_list[0])
                        len_tmp_f = len(tmp_f_list)
                        if len_tmp_f == 1:
                            # �Ǹ��ӹ�ϵ�ṹ,T1=F,��������
                            pass
                        elif len_tmp_f == 2:
                            # ���ӹ�ϵ�ṹ,T1=F^BS1^CS2^C��^CSm
                            if tmp_f_list[0] == '-':
                                # ���ڵ�Ϊ��(F='-'),�ӽڵ�ǿ�,��Ҫ����,�ֶ���䣬ͳһ�ֶ���
                                result_list[0] = '\004'.join(['-' for i in xrange(len(resp_list_2_0_father))])
                            # chardet
                            # 2014-10-28 
                            coding_result_1 = {}
                            if not coding_name.startswith('gb'):
                                son_line = tmp_f_list[1]
                                # ���б���û����,�ֲ�ת��(sug�������ӹ�ϵչ��)
                                coding_name_1 = '-'
                                try:
                                    coding_result_1 = chardet.detect(son_line)
                                    coding_name_1 = coding_result_1['encoding']
                                    if pattern_gb.match(coding_name_1):
                                        tmp_f_list[1] = son_line.decode(coding_name_1).encode('utf-8')
                                except Exception,err:
                                    print >>sys.stderr,'son coding_name_1='+str(coding_name_1)
                                    coding_name_1 = '-'
                            # ׷���ӽڵ�:S1,S2,S3---�Ӽ�������С������ʾ,�ֶθ�����ͬ�ڸ�����
                            tmp_s_list = tmp_f_list[1].split('\003')
                            len_tmp_s = len(tmp_s_list)
                            response_dict['son_num'] = len_tmp_s # �Ӽ���չ�ָ���
                            for i in tmp_s_list:
                                j_tmp_list = i.split('\004')
                                j_tmp_list_len = len(j_tmp_list)
                                if j_tmp_list_len != resp_len_son:
                                    print >>sys.stderr,'illegal son sug item:len(%s)!=%s'%(j_tmp_list_len,resp_len_son)
                                    continue
                                # �����Ӽ���poi�ֶ�˳��,�븸�����ֶα��ֻ���һ��
                                # old: ['pos','poiid','shortname','name','x','y','adcode'] 
                                # new: ['pos','name','shortname','adcode','poiid','x','y']
                                result_list.append('\004'.join([j_tmp_list[0],j_tmp_list[3],j_tmp_list[2],j_tmp_list[6],j_tmp_list[1],j_tmp_list[4],j_tmp_list[5]]))
                            #result_list.extend(tmp_f_list[1].split('\003'))
                        else:
                            print >>sys.stderr,'illegal first sug item:len(%s)!=2'%(len_tmp_f)
                            continue
                        # ------------ ����һ��չ����Ŀ
                        result_list.extend(tmp_list[2:])
                        # �ֶηָ�������,������Ź�ܴ���
                        for i,vi in enumerate(result_list):
                            i_tmp_list = vi.split('\004')
	                    for j,vj in enumerate(i_tmp_list):
                                if vj == '': # ��ֵУ��'-'
                                    i_tmp_list[j] = '-'
                                else:
	                            i_tmp_list[j] = vj.replace('|','$').replace('&','#') 
                            result_list[i] = '|'.join(i_tmp_list)
                        response_dict['result'] = '&'.join(result_list)
                else:
                    print >>sys.stderr,'type parse error ! not hive or hivenew !\n%s'%(line)
                    continue
            else:
                in_dict[k] = dict(zip(eval(k+'_list'),tmp_list))
        #print in_dict
        # �ֶ�����
        request_dict.update(in_dict['req1'])
        # 2014-6-19 ȥ��sug������־
        if 'query_src' in in_dict['req1'] and  in_dict['req1']['query_src'] == 'test':
            continue
        request_dict.update(in_dict['req2'])
        request_dict['tid'] = in_dict['tid']
        request_dict['aos_verion'] = in_dict['sysinfo']['aos_version'] if 'aos_version' in in_dict['sysinfo'] else '-'
        response_dict['spend_time'] = in_dict['sysinfo']['spend_time'] if 'spend_time' in in_dict['sysinfo'] else '-'
        #print response_dict
        # uid
        out_dict['uid'] = '-'
        for i in ('user_info','diu'):
            if i in request_dict and request_dict[i] != '-':
                out_dict['uid'] = func.get_value(request_dict,i).upper() # 2014-6-21 sug��uid��ת��д,ͬsp
                break
        if not pattern_uid.match(out_dict['uid']) and out_dict['uid'] != '-':
            func.counter('Count','uid illegal pass',1)
            continue
        # sessionid,stepid
        for i in ('sessionid','stepid'):
            out_dict[i] = func.get_value(request_dict,i)
        # time
        if len(in_dict['time']) == 14:
            date = in_dict['time'][:8]
            time = in_dict['time'][8:10]+':'+in_dict['time'][10:12]+':'+in_dict['time'][12:]
        else:
            date,time = '-','-'
        out_dict['time'] = time
        other_dict['date'] = date
        # position
        for i in ('geoobj','user_loc','user_city'):
            if i == 'geoobj': # [2014-5-21]geoobj�ָ����滻: | --> ;
                position_dict[i] = func.get_value(request_dict,i).replace('|',';')
            else:
                position_dict[i] = func.get_value(request_dict,i)
        out_dict['action'] = func.get_value(request_dict,'query_type')
        # cellphone
        for i in ('div','platform'):
            if i == 'div': # [2014-5-21] div��д
                cellphone_dict[i] = func.get_value(request_dict,i).upper() 
            else:
                cellphone_dict[i] = func.get_value(request_dict,i)

        for i in ('position','request','response','cellphone','other'):
            out_dict[i] = func.dict2str(eval("%s_dict"%(i)))
        print '\t'.join([out_dict[i] for i in out_list])

if __name__ == '__main__':
    main()
