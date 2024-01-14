
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class QueryViewTests(APITestCase):
    
    def test_query_view_post(self):
        """
        Ensure we can send a query to the QueryView and get a response.
        """
        url = reverse('query')
        data = {'query': '1st Line Treatment for Glaucoma'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

# Run tests using:
# python manage.py test backend
