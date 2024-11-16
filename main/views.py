from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories

class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Home - Главная",
            "content": "Магазин мебели HOME",
        })
        return context


# def index(request):
#     categories = Categories.objects.all()
#     context = {
#         "title": "Home - Главная",
#         "content": "Магазин мебели HOME",
#         "categories": categories,
#     }
#     return render(request, "main/index.html", context)


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Home - О нас",
            "content": "О нас",
            "text_on_page": "длинный текст о магазине",
        })
        return context

# def about(request):
#     context = {
#         "title": "Home - О нас",
#         "content": "О нас",
#         "text_on_page": "длинный текст о магазине",
#     }
#     return render(request, "main/about.html", context)
