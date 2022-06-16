from django.views.generic import ListView, DetailView
from .models import Product
from .models import Category


class HomePage(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.filter(important=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        categories = Category.objects.all()[:4]
        context['categories'] = categories

        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'

class CategoryProductDetailView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category_product_detail.html'
    paginate_by = 9
    ordering = '-id'
    
    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = None
            pk = self.kwargs.get('pk')
            self.ordering = self.kwargs.get('ordering')
            if pk is not None:
                if self.ordering not in ['-id', 'id', 'price', '-price']:
                    self.ordering = '-id'
                queryset = Product.objects.filter(category=pk).order_by(self.ordering)
            return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryProductDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['category'] = Category.objects.get(id=pk)
        context['ordering'] = self.ordering

        return context