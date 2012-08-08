'''
Created on Jul 30, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from jom.factory import JomFactory, JomDescriptor 
from jomtest.foo.models import SimpleModel, ModelWithAllFields, ModelWithFK,\
    ModelWithM2M, ModelWithOneToOne

jomFactory = JomFactory.default()

class SimpleModelJomDescriptor(JomDescriptor):
    model = SimpleModel
    
    def canUpdate(self, request):
        return True
    
    def canCreate(self, request):
        return True
    
    def canGet(self, request):
        return True
    
    def canDelete(self, request):
        return True
    
jomFactory.register(SimpleModelJomDescriptor)


class ModelWithAllFieldsJomDescriptor(JomDescriptor):
    model = ModelWithAllFields
    exclude = ('excluded_field',)
    
jomFactory.register(ModelWithAllFieldsJomDescriptor)


class ModelWithFKJomDescriptor(JomDescriptor):
    model = ModelWithFK
    
jomFactory.register(ModelWithFKJomDescriptor)


class ModelWithOneToOneJomDescriptor(JomDescriptor):
    model = ModelWithOneToOne
    
jomFactory.register(ModelWithOneToOneJomDescriptor)


class ModelWithM2MJomDescriptor(JomDescriptor):
    model = ModelWithM2M
    
jomFactory.register(ModelWithM2MJomDescriptor)