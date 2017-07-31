from django.contrib import admin
from app import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','qq','source','consultant','status')
    list_filter = ('source','status','consultant')
    search_fields = ['qq','source__name']
    list_per_page = 2
    filter_horizontal = ['tags', 'consult_courses']

admin.site.register(models.Source)
admin.site.register(models.Branch)
admin.site.register(models.Course)
admin.site.register(models.Contract)
admin.site.register(models.Account)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.ClassList)
admin.site.register(models.Account1)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.SubMenu)
admin.site.register(models.Tag)




