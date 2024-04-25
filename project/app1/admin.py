from django.contrib import admin
from .models import Category,subcategory,Product,Section,Contact_us,Order,Brand
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import UserCreateForm
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class product_Admin(admin.ModelAdmin):
   list_display=('name','price','subcategory','section','discount')
   list_editable=('subcategory','section','discount')
# Register your models here.
admin.site.register(Category)
admin.site.register(subcategory)
admin.site.register(Product,product_Admin)
admin.site.register(Section)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)
# admin.site.register(Cart)



