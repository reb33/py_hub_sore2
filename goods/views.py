from django.shortcuts import render

from goods.models import Products


# Create your views here.


def catalog(request):
    goods = Products.objects.all()
    context = {
        "title": "Home - Каталог",
        "goods": goods
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_id):
    _product = Products.objects.get(id=product_id)
    context = {
        "product": _product
    }
    return render(request, 'goods/product.html', context)
