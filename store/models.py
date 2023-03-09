from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        customer_name = self.customer
        if customer_name == None:
            return 'Deleted Customer'
        else:
            return f"{self.customer} Order. "
    
    @property
    def item_count(self):
        count = 0
        for item in self.orderitems_set.all():
            count += item.quantity
        return count
    
    @property
    def cost_total(self):
        total = 0
        for item in self.orderitems_set.all():
            total += item.individual_item_total
        return total

    @property
    def shipping(self):
        shipping = False
        for item in self.orderitems_set.all():
            if item.product.is_digital == False:
                shipping = True
        return shipping

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{ self.order.customer.user } Items. {self.product.name}"

    @property
    def individual_item_total(self):
        cost = self.quantity * self.product.price
        return cost

    class Meta:
        verbose_name_plural = 'Order Items'

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.customer.name} address."
    
    class Meta:
        verbose_name_plural = 'Shipping Address'