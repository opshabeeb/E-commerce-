from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class subcategory(models.Model):
    name=models.CharField(max_length=150)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Section(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    product_details=RichTextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=False)
    subcategory=models.ForeignKey(subcategory,on_delete=models.CASCADE,null=False)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    available_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products', blank=True, null=True)
    section=models.ForeignKey(Section,on_delete=models.DO_NOTHING,blank=True, null=True)
    slug=models.SlugField(default='',max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})
    class Meta:
        db_table="app1_product_detail"
    
def create_slug(instance,new_slug=None):
    slug=slugify(instance.name)
    if new_slug is not None:
        slug=new_slug
    qs=Product.objects.filter(slug=slug).order_by('-id')
    exists=qs.exists()
    if exists:
        new_slug="%s-%s" % (slug, qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)
    
pre_save.connect(pre_save_post_receiver,Product)


    
class UserCreateForm(UserCreationForm):
    # Define additional fields with customization
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This email already exists'})
    first_name = forms.CharField(max_length=30, required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone = forms.CharField(max_length=15, required=False, label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    address = forms.CharField(max_length=50, required=False, label='Address', widget=forms.Textarea(attrs={'placeholder': 'Address'}))

    # Meta class provides metadata about the form
    class Meta:
        model = User  # Specifies the User model
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address')  # Specifies the fields to include in the form
        
    # def __init__(self,*args,**kwargs):

    # Override the save method to customize user creation
    def save(self, commit=True):
        # Call the save method of the parent class with commit=False to get an unsaved user instance
        user = super(UserCreateForm, self).save(commit=False)
        # Set the additional attributes of the user instance to the cleaned data from the form
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']

        # If commit is True, save the user to the database
        if commit:
            user.save()
            
        return user
    

    # Define a custom validation method for the email field
    def clean_email(self):
        # Get the cleaned email data from the form
        email = self.cleaned_data.get('email')

        # Check if a user with the entered email already exists in the database
        if User.objects.filter(email=email).exists():
            # If the email exists, raise a validation error with a custom error message
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])

        # If the email is unique, return the cleaned email
        return email
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    
# class Cart(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

#     def _str_(self):
#         return str(self.user)

class Contact_us(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    
    def __str__(self):
        return self.subject
    
class Order(models.Model):
    image=models.ImageField(upload_to='order/image')
    product=models.CharField(max_length=1000,default='')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total=models.CharField(max_length=1000,default='')
    lastprice=models.CharField(max_length=1000,default='')
    discounted_price=models.CharField(max_length=1000,default='')
    quantity=models.CharField(max_length=5)
    address=models.TextField()
    phone=models.CharField(max_length=10)
    pincode=models.CharField(max_length=10)
    payment_id=models.CharField(max_length=500,null=True,blank=True)
    paid=models.BooleanField(default=False,null=True)
    date=models.DateField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.product
# class Cart(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

#     def _str_(self):
#         return str(self.user)