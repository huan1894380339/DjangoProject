from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from app.models import Membership, Order


@receiver(post_save, sender=Order, dispatch_uid='update_voucher')
def update_voucher(sender, instance, **kwargs):
    membership = Membership.objects.get(user=instance.user.id)
    if membership.voucher != 0.25:
        all_order = Order.objects.filter(user=instance.user, status='SU')
        voucher = (sum(order.cart_total for order in all_order) * 0.01) / 100
        membership.voucher = voucher
        membership.save()


# @receiver(m2m_changed, sender=Order.cart_item.through)
# def update_status_cartitem(sender, instance, **kwargs):
#     cart_item = instance.cart_item.all()
#     for cart in cart_item:
#         cart.status = 'C'
#         cart.save()

# handle cartitem
@receiver(m2m_changed, sender=Order.cart_item.through)
def update_status_cartitem(sender, instance, action, **kwargs):
    if action == 'post_add':
        if instance.user in [x.user for x in instance.cart_item.all()]:
            instance.save()
            cart_item = instance.cart_item.all()
            for cart in cart_item:
                cart.status = 'C'
                cart.save()
        else:
            raise Exception('Something error with user value')


# @receiver(m2m_changed, sender=Order.cart_item.through)
# def validate_cart_item(sender, instance, **kwargs):
#     import ipdb;ipdb.set_trace()
#     if instance.user not in [x.user for x in instance.cart_item.all()]:
#         raise Exception('Something error with user value')
#     else:
#         instance.save()

#  check user in cart item and order


# def validate_cart_item(sender, instance, **kwargs):
#     import ipdb;ipdb.set_trace()
#     if instance.user not in [x.user for x in instance.cart_item.all()]:
#         raise Exception('Something error with user value')
#     else:
#         instance.save()

# m2m_changed.connect(validate_cart_item, sender=Order.cart_item.through)
