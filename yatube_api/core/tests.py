from django.test import TestCase

UNEXISTING_URL = '/unexisting_page/'


class ViewTestClass(TestCase):
    def test_error_page(self):
        response = self.client.get(UNEXISTING_URL)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
