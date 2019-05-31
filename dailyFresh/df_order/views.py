from django.shortcuts import render, redirect
from df_user import user_decorator
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from .models import OrderInfo, OrderDetailInfo
from django.db import transaction
from datetime import datetime
from decimal import Decimal

# Create your views here.


@user_decorator.login
def order(request):
    uid = request.session.get('user_id')
    cart_list = request.GET.getlist('cart_id')
    goods_list = CartInfo.objects.filter(user_id=uid).filter(pk__in=cart_list)
    total = 0.00
    for g in goods_list:
        g.good = GoodsInfo.objects.get(pk=g.good_id)
        gprice = g.good.gprice
        total = total + g.count * float(gprice)
    context = {'page_name': 1, 'title': '提交订单', 'good_list': goods_list, 'total': total}
    return render(request, 'df_order/order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()

    cart_ids = request.POST.get('good_list')
    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('user_id')
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.save()

        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            cart = CartInfo.objects.get(id=id1)

            goods = cart.goods

            if goods.gkucun >= cart.count:
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '======================%s'%e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')