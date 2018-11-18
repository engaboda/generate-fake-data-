from django.contrib import admin
from .models import Lead , UserModel  , Employee

# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id' , 'username')

class EmployeelAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name')


class LeadAdmin(admin.ModelAdmin):
    filter_horizontal=['employee']
    list_display = ('id', 'user_name'  , 'RPODateAdded')
    # list_filter = ('LEADFirstName','LEADSecondName','LEADLastName')
    # ordering = ('LEADFirstName', 'LEADSecondName')
    change_form_template = 'admin/duplicate/Lead/change_form.html'
    change_list_template = 'admin/duplicate/Lead/change_list.html'
    prepopulated_fields = {"RPOSlug": ("user_name",)}
    # class Media:
    #     js = ('duplicate/js/change_form.js',)
    

admin.site.register(Employee , EmployeelAdmin)
admin.site.register(Lead , LeadAdmin)
admin.site.register( UserModel , UserModelAdmin)