from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Super.form.cliente import ClienteForm
from Super.models import Cliente 
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    paginate_by = 2

    def get_queryset(self):
        q = self.request.GET.get('q') 
        if q:
            return Cliente.objects.filter(
                Q(user=self.request.user) & (Q(codigo__icontains=q)|
                                             Q(nombre__icontains=q)|
                                             Q(apellido__icontains=q)|
                                             Q(cedula__icontains=q)|
                                             Q(telefono__icontains=q)|
                                             Q(fecha_nacimiento__icontains=q)|
                                             Q(genero__icontains=q)) 
            ) 
        return Cliente.objects.filter(user=self.request.user).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Clientes'
        context['create_url'] = reverse_lazy('Super:cliente_create')
        return context 

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente 
    template_name = 'clientes/form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('Super:cliente_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Registro de Clientes'
        context['grabar'] = 'Registrar Cliente'
        context['back_url'] = self.success_url
        return context 

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'clientes/form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('Super:cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(user=self.request.user) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de Cliente'
        context['grabar'] = 'Editar Cliente'
        context['back_url'] = self.success_url 
        return context 

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente 
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('Super:cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(user=self.request.user) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Eliminación de Cliente'
        context['grabar'] = 'Eliminar Cliente'
        context['description'] = f'¿Desea eliminar al cliente N°{self.object.id}: {self.object.codigo} - {self.object.get_full_name()}?' 
        context['back_url'] = self.success_url
        return context 

