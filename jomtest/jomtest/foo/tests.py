'''
Created on Jul 30, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from jom.factory import JomFactory
from jom.fields import StringJomField, NumeralJomField, BooleanJomField,\
    DateJomField, UrlJomField

from jomtest.foo.models import SimpleModel
from jomtest.foo.joms import SimpleModelJomDescriptor,\
    ModelWithAllFieldsJomDescriptor



class ExportTestCase(TestCase):
    
    def setUp(self):
        call_command('export_jom')
    
    def tearDown(self):
        call_command('clear_jom')
        
    def testAllJomCreated(self):
        raise NotImplementedError()
    

class JomFactoryTestCase(TestCase):
    
    def setUp(self):
        self.factory = JomFactory()
        
    def tearDown(self):
        self.factory = None
        
    def testRegisterJomDescriptor(self):
        descriptor = self.factory.register(SimpleModelJomDescriptor)
        self.assertTrue(isinstance(descriptor, SimpleModelJomDescriptor))
    
    def testGetForName(self):
        name = SimpleModel.__name__
        descriptor = self.factory.register(SimpleModelJomDescriptor)
        self.assertEqual(descriptor, self.factory.getForName(name))
    
    def testGetForModel(self):
        descriptor = self.factory.register(SimpleModelJomDescriptor)
        self.assertEqual(descriptor, self.factory.getForModel(SimpleModel))
    
    def testGetJomInstance(self):
        instance = SimpleModel.objects.create(name = "foo")
        descriptor = self.factory.register(SimpleModelJomDescriptor)
        self.assertEqual(descriptor,
                self.factory.getJomInstance(instance).descriptor)
        instance.delete()
        
    def testGetJomClass(self):
        descriptor = self.factory.register(SimpleModelJomDescriptor)
        self.assertEqual(descriptor,
                self.factory.getJomClass(SimpleModel).descriptor)
        

class JomDescriptorTestCase(TestCase):
    
    def setUp(self):
        self.factory = JomFactory()
        self.descriptor = self.factory.register(
                ModelWithAllFieldsJomDescriptor)
        
    def tearDown(self):
        self.factory = None
        self.descriptor = None
        
    def testJomFieldsCreated(self):
        fields = self.descriptor.jom_fields
    
        self.assertEqual(StringJomField, fields['slug'])
        self.assertEqual(StringJomField, fields['text'])
        self.assertEqual(StringJomField, fields['char'])
        self.assertEqual(StringJomField, fields['email'])
        self.assertEqual(StringJomField, fields['url'])
        self.assertEqual(StringJomField, fields['comma_separated_integer'])
        
        self.assertEqual(NumeralJomField, fields['integer'])
        self.assertEqual(NumeralJomField, fields['positive_integer'])
        self.assertEqual(NumeralJomField, fields['small_integer'])
        self.assertEqual(NumeralJomField, fields['small_positive_integer'])
        self.assertEqual(NumeralJomField, fields['big_integer'])
        self.assertEqual(NumeralJomField, fields['float'])
        
        self.assertEqual(BooleanJomField, fields['boolean'])
        
        self.assertEqual(DateJomField, fields['date'])
        self.assertEqual(DateJomField, fields['time'])
        self.assertEqual(DateJomField, fields['datetime'])
        
        self.assertEqual(UrlJomField, fields['file'])
        self.assertEqual(UrlJomField, fields['image'])

    
class BackEndTestCase(TestCase):
    
    def setUp(self):
        self.factory = JomFactory.default()
        self.descriptor = self.factory.register(
                SimpleModelJomDescriptor)
        
    def tearDown(self):
        TestCase.tearDown(self)
    
    def testUpdate(self):
        instance = SimpleModel.objects.create(name = "foo")
        print instance.__class__.__name__
        response = self.client.post(
                reverse("jom_async_update_ajax"),
                data = {'model': instance.__class__.__name__,
                 'id': instance.id,
                 'name': "bar"}, 
                content_type = "application/json"
                )
        
        print(response.content)
        instance = SimpleModel.objects.get(id = instance.id)
        self.assertEqual("bar", instance.name)
        instance.delete()