from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from Super.form.vendedor import VendedorForm 
from Super.models import Vendedor
from django.urls import reverse_lazy
from django.db.models import Q

class VendedorListView(LoginRequiredMixin, ListView):
    model = Vendedor
    template_name = 'vendedores/list.html'
    context_object_name = 'vendedores'
    paginate_by = 2 

    def get_queryset(self):
        q = self.request.GET.get('q') 
        if q:
            return Vendedor.objects.filter(
                Q(user=self.request.user) & (Q(codigo__icontains=q)|
                                             Q(nombre__icontains=q)|
                                             Q(apellido__icontains=q)|
                                             Q(cedula__icontains=q)|
                                             Q(telefono__icontains=q)|
                                             Q(fecha_nacimiento__icontains=q)|
                                             Q(genero__icontains=q)) 
            ) 
        return Vendedor.objects.filter(user=self.request.user).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Lista de Vendedores'
        context['create_url'] = reverse_lazy('Super:vendedor_create')
        return context 

class VendedorCreateView(LoginRequiredMixin, CreateView):
    model = Vendedor
    template_name = 'vendedores/form.html' 
    form_class = VendedorForm
    success_url = reverse_lazy('Super:vendedor_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Registro de Vendedores'
        context['grabar'] = 'Registrar Vendedor'
        context['back_url'] = self.success_url
        return context 

class VendedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendedor 
    template_name = 'vendedores/form.html' 
    form_class = VendedorForm 
    success_url = reverse_lazy('Super:vendedor_list') 

    def get_queryset(self):
        return Vendedor.objects.filter(user=self.request.user) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de Vendedor'
        context['grabar'] = 'Editar Vendedor'
        context['back_url'] = self.success_url 
        return context 

class VendedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendedor
    template_name = 'vendedores/delete.html'
    success_url = reverse_lazy('Super:vendedor_list') 

    def get_queryset(self):
        return Vendedor.objects.filter(user=self.request.user)  
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data() 
        context['title'] = 'Eliminación de Vendedor' 
        context['grabar'] = 'Eliminar Vendedor'
        context['description'] = f'¿Desea eliminar al Vendedor N°{self.object.id}: {self.object.codigo} - {self.object.get_full_name()}?' 
        context['back_url'] = self.success_url 
        return context 

