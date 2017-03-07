from requests import HTTPError


class FakeHTTPResponse:
    def __init__(self, resp_path='tests/util/fake_response', status_code=200):
        self.resp_path = resp_path
        self.status_code = status_code

    @property
    def text(self):
        if self.status_code == 200:
            fake_response = open(self.resp_path, 'r')
            return fake_response.read()

    def raise_for_status(self):
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = u'%s Client Error' % self.status_code

        elif 500 <= self.status_code < 600:
            http_error_msg = u'%s Server Error' % self.status_code

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)