from ctypes import (
              cdll
            , c_int
            , Structure
            , c_int32
            , c_char_p
            , c_uint32
            , CFUNCTYPE
            , pythonapi
            , sizeof
    )

import base64
import json
import time
from enum import Enum
from .utils import ClientError, GoString, GoClient
from .utils import Fingerprint, Lib, Response

class Session:
    loaded = False
    is_listening = False
    lib = None
    client_id = 0
    BROWSER_DICT = dict(chrome=0, firefox=1, ff=1)

    @classmethod
    def _get_clients(cls):
        return

    def __del__(self):
        if not self.client_id:
            return
        self.lib.lib.delete_client(self.client_id)

    def __init__(self, proxy=None, browser=Fingerprint.CHROME, ja3=None, timeout=20):
        self.lib = Lib()
        self.client_id, self.fingerprint, self.proxy = self.lib.new_client(proxy, browser, ja3, timeout=timeout)
        self.ja3 = ja3
         
    def request(self, method, url, **kw):
        return self.lib.request(self.client_id, method, url, **kw)
        
    def get(self, url, **kw):
        return self.request(url, "GET", **kw)
    
    def post(self, url, **kw):
        return self.request(url, "POST", **kw)

    def patch(self, url, **kw):
        return self.request(url, "PATCH", **kw)

    def delete(self, url, **kw):
        return self.request(url, "DELETE", **kw)
    
    def put(self, url, **kw):
        return self.request(url, "PUT", **kw)
    
