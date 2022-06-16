from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.http import JsonResponse

from products.models import Product, ProductSize
from .models import Order, OrderItem
from .models import RefundForm


class RefundView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'carts/refund.html'
    form_class = RefundForm
    success_url = reverse_lazy('refund')
    success_message = "Su consulta fue enviada correctamente"

    def form_valid(self, form):
        try:
            order = Order.objects.get(order_id=form.cleaned_data['order_id'])
        except Order.DoesNotExist:
            messages.warning(self.request, "El ID de Orden ingresado no existe")
            return redirect('refund')
        order.refund_requested = True
        order.save()
        form.instance.user = self.request.user
        form.instance.order = order
        form.save()
        return super().form_valid(form)


class OrdersListView(LoginRequiredMixin, ListView):
    context_object_name = 'orders'
    paginate_by = 3

    def get_queryset(self):
        return self.request.user.order_set.filter(ordered=True)


class CartDetailView(DetailView):
    context_object_name = 'order'
    template_name = 'carts/cart.html'

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            return Order.objects.filter(device=self.request.COOKIES['device'], ordered=False).last()
        return self.request.user.order_set.filter(ordered=False).last()


class AddToCartAjax(View):
    def post(self, request, buy_now, *args, **kwargs):
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')
        if not size:
            messages.error(request, 'Debe seleccionar el talle.')
            return redirect(request.META['HTTP_REFERER'])
        product_size = get_object_or_404(ProductSize, pk=size)

        if not self.request.user.is_authenticated:
            order, _ = Order.objects.get_or_create(device=request.COOKIES['device'], ordered=False)
        else:
            order = Order.objects.filter(user=request.user, ordered=False).last()
            if not order:
                order = Order.objects.create(user=request.user, ordered=False)
                order.save()
        if order.items.filter(item__pk=product_size.id).exists():
            order_item = order.items.get(item__pk=product_size.id)
            order_item.quantity += 1
            order_item.save()
        else:
            if not self.request.user.is_authenticated:
                order_item = OrderItem.objects.create(device=request.COOKIES['device'], item=product_size)
            else:
                order_item = OrderItem.objects.create(user=self.request.user, item=product_size)
            order.items.add(order_item)
        messages.error(request, 'Producto agregado al carrito correctamente')
        if buy_now:
            return redirect('carts:show-cart')
        return redirect(request.META['HTTP_REFERER'])


@login_required
def increase_product_in_cart(request, product_size_id):
    product_size = get_object_or_404(ProductSize, pk=product_size_id)
    if not request.user.is_authenticated:
        order, _ = Order.objects.get_or_create(device=request.COOKIES['device'], ordered=False)
    else:
        order = Order.objects.filter(user=request.user, ordered=False).last()
        if not order:
            order = Order.objects.create(user=request.user, ordered=False)
            order.save()
    if order.items.filter(item__pk=product_size_id).exists():
        order_item = order.items.get(item__pk=product_size_id)
        order_item.quantity += 1
        order_item.save()
    else:
        order.items.create(user=request.user, item=product_size)
    messages.success(request, 'Producto agregado al carrito correctamente')
    return redirect('carts:show-cart')


@login_required
def decrease_product_in_cart(request, product_size_id):
    product_size = get_object_or_404(ProductSize, pk=product_size_id)
    if not request.user.is_authenticated:
        order, _ = Order.objects.get_or_create(device=request.COOKIES['device'], ordered=False)
    else:
        order = Order.objects.filter(user=request.user, ordered=False).last()
        if not order:
            order = Order.objects.create(user=request.user, ordered=False)
            order.save()
    if order:
        order_item = order.items.filter(user=request.user, item=product_size_id).last()
        if order_item:
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity <= 0:
                order.items.remove(order_item)
            messages.success(request, 'Producto eliminado del carrito correctamente')
        else:
            messages.warning(request, 'Este producto no se encuentra en el carrito')
    else:
        messages.warning(request, 'Este carrito no existe. Ha ocurrido un error')
        return redirect('products:home-page')
    return redirect('carts:show-cart')


@login_required
def remove_from_cart(request, product_size_id):
    product_size = get_object_or_404(ProductSize, pk=product_size_id)
    if not request.user.is_authenticated:
        order, _ = Order.objects.get_or_create(device=request.COOKIES['device'], ordered=False)
    else:
        order = Order.objects.filter(user=request.user, ordered=False).last()
        if not order:
            order = Order.objects.create(user=request.user, ordered=False)
            order.save()
    if order:
        order_item = order.items.filter(user=request.user, item=product_size).last()
        if order_item:
            order.items.remove(order_item)
            messages.success(request, 'Producto eliminado correctamente del carrito')
        else:
            messages.warning(request, 'Este producto no se encuentra en el carrito')
    else:
        messages.warning(request, 'Este carrito no existe. Ha ocurrido un error')
        return redirect('products:home-page')
    return redirect('carts:show-cart')
