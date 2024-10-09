from django.contrib import admin

from carts.models import Cart

# admin.site.register(Cart)


class CartTabularAdmin(admin.TabularInline):  # таблица которую добавили на страницу пользователей
    model = Cart
    fields = ["product", 'quantity', 'created_timestamp']
    readonly_fields = ['created_timestamp']
    extra = 1  # одно пустое поле внизу таблицы


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp']  # переопределили отображение в таблице в Корзинах
    list_filter = ['created_timestamp', 'user', 'product__name']

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return 'Анонимус'

    def product_display(self, obj):
        return obj.product.name
