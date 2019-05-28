from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from df_user import user_decorator
from df_goods.models import GoodsInfo
from .models import CartInfo
# Create your views here.


@user_decorator.login
def cart(request):
    uid = request.session.get('user_id')
    cart_list = CartInfo.objects.filter(user_id=int(uid))
    for g in cart_list:
        g.goods = GoodsInfo.objects.get(pk=g.good_id)

    return render(request, 'df_cart/cart.html', {'page_name': 1, 'title': "购物车", 'cart_list': cart_list})


@user_decorator.login
def add(request, gid, amount):
    gid = int(gid)
    amount = int(amount)
    uid = request.session.get('user_id')
    cart1 = CartInfo()
    carts = CartInfo.objects.filter(user_id=uid, good_id=gid)
    if len(carts) > 0:
        cart1 = carts[0]
        cart1.count += amount
    else:
        cart1.user_id = uid
        cart1.good_id = gid
        cart1.count = amount
    cart1.save()
    count = CartInfo.objects.filter(user_id=uid).count()
    if request.is_ajax():
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def del_cart(request, cart_id):
    try:
        cart1 = CartInfo.objects.get(pk=int(cart_id))
        cart1.delete()
        data = {'ok': cart_id}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)


@user_decorator.login
def edit(request):
    cart_id = request.GET.get('cart_id')
    count = int(request.GET.get('amount'))
    try:
        cart1 = CartInfo.objects.get(pk=int(cart_id))
        cart1.count = count
        cart1.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count}
    return JsonResponse(data)
