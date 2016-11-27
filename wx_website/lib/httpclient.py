# coding=utf-8
import httplib


class HttpClient:
    '''
    http/https client, only one request and one response
    '''

    def __init__(self, ip, port=80, method="GET", url="", headers={},
                 body="", https=False):
        '''
        Constructor
        '''
        self.ip = ip
        self.port = port

        self.set_method(method)
        self.set_url(url)
        self.headers = {}
        self.set_headers(headers)
        self.set_body(body)

        self.rsp_status = 200
        self.rsp_headers = {}
        self.rsp_body = ""
        self.exception = None

        self.hc = None
        self.rsp = None

        self.https = https
        if https and port == 80:
            self.port = 443

    def set_dst(self, ip, port):
        self.ip = ip
        self.port = port

    def set_url(self, url):
        if isinstance(url, unicode):
            self.url = url.encode('utf-8', 'ignore')
        else:
            self.url = url

    def set_method(self, method):
        if isinstance(method, unicode):
            self.method = method.encode('utf-8', 'ignore')
        else:
            self.method = method

    def set_headers(self, headers):
        str_headers = {}
        for k in headers:
            v = headers[k]
            if isinstance(k, unicode):
                k = k.encode('utf-8', 'ignore')
            if isinstance(v, unicode):
                v = v.encode('utf-8', 'ignore')
            str_headers[k] = v

        self.headers.update(str_headers)

    def add_header(self, header):
        self.header.update(header)

    def set_body(self, body):
        if isinstance(body, unicode):
            self.body = body.encode('utf-8', 'ignore')
        else:
            self.body = body

    def get_status(self):
        return self.rsp_status

    def get_headers(self):
        return self.rsp_headers

    def get_body(self):
        return self.rsp_body

    def get_rsp(self):
        return self.rsp

    def get_exception(self):
        return self.exception

    def send_and_recv(self, httpcode=200, timeout=10, recv_len=None):
        try:
            if self.method == "POST":
                bodylen = len(self.body)
                self.headers.update({"Content-Length": bodylen})

            if self.https:
                self.hc = httplib.HTTPSConnection(self.ip, self.port, timeout=timeout)
            else:
                self.hc = httplib.HTTPConnection(self.ip, self.port, timeout=timeout)

            self.hc.request(self.method, self.url, body=self.body, headers=self.headers)
            self.rsp = self.hc.getresponse()

            self.rsp_status = self.rsp.status
            if self.rsp_status != httpcode:
                return (1, "check http code fail, recv http code:".format(self.rsp_status))

            self.rsp_headers = self.rsp.getheaders()
            self.rsp_body = self.rsp.read(recv_len)

            return (0, self.rsp_body)
        except Exception as e:
            self.exception = e
            return (2, 'http exception, msg:' + str(e))
        finally:
            if self.hc:
                self.hc.close()


if __name__ == "__main__":
    print "begin .."
    url1 = "/cgi-bin/token?grant_type=client_credential&appid=wxe190392b2c7d0c25&secret=39b8e16f4b6e479f204157d953d0aa9b"
    print 'len:', len(url1)
    hc = HttpClient('api.weixin.qq.com', url=url1, https=True)
    (ret, info) = hc.send_and_recv()
    print "ret: ", ret
    print "info: ", info
