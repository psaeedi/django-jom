'''
Copyright PuzzleDev s.n.c.
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from jom.ajax import AjaxResponse
from jom.factory import JomFactory

@AjaxResponse()
def jom_async_update_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canUpdate(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model.objects.get(
            id = values.get("id"))
    
    #jomInstance = factory.getJomInstance(instance)
    #jomInstance.update(values)
    form = descriptor.update_form(
            request.POST, request.FILES, instance = instance)
    if form.is_valid():
        form.save()
        instance = form.save()
        jomInstance = factory.getJomInstance(instance)
        return True, {'config': jomInstance.instanceToDict()}, ""
    else:
        return False, form._errors, form.non_field_errors()


@AjaxResponse()
def jom_async_create_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canCreate(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    form = descriptor.create_form(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save()
        jomInstance = factory.getJomInstance(instance)
        jomInstance.update(values)
        return True, {'config': jomInstance.instanceToDict()}, ""
    else:
        return False, form._errors, form.non_field_errors()
    
    
@AjaxResponse()
def jom_async_delete_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canDelete(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model.objects.get(
            id = values.get("id"))
    
    instance.delete()
    return True, {}, ""


@AjaxResponse()
def jom_async_get_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canGet(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model.objects.get(
            id = values.get("id"))
    
    jomInstance = factory.getJomInstance(instance)
    jomInstance.update(values)
    return True, {'config': jomInstance.instanceToDict()}, ""