from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from Super.form.producto import ProductoForm 
from Super.models import Producto
from django.urls import reverse_lazy
from django.db.models import Q 

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto 
    template_name = 'productos/list.html'
    context_object_name = 'productos' 
    paginate_by = 2

    def get_queryset(self):
        q = self.request.GET.get('q') 
        query = Q()

        if q:
            query &= (Q(codigo__icontains=q) |
                      Q(marca__nombre__icontains=q) |
                      Q(categoria__nombre__icontains=q) |
                      Q(nombre__icontains=q) |
                      Q(descripcion__icontains=q) |
                      Q(precio__icontains=q) |
                      Q(fecha_elaboracion__icontains=q) |
                      Q(fecha_expiracion__icontains=q) |
                      Q(estado__icontains=q))

        return self.model.objects.filter(query).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Productos'
        context['create_url'] = reverse_lazy('Super:producto_create')
        return context
    

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto 
    template_name = 'productos/form.html' 
    form_class = ProductoForm 
    success_url = reverse_lazy('Super:producto_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Registro de Productos' 
        context['grabar'] = 'Registrar Producto' 
        context['back_url'] = self.success_url
        return context 
    

class ProductoEstadoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'productos/detail.html'
    context_object_name = 'producto'
    
    def post(self, request, *args, **kwargs):
        try:
            producto = self.get_object()
            producto.estado = False
            producto.save()
            return redirect('Super:producto_list')
        except Exception as e:
            context = self.get_context_data()
            context['error'] = str(e)
            return self.render_to_response(context)
    

class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'productos/detail_popup.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del Producto'
        context['back_url'] = reverse_lazy('Super:producto_list')
        return context


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto 
    template_name = 'productos/form.html'
    form_class = ProductoForm 
    success_url = reverse_lazy('Super:producto_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Edición de Producto' 
        context['grabar'] = 'Editar Producto' 
        context['back_url'] = self.success_url
        return context 
    

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/delete.html' 
    success_url = reverse_lazy('Super:producto_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Eliminación de Producto' 
        context['grabar'] = 'Eliminar Producto' 
        context['description'] = f'¿Desea eliminar el producto N°{self.object.id}: {self.object.codigo} - {self.object.nombre}?' 
        context['back_url'] = self.success_url 
        return context 





