from django.test import TestCase
 
from ..models import Snippet
from django.contrib.auth.models import User
 
 
class SnippetTest(TestCase):
 
   def setUp(self):
       user = User.objects.create(username='vishal', password='python')
       Snippet.objects.create(title='python', code='Code of python!', owner=user)
       Snippet.objects.create(title='C++', code='C++ Code', owner=user)
  
   def test_snippet_name(self):
       python = Snippet.objects.get(title='python')
       c = Snippet.objects.get(title='C++')
       self.assertEqual(python.get_string(),'Code of python!')
       self.assertEqual(c.get_string(), 'C++ Code')
 
 
