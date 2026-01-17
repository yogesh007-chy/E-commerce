from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from accounts.models import CustomUserModel

# Create your models here.
class Offerproduct(models.Model):
    title=models.CharField(max_length=200)
    desc=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to='offer_images')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Category(models.Model): #men,electronic
    title=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=200) #mobile
    category=models.ForeignKey(Category, on_delete=models.CASCADE) #electronic
    
    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    
    category=models.ForeignKey(Category, on_delete=models.CASCADE) 
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    desc=CKEditor5Field('Text', config_name='extends')
    image=models.ImageField(upload_to="images")
    mark_price=models.DecimalField(max_digits=8,decimal_places=2) #100
    discount_percent=models.DecimalField(max_digits=4,decimal_places=2) #10
    price=models.DecimalField(max_digits=8, decimal_places=2,editable=False) #90
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # price=100*(1-discount_percent/100) -->100*(1-10/100) -->100 * (1-0.1) -->100 *0.9 -->90
    
    
    def save(self,*args, **kwargs):
        self.name=self.name.capitalize()
        self.price =self.mark_price*(1-self.discount_percent/100)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    images=models.ImageField(upload_to='product_images')
    
    def __str__(self):
       return self.product.name
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField()
    feedback=models.CharField()
    created_date=models.DateTimeField(auto_now=True)

           
