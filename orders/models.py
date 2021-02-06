import math

from django.db import models
from django.db.models.signals import pre_save, post_save

from KAproject.utils import unique_order_id_generator
from billing.models import BillingProfile
from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Создан'),  # Created
    ('paid', 'Оплачен'),  # Paid
    ('shipped', 'Отправлен'),  # Shipped
    ('refunded', 'Возвращен'),  # Refunded
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created
        #old code, but its working
        #qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        #if qs.count() == 1:
        #    obj = qs.first()
        #else:
        #    obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
        #return obj


# Random, Unique
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    # pk / id
    order_id = models.CharField(max_length=120, blank=True, verbose_name='Номер заказа')   # AB31DE3
    # Billing Profile
    # shipping address
    # billing address
    cart = models.ForeignKey(Cart, verbose_name='Корзина')
    status = models.CharField(max_length=120, default='created', verbose_name='Статус', choices=ORDER_STATUS_CHOICES)  # создан
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    order_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        print(cart_total)
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        print(new_total)
        formatted_total = format(new_total, '.2f')
        self.order_total = formatted_total
        print(self.order_total)
        self.save()
        return new_total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if(qs.exists() and qs.count() == 1):   #can remove qs.exists()
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("Updating ... first")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)

#generate the order_id
#generate the order total
