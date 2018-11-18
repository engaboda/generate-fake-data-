from django.shortcuts import render
from django.http import  HttpResponse

from django import forms

from django.views.decorators.csrf import csrf_exempt

from django.db.models import fields as model_fields
from django.db.models.fields.files import ImageFieldFile , ImageField
from django.db.models.fields.files import FileField 
from django.db.models.fields import  SlugField


from django.db.models.fields import IntegerField
from django.db.models.fields import CharField
from django.db.models.fields import DateField
from django.db.models.fields import DateTimeField


from django.apps import apps

from .forms import LeadForm

import string

import random

import datetime

# Create your views here.
@csrf_exempt
def duplicate_row(request):

    '''
        duplicate row depend on form of mode *:*
    '''
    id = request.POST.get("item")
    post = []
    post_dict = {}
    many_to_many = []
    file = {}

    model = request.POST.get('model')
    app = request.POST.get('app')
    
    # print(dir(apps))
    models = apps.get_app_config(app)
    
    try:
        lead_str = apps.get_registered_model(app , model)
    except Exception as e :
        return HttpResponse("Page Not found")
    # print(dir(lead_str))
    # lead
    # for item in models.get_models():
    #     # print(dir(item._meta))
    #    if item._meta.model_name == model:
    #         # print(dir(item._meta))
    #         print(dir(item._meta.pk))#still need to get fields name and value*******
    slug = ''
    try:
        # item = Lead.objects.filter(id=id)
        item = lead_str.objects.filter(id=id)
        fields = lead_str._meta.get_fields()# real name like crm.teammemberactivity
        print([dir(x) for x in fields])
        for one in item.iterator():
            # print(type(one.picture))
            # print(dir(one.picture))
            # print( type(one.picture.field) )
            for field in dir(one):
                try:
                    key = one._meta.get_field(field)#keys
                    # print(type(key) , key.get_attname() )
                    # print(dir(key))
                    # print(type(key) , key.get_attname())
                    # if isinstance(key , ImageField):
                    #     file.append({ one.get_attname() : one._meta.__getattribute__(key.get_attname()) })
                    if isinstance( key , (ImageField or FileField) ):#File ):# or  ImageFieldFile)):
                        file[ key.get_attname() ] =  one.__getattribute__(key.get_attname())
                        # print(dir(type(key)) , key.get_attname())
                        # print("file")
                        # post_dict.append({ one.get_attname() : one._meta.__getattribute__(key.get_attname()) })
                    elif isinstance(key , SlugField):
                       
                        position = one.__getattribute__(key.get_attname()).find("-")
                        slug =str(one.__getattribute__(key.get_attname()))[:position]
                        # print(id)
                        slug=slug + "-" +id
                        # print(slug)
                    elif key.many_to_many:
                        # print( dir(one.__getattribute__(key.get_attname())) )
                        many_to_many.append( one.__getattribute__(key.get_attname()) )
                    # elif key.get_attname() == "LEADPicture":
                    #     # print (dir(key))
                    #     pass
                    
                    elif key.get_attname() == 'id': #get_attname() to get real name not refrance type
                        # print(one.id)
                        pass
                    # print(key.get_attname())
                    elif key.is_relation:
                        if {key.get_attname().replace("_id" , ''):one.__getattribute__(key.get_attname())} in post :
                            pass
                        # elif key.get_attname() == 'LEADPicture' or key.get_attname()=='LeadTags_CTTKeyField' or key.get_attname()=='LEADSlug':
                        #     pass
                        else:
                            post_dict[key.get_attname().replace("_id" , '')]=one.__getattribute__(key.get_attname())
                            # post.append( { key.get_attname().replace("_id" , ''): one.__getattribute__(key.get_attname()) }  )                      
                    else:
                        if {key.get_attname():one.__getattribute__(key.get_attname())} in post :
                            pass
                        # elif key.get_attname() == 'LEADPicture' or key.get_attname()=='LeadTags_CTTKeyField' or key.get_attname()=='LEADSlug':
                        #     pass
                        else:
                            # print(key.get_attname())
                            post_dict[key.get_attname()]=one.__getattribute__(key.get_attname())
                            # post.append( { key.get_attname(): one.__getattribute__(key.get_attname()) } )
                except Exception as e:
                    # print(e)
                    # print(e , "inner")
                    pass
            # print(post_dict)
            # print([x for x in post])
            # print(many_to_many)
            # lead = Lead(*post)
            # print("not yet")
            # lead.save()
            # form = LeadForm()
            # print(file)
                    
            form = LeadForm(post_dict , file)
            if form.is_valid():
                form.save()
                
            else:
                print(form.errors)
            
            # print(dir(Lead.objects))
            lead_last = lead_str.objects.last()
            # print(dir(many_to_many[0]))
            many2many=[]
            for many in many_to_many[0].all():
                many2many.append(many)
            lead_last.employee.set( many2many )
            # print(lead_last)
            # print(slug , '14')
            lead_last.RPOSlug=slug
            lead_last.save()
            # lead_last.objects.update(LEADSlug=slug)
            

            url = request.POST.get('url').split("/")
            # print(url)
            str_url  = ''
            current_id =  url[6]
            new_id = lead_str.objects.last()
            new_id = new_id.id
            for part in url:
                if part == "":
                    str_url += "/"
                elif part == current_id:
                    str_url += str(new_id) + "/"
                else:
                    str_url += part+"/"
            # print(str_url[:-1])
    except Exception as e:
        print(e , "outer")
        return HttpResponse(e)
    new_id = int(id)+1
    return HttpResponse(str_url[:-1])


@csrf_exempt
def fake_data(request):
    '''
        duplicate row depend on form of mode *:*
    '''


    model = request.POST.get('model')
    app = request.POST.get('app')

    # models = apps.get_app_config(app)
    # print(dir(apps))
    model_object = apps.get_registered_model(app , model)

    # # Fields 

    #this way i get fields
    #model_object._check_fields() get all Warning 
    # print(dir(model_object._meta))
    # print(model_object._meta.get_fields())
    fields = model_object._meta.get_fields()
    
    # type_of_fields = []  #type of each field in model
    # name_of_fields = []  #name of fields in model
    one_related_models = []
    many_related_models = []
    # name_type_of_field =  {}
    
    post_dict = {}
    slug = ''
    file = {}

    for one in range(5):
        for field in fields:
            # get type of fields
            # type_of_fields.append( type(field) )
            # get name of fields
            # name_of_fields.append(field.name)
            # name_type_of_field[field.name] = type(field)

            if field.many_to_one or field.one_to_many : #still need to handle one_2_one
                print("relation")
                print(field.name)
                print(field.related_model)#that object we can use objects.all() or objects.filter() or objects.get()
                all_data_for_related_model = field.related_model.objects.all()
                all_data_for_related_model_length = len(all_data_for_related_model)
                if all_data_for_related_model_length < 4:
                    create_rows(field.related_model)
                    all_data_for_related_model = field.related_model.objects.all()
                    all_data_for_related_model_length = len(all_data_for_related_model)
                    one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length-1)]
                    # print(one_model_data.id , "many_to_one")
                    post_dict[field.name]=one_model_data.id
                else:
                    all_data_for_related_model = field.related_model.objects.all()
                    all_data_for_related_model_length = len(all_data_for_related_model)
                    one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length-1)]
                    # print(one_model_data.id , "many_to_one")
                    post_dict[field.name]=one_model_data.id
            # if field.many_to_one:
            #     print("many_to_one")
            #     print(field.name)
            #     print(field.related_model)# realted model name
            if field.many_to_many:
                print("many_to_many")
                print(field.name)
                print(field.related_model)# realted model name
                all_data_for_related_model = field.related_model.objects.all()
                all_data_for_related_model_length = len(all_data_for_related_model)
                if all_data_for_related_model_length < 4:
                    create_rows(field.related_model)
                    all_data_for_related_model = field.related_model.objects.all()
                    all_data_for_related_model_length = len(all_data_for_related_model)
                    one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length-1)]
                    many_related_models.append(one_model_data)

                else:
                    one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length-1)]
                    many_related_models.append(one_model_data)

            if isinstance(field , ImageField):
                print("image")
                print(field.name)
                # file[field.name] = "/media/image/Screenshot_from_2018-11-16_16-16-13.png"
            if isinstance(field , CharField ):
                post_dict[field.name]=generate_char_field_data()
            elif isinstance(field , IntegerField):
                post_dict[field.name]=genearte_integer_field()
            elif isinstance(field , DateField):
                print(generate_date_field_data())
                post_dict[field.name]=generate_date_field_data()

                
            # if field.one_to_many:
            #     print(field.name)
            #     print("one_to_many")
            #     print(field.related_model)# realted model name
            # if field.one_to_one:
            #     print(field.name)
            #     print("one_to_many")
            #     print(field.related_model)# realted model name
        form = LeadForm(post_dict)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        slug = generate_char_field_data()
        last_object = model_object.objects.last()
        last_object.RPOSlug=slug
        last_object.employee.set(many_related_models)
        last_object.save()
    
    # many2many = []
    # for field_name , field_type in name_type_of_field.items():
    #     print(field_name, field_type)
    #     if isinstance(field_type , CharField ):
    #         print("hhh")
            # post_dict[field.name]=generate_char_field_data()
            # print(post_dict , "char")
    #     elif isinstance(field_type , IntegerField):
    #         post_dict[field.name]=genearte_integer_field()
    #     elif isinstance(field_type , DateField):
    #         post_dict[field.name]=generate_date_field_data()
    #     elif isinstance(field_type , SlugField):
    #         post_dict[field.name]=generate_char_field_data()
    #     for related in one_related_models:
    #         if isinstance(field_type , related):
    #             all_data_for_related_model = related.objects.all()
    #             all_data_for_related_model_length = len(all_data_for_related_model)
    #             one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length)]
    #             post_dict[field_name]=one_model_data
    #     for related in many_related_models:
    #         if isinstance(field_type , related):
    #             all_data_for_related_model = related.objects.all()
    #             all_data_for_related_model_length = len(all_data_for_related_model)
    #             one_model_data = all_data_for_related_model[random.randint(0,all_data_for_related_model_length)]
    #             many2many.append(one_model_data)
    # form = LeadForm(post_dict)
    # if form.is_valid():
    #     form.save()
    # last_object = model_object.objects.last()
    # last_object.employee.set( many2many )

    return HttpResponse("done")


def create_rows(model_object):
    post_dict = {}
    fields = model_object._meta.get_fields()

    class ModelForm(forms.ModelForm):
        class Meta:
            model = model_object
            fields = '__all__'

    for num in range(5):
        for field in fields:
            if isinstance(field , CharField):
                post_dict[field.name]=generate_char_field_data()
            elif isinstance(field , IntegerField):
                post_dict[field.name]=genearte_integer_field()            
            elif isinstance(field , SlugField):
                post_dict[field.name]=generate_char_field_data()            
            elif isinstance(field , DateField):
                post_dict[field.name]=generate_date_field_data()            
            elif isinstance(field , DateTimeField):
                post_dict[field.name]=generate_datetime_field_data()
    


        form = ModelForm(post_dict)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)














# to get all lower case chars
# string.ascii_lowercase
def generate_char_field_data():
    '''
    CharField generate data
    '''
    #char that will hold generated char 
    char_field = ''

    #loop to generate 6 char and save it in char_field
    for num in range(6):
        rand = int(random.randint(0,25))
        char = string.ascii_lowercase[rand]
        char_field += char
    
    #this  :(
    return char_field



# print( dir(datetime.datetime) )
def generate_date_field_data():
    '''
    DateField generate data
    '''
    date = datetime.datetime.now().date()
    year = random.randint(2017,2018)

    month = random.randint(1,12)
    day = random.randint(1,31)

    date = str(date).split("-")[0]
    return str(date)+"-"+str(month)+"-"+str(day) 

# print((datetime.datetime.now().time().hour))
# print(dir(datetime.datetime.now().time()))

# print(datetime.datetime.now())

def generate_datetime_field_data():
    '''
    DateTimeField generate data
    '''
    time = datetime.datetime.now().time()
    
    hour = random.randint(1,12)
    min = random.randint(1,60)
    sec = random.randint(1,60)
    
    date = datetime.datetime.now().date()
    
    # year = random.randint(2017,2018)

    month = random.randint(1,12)
    day = random.randint(1,31)

    date = str(date).split("-")[0]
    return str(date)+"-"+str(month)+"-"+str(day)+ " " + str(hour)+":"+str(min)+":"+str(sec)

def genearte_integer_field():
    '''
        IntegerField generate data
    '''
    return random.randint(0,100000)

