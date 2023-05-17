import unittest
from flask_testing import TestCase
from your_application import app

class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_upload_endpoint(self):
        tester = app.test_client(self)
        response = tester.get('/upload', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_files_endpoint(self):
        tester = app.test_client(self)
        response = tester.get('/files', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_generate_oauth_headers_endpoint(self):
        tester = app.test_client(self)
        response = tester.post('/generate_oauth_headers', content_type='application/json',
                               json={
                                   "consumer_key": "your_key",
                                   "signing_key": "your_signing_key",
                                   "keystore_password": "your_password",
                                   "uri": "your_uri",
                                   "http_verb": "your_verb",
                                   "json_obj": "your_json_obj"
                               })
        self.assertEqual(response.status_code, 200)

    def test_api_upload_certificate_endpoint(self):
        tester = app.test_client(self)
        response = tester.post('/api/upload_certificate', content_type='multipart/form-data', data={
            'file': (open('your_file.p12', 'rb'), 'your_file.p12')
        })
        self.assertEqual(response.status_code, 200)

    def test_api_get_certificates_endpoint(self):
        tester = app.test_client(self)
        response = tester.get('/api/get_certificates', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_healthcheck_endpoint(self):
        tester = app.test_client(self)
        response = tester.get('/healthcheck', content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
