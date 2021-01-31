from ctypes import *
import base64
import json

class ClientError(Exception):
    pass

class GoClient(Structure):
    _fields_ = [("r1", c_int), ("r2", c_char_p)]

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

class Session:
    loaded = False
    lib = None
    BROWSER_DICT = dict(chrome=0, firefox=1, ff=1)

    @classmethod
    def load(cls):
        if cls.loaded:
            return

        cls.lib = cdll.LoadLibrary("./tls/ja3.so")
        cls.lib.make_request.argtypes = [c_int32, GoString, GoString, GoString, GoString]
        cls.lib.make_request.restype = c_char_p
        cls.lib.new_client.argtypes = [GoString, c_int32]
        cls.lib.new_client.restype = GoClient

        cls.make_request = cls.lib.make_request
        cls.new_client = cls.lib.new_client

        cls.loaded = True

    def __init__(self, proxy=None, browser="chrome"):
        self.load()
        browser_id = self.BROWSER_DICT.get(browser, 0)
        self.proxy = str.strip(proxy or '')
        proxy = self.convert_string(self.proxy)
        client = self.new_client(proxy, browser_id)
        if client.r2.strip():
            raise ClientError(client.r2)
        self.client_id = client.r1
        #print(self.client_id)
    
    @staticmethod
    def convert_string(string):
        gstring = bytes(string, encoding="utf-8")
        return GoString(gstring, len(gstring))
         
    def request(self, url, method, headers, data=None):
        url = self.convert_string(url)
        if isinstance(headers, dict):
            headers = list(headers.items())
        if not isinstance(headers, list):
            raise AttributeError('expected headers to be list or dict')
        headers = json.dumps(headers).encode()
        headers = base64.b64encode(headers).decode()
        headers = self.convert_string(headers)
        method = self.convert_string(method)
        data = self.convert_string(data)
        out = json.loads(self.lib.make_request(self.client_id, url, headers, method, data))
        if out.get("error"):
            raise ClientError(out["error"])
        body = out["body"]
        headers = json.loads(out["headers"])
        status, reason = int(out["status"]), ""
        cookies = out["cookies"]
        new_headers = {}
        
        for header in headers:
            new_headers[header] = headers[header][0]
        
        return Response(body, new_headers, status, reason, cookies)
        
    def get(self, url, headers, data=""):
        return self.request(url, "GET", headers, data)
    
    def post(self, url, headers, data=""):
        return self.request(url, "POST", headers, data)

    def patch(self, url, headers, data=""):
        return self.request(url, "PATCH", headers, data)

    def delete(self, url, headers, data=""):
        return self.request(url, "DELETE", headers, data)
    
    def put(self, url, headers, data=""):
        return self.request(url, "PUT", headers, data)
    
    
class Response:


    
    def __init__(self, text, headers, status, reason, cookies):
        self.text = text
        self.reason = reason
        self.headers = headers
        self.status_code = status
        self.cookies = cookies
        # self.json = json.loads(text)
    
        
    
        
