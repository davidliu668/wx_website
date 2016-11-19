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

        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

        self.rsp_status = 200
        self.rsp_headers = {}
        self.rsp_body = ""

        self.hc = None
        self.rsp = None

        self.https = https
        if https and port == 80:
            self.port = 443

    def set_dst(self, ip, port):
        self.ip = ip
        self.port = port

    def set_url(self, url):
        self.url = url

    def set_method(self, method):
        self.method = method

    def add_header(self, header):
        self.header.update(header)

    def set_body(self, body):
        self.body = body

    def get_status(self):
        return self.rsp_status

    def get_headers(self):
        return self.rsp_headers

    def get_body(self):
        return self.rsp_body

    def get_rsp(self):
        return self.rsp

    def send_and_recv(self, httpcode=200, timeout=10, recv_len=None):
        try:
            if self.method == "POST":
                bodylen = len(self.req_body)
                self.req_headers.update({"Content-Length": bodylen})

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
        except Exception, e:
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
