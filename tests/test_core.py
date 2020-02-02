from mpbox import app
# Importamos a biblioteca de testes
import unittest

class MPBoxTest(unittest.TestCase):

    def setUp(self):
        appp = app.test_client()
        self.response = appp.get('/hi')
    
    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content(self):
        response_str = self.response.data.decode('utf-8')
        self.assertIn("Hi, I'm up!", str(response_str))