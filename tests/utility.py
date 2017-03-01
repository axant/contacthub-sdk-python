class FakeHTTPResponse:
    def __init__(self):
        fake_response = open('tests/util/fake_response', 'r')
        self.text = fake_response.read()