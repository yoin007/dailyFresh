from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from df_cart.models import CartInfo

# Create your views here.


def index(request):
    uid = request.session.get('user_id')
    if uid:
        cart_amount = CartInfo.objects.filter(user_id=int(uid)).count()
    else:
        cart_amount = 0
    type_list = TypeInfo.objects.all()
    type0 = type_list[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = type_list[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = type_list[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = type_list[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = type_list[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = type_list[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = type_list[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = type_list[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = type_list[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = type_list[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = type_list[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = type_list[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'guest_cart': 1, 'title': "首页",
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               'cart_amount': cart_amount
               }
    return render(request, 'df_goods/index.html', context)


def goods_list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=tid)
    new = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':  # 默认，最新
        goods = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-id')
    elif sort == '2':   # 价格
        goods = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-gprice')
    elif sort == '3':   # 点击量
        goods = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-gclick')

    paginator = Paginator(goods, 10)
    page = paginator.page(int(pindex))
    cart_count1 = cart_count(request)
    context = {
        'title': typeinfo.ttitle, 'guest_cart': 1,
        'page': page, 'paginator': paginator,
        'typeinfo': typeinfo, 'sort': sort,
        'new': new, 'cart_amount': cart_count1,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    uid = request.session.get('user_id')
    if uid:
        cart_amount = CartInfo.objects.filter(user_id=int(uid)).count()
    else:
        cart_amount = 0
    gid = int(gid)
    goods = GoodsInfo.objects.get(pk=gid)
    goods.gclick += 1
    goods.save()
    new = GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]
    # news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    # print(news)
    # print(new)
    response = render(request, 'df_goods/detail.html',
                      {'g': goods, 'title': goods.gtype.ttitle,
                       'guest_cart': 1, 'id': gid, 'new': new, 'cart_amount': cart_amount})

    goods_ids = request.COOKIES.get('goods_ids', '')
    gid = str(gid)
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if gid in goods_ids1:
            goods_ids1.remove(gid)
        goods_ids1.insert(0, gid)
        if len(goods_ids1) >= 6:
            goods_ids1.pop()
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = gid

    response.set_cookie('goods_ids', goods_ids)

    return response


def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=int(request.session.get('user_id'))).count()
    else:
        return 0


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        context['cart_amount'] = cart_count(self.request)
        return context
