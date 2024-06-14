from django.test import TestCase
from django.http import HttpResponse


# Create your tests here.
class TestsExistingUrls(TestCase):
    def test_health(self):
        url: str = "/health/"
        request: HttpResponse = self.client.get(url)
        self.assertEqual(request.status_code, 200)
