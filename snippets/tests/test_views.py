from django.test import TestCase, Client
from django.urls import reverse
from ..models import Snippet
from django.contrib.auth.models import User
from ..serializers import SnippetSerializer
from rest_framework import status
import json
from rest_framework.test import force_authenticate, APIRequestFactory
from ..views import SnippetDetail, SnippetList
 
 
client = Client()
factory = APIRequestFactory()
 
class AllSnippetTest(TestCase):
 
   def setUp(self):
       user = User.objects.create(username='vishal', password='python')
       Snippet.objects.create(title='python', code='Code of python!', owner_id=user.id)
       Snippet.objects.create(title='C++', code='C++ Code', owner_id=user.id)
 
   def test_snippet(self):
       response = client.get(reverse('snippet-list'))
       snippets = Snippet.objects.all()
       serializer = SnippetSerializer(snippets, many=True)
       self.assertEqual(response.data, serializer.data)
       self.assertEqual(response.status_code, status.HTTP_200_OK)
 
 
class SingleSnippetTest(TestCase):
 
   def setUp(self):
       user = User.objects.create(username='vishal', password='python')
       self.python = Snippet.objects.create(title='python', code='Code of python!', owner_id=user.id)
       self.c = Snippet.objects.create(title='C++', code='C++ Code', owner_id=user.id)
 
   def test_single_snippet(self):
       response = client.get(reverse('snippet-detail', kwargs={'pk':self.python.pk}))
       language = Snippet.objects.get(pk=self.python.pk)
       serializer = SnippetSerializer(language)
       self.assertEqual(response.data, serializer.data)
       self.assertEqual(response.status_code, status.HTTP_200_OK)
 
   def test_single_invalid(self):
       response = client.get(reverse('snippet-detail', kwargs={'pk':30}))
       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
 
class CreateNewSnippet(TestCase):
 
   def setUp(self):
       user = User.objects.create(username='vishal', password='python')
       view = SnippetList.as_view()
       self.valid_payload = {
           'title': 'python',
           'code': 'Code of Python!',
           'owner': user
       }
       self.invalid_payload = {
           'title': 'python',
           'code': 'Code of Python!',
           'owner': ''
       }
 
   def test_create_valid(self):
       response = client.get(reverse('snippet-list'), data = json.dumps(self.valid_payload), content_type='application/json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
