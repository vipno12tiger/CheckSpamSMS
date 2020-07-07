import os
import re
import unicodedata


from underthesea import word_tokenize as wt
from pyparsing import unicode



def no_accent_vietnamese(s):
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')


def delFirstWord(string):
    split_string = string.split()
    if len(split_string) <= 1:
        return None
    else:
        res =''
        for i in range(1,len(split_string)):
            if res == '':
                res = split_string[i]
            else:
                res = res + ' ' + split_string[i]
        return res

def findRegex(regex, string):
    res = None
    while string != None:
        flag = re.match(regex,string)
        if flag:
            res = flag[0]
            break
        else:
            string = delFirstWord(string)
    return res

def replaceByRegex(regex_diction, string):
    res = string
    for r_d in regex_diction:
        regex_list = regex_diction.get(r_d)
        for regex in regex_list:
            flag = findRegex(regex,res)
            if flag != None:
                regex_text = r_d + '_text'
                res = res.replace(flag, regex_text,1)
    return res


def Regex_text(string):
    regexs = {
        'hour': ['[0-9]{1,2}(h)[0-9]{1,2}', '[0-9]{1,2}(h)[0-9]*']*5,
        'sending': ['(soan).*(gui).[0-9]{4}', '(soan).*(gui).[0-9]{3}']*5,
        'denined': ['(tc qc)', '(tc).*', '(tc)', '(tcqc)', '(tu choi)', '(tu choi quang cao)', '(tu choi qc)',
                    '(tuchoi qc)', '(tuchoi)'],
        'percent': ['[0-9].*(%)']*5,
        'money': ['[0-9]{1,3}\.*[0-9]*( )(d)','[0-9]{1,3}\.*[0-9]*(d)','[0-9]{1,3}(\.)[0-9]*( )(d)','[0-9]{1,3}(\.)[0-9]*(d)' , '[0-9]{1,3}( )(k|d)', '[0-9]{1,3}(k|d)']*10,
        'contact_number': ['(lh)( )[0-9]{3,12}', '(lh)[0-9]{3,12}','(tb)( )[0-9]{3,12}','[0-9]{3,12}']*5,
        'generation_telecom': ['[2-5]g']*5,
        'data': ['[0-9]*(\.)[0-9]*( )(m|k|g)(b)','[0-9]*( )(m|k|g)(b)','[0-9]*(\.)[0-9]*(m|k|g)(b)','[0-9]*(m|k|g)(b)', 'v[1-9]0', 'd[0-9]{1,2}', '^v$']*5,
        'date': ['[0-9]{1,2}(\/)[0-9]{1,2}(\/)[0-9]{1,4}', '[0-9]{1,2}(\/)[0-9]{1,2}']*5,
        'number': ['[0-9]{1,2}']*10
    }
    return replaceByRegex(regexs, string)

# print(Regex_text('(QC) 08h Khong can Wifi, xem video 100 % 8gb DATA 4G TOC DO CAO 18h03 7 ngay 15/7/2020 tai http://myclip.vn/hay9 voi DV Myclip. Dang ky, soan XN gui 9062 (3.000d/ngay, gia han theo ngay). Chi tiet LH 191218 (3k). Tu choi han cuoi 20/7 QC, soan TC4 gui 199'))


def StandardText(string):
    split_string = string.lower().split(" ")
    res = ""
    for s in split_string:
        pre_res = s
        if "dk" in s:
            pre_res = "register_text"
        elif "vip" in s or "v.i.p" in s:
            pre_res = "vip_text"

        links = ['http', '.vn', '.com', '.ly', '.net']
        for link in links:
            if link in s:
                pre_res = "advancetage_link"

        phones = ['iphone', 'xs' ,'i10','oppo', 'f11', 'f2', 'samsung', 'galaxy', 'note', 'nokia', 'xiaomi', 'redmi', 'huawei']
        for phone in phones:
            if phone in s:
                pre_res = 'phone_text'

        countries = ['malai', 'malay', 'malaysia', 'hongkong', 'trung quoc',
                     'trungquoc','tq', 'dai loan', 'dailoan', 'viet nam', 'vietnam', 'sing', 'singapore',
                     'au', 'my', 'mi', 'lao', 'campuchia', 'canada']
        for country in countries:
            if country in s:
                pre_res = 'country_text'

        telecom_hosts = ['vina', 'vinaphone', 'mobile', 'viettel', 'viettell', 'vietell', 'vt', 'vietnammobile', 'vnpt']
        for telecom_host in telecom_hosts:
            if telecom_host in s:
                pre_res = 'telecom_text'

        social_networks = ['fb', 'face', 'facebook', 'youtube', 'youtobe', 'utobe', 'utube', 'insta', 'ins',
                           'instagram', 'twitter', 'twiter', 'iflix', 'netflix']
        for social_network in social_networks:
            if social_network in s:
                pre_res = 'social_network_text'

        if res == "" :
            res = pre_res
        else:
            res = res + " " + pre_res

    return res


# Loại bỏ các loại dấu câu thừa
def preFix(string):
    trashes = [" ","=", ")", ":", ";", "?", "/", "!", ">", "<", "@", "^", "(", "~", "-", ",", "'", "=))", ":))", "=)",
               ":)", "[", ']', '{', '}', '.', '->', '+', '*', '#']
    no_accent_string = no_accent_vietnamese(string).decode()
    splitString = wt(no_accent_string)
    for trash in trashes:
        while trash in splitString:
            splitString.remove(trash)
            #print(splitString)
    res=""
    if len(splitString) == 1:
        res = splitString[0]
    else:
        for s in splitString:
            splitS = s
            if(res == ""):
                res = splitS
            else:
                res = res + " " + splitS
    r = res.lower()
    # pre_final_res = Regex_text(r)
    # final_res = StandardText(pre_final_res)
    return r


def pre_fix_String(string):
    prefix_string = preFix(string)
    regex_string = Regex_text(prefix_string)
    standard_string = StandardText(regex_string)
    clear_list = ['social_network_text','telecom_text','country_text','register_text','vip_text','advancetage_link','phone_text',
                  'hour_text', 'sending_text', 'denined_text', 'percent_text', 'money_text', 'contact_number_text', 'generation_telecom_text',
                  'data_text', 'date_text', 'number_text']
    split_standard_string = standard_string.split(' ')
    res = ''
    for sss in split_standard_string:
        pre_res = sss
        for cl in clear_list:
            if cl in sss:
                pre_res = cl

        if res == '':
            res = pre_res
        else:
            res = res + ' ' + pre_res
    return res


def load_Data(data_folder):
    text = []
    label = []

    folders = os.listdir(data_folder)
    for folder in folders:
        link_label = data_folder + "\\" + folder
        docs = os.listdir(link_label)

        for doc in docs:
            link_doc = link_label + "\\" + doc
            with open(link_doc, "r", encoding='utf8') as f:
                pre_text = f.read()

            text.append(pre_fix_String(pre_text))
            label.append(folder)

    return [text, label]


# data = load_Data("D:\\Giao trinh + Bai tap\\2019-2020\\2019.2\\PythonProject\\LastPython\\Data")
# print(len(data[0]))
