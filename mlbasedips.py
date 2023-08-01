from http.server import SimpleHTTPRequestHandler, HTTPServer 
from urllib import request, error
import pandas as pd 
from pycaret.clustering import *
import urllib.parse
import sys

badwords = ['sleepy', 'drop', 'uid', 'select', 'waitfor', 'delay', 'system', 'union', 'order by', 'group by']
def ExtractFeatures(path):
  path = urllib.parse.unquote(path)
  badwords_count = 0
  single_q = path.count("'")
  double_q = path.count("\"")
  dashes = path.count("--") 
  braces = path.count(" (") 
  spaces = path.count(" ") 
  for word in badwords: 
    badwords_count+=path.count(word)
  lst = [single_q,double_q,dashes,braces,spaces,badwords_count]
  print(lst)
  return pd.DataFrame([lst],columns = ['single_q','double_q','dashes','braces','spaces','badwords'])

http = pd.read_csv(r'./alldata.csv')
clu1 = setup(data=http, normalize=True, numeric_features=['single_q','double_q','dashes','braces','spaces','badwords'], ignore_features=['method','path','body','class'])
kmeans = create_model('kmeans', num_clusters=2)

class SimpleHTTPProxy(SimpleHTTPRequestHandler):
  proxy_routes = {}

  @classmethod
  def set_routes(cls, proxy_routes):
    cls.proxy_routes = proxy_routes
  
  def do_GET(self):
    parts = self.path.split('/')
    print(parts)
    live_data = ExtractFeatures(parts[3])
    result = predict_model(kmeans, data=live_data) #PyCaret function
    print(result['Cluster'][0])
    if (result['Cluster'][0]=="Cluster 1"):
      print("Intrusion Detected")
    if (len(parts)>=2):
      self.proxy_request('http://'+parts[2]+'/')
    else:
      super().do_GET()
  
  def proxy_request(self, url):
    try:
      response = request.urlopen(url)
    except error.HTTPError as e:
      print('err')
      self.send_response_only(e.code)
      self.end_headers()
      return
    self.send_response_only(response.status)
    for name, value in response.headers.items():
      self.send_header(name, value)
    self.end_headers()
    self.copyfile(response, self.wfile)

SimpleHTTPProxy.set_routes({'proxy_route':'http://demo.testfire.net/'})
with HTTPServer(('127.0.0.1',8080), SimpleHTTPProxy) as httpd:
  host, port = httpd.socket.getsockname()
  print(f'Listening on http://{host}:{port}')
  try:
    httpd.serve_forever()
  except KeyboardInterrupt: 
    print('\nKeyboard interrupt received, exiting.')
    sys.exit(0)