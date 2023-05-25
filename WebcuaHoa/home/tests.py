from django.test import TestCase , SimpleTestCase
class SimpleTest(SimpleTestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assert_(response.status_code, 200)

# Create your tests here.
