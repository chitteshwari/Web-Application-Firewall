from rawweb import RawWeb
from xml.etree import ElementTree as ET
import urllib.parse
import base64
import csv
from io import StringIO

log_path = 'test_crawl1.log'
output_csv_log = 'test_crawl1.csv'
class_flag = 'good'
class LogParse:
    def __init__(self):
        pass

    def parse_log(self, log_path):
        '''
        This fucntion accepts burp log file path.
        and returns a dict. of request and response
        result = {'GET /page.php...':'200 OK HTTP / 1.1....','':'',.....}
        '''
        result = {}
        try:
            with open(log_path): pass
        except IOError:
            print("[+] Error!!! ",log_path,"doesn't exist..")
            exit()
        try:
            tree = ET.parse(log_path)
        except Exception as e:
            print('[+] Opps..!Please make sure binary data is not present in Log, Like raw image dump,flash(.swf files) dump etc')
            exit()
        root = tree.getroot()
        for reqs in root.findall('item'):
            raw_req = reqs.find('request').text
            raw_req = urllib.parse.unquote(raw_req)
            raw_resp = reqs.find('response').text
            result[raw_req] = raw_resp
        return result

    def parseRawHTTPReq(self, rawreq):
        try:
            raw = rawreq.decode('utf8')
        except Exception as e:
            raw = rawreq
        global headers,method,body,path
        headers = {}
        sp = raw.split('\r\n\r\n',1)
        #print(len(sp), sp[1])
        if sp[1] != "": #checking whether body is empty or not
            head = sp[0]
            body = sp[1]
        else :
            head = sp[0]
            body = ""
        c1 = head.split('\n',head.count('\n'))
        method = c1[0].split(' ',2)[0]
        path = c1[0].split(' ',2)[1]
        for i in range(1, head.count('\n')+1):
            slice1 = c1[i].split(': ',1)
            if slice1[0] != "":
                try:
                    headers[slice1[0]] = slice1[1]
                except:
                    pass
        return headers,method,body,path

badwords = ['sleepy', 'drop', 'uid', 'select', 'waitfor', 'delay', 'system', 'union', 'order by', 'group by']
def ExtractFeatures(method, path_enc, body_enc, headers):
    badwords_count = 0
    path = urllib.parse.unquote_plus(path_enc)
    body = urllib.parse.unquote(body_enc)
    single_q = path.count("'") + body.count("'")
    double_q = path.count("\"") + body.count("\"")
    dashes = path.count("--") + body.count("--")
    braces = path.count(" (") + body.count(" (")
    spaces = path.count(" ") + body.count(" ")
    for word in badwords:
        badwords_count += path.count(word) + body.count(word)
    for header in headers:
        single_q += headers[header].count("'")
        double_q += headers[header].count("\"")
        dashes += headers[header].count("-")
        braces += headers[header].count("(")
        badwords_count += headers[header].count(word) + headers[header].count(word)
    
    return [method, path_enc.strip(), body_enc.strip(), single_q, double_q, dashes, braces, spaces, badwords_count, class_flag]
    raw_input('>>>')

#Open the log file 
f = open(output_csv_log, "w")
c = csv.writer(f)
c.writerow(["method","path","body", "single_q", "double_q", "dashes", "braces", "spaces", "badwords"])
lp = LogParse()
result = lp.parse_log(log_path)
f = open(output_csv_log, "ab")
for items in result:
    raaw = base64.b64decode(items)
    headers,method,body,path = lp.parseRawHTTPReq(raaw)
    result = ExtractFeatures(method, path, body, headers)
    c.writerow(result)
f.close()