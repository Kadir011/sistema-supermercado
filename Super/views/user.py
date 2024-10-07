from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from Super.form.user import UserForm
from Super.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 2

    def get_queryset(self):
        q1 = self.request.GET.get('q1')  # DNI
        q2 = self.request.GET.get('q2')  # Apellido
        q3 = self.request.GET.get('q3')  # Email
        self.query = Q()  # Inicializar la consulta
        if q1 is not None:
            self.query.add(Q(dni__icontains=q1), Q.AND)
        if q2 is not None:
            self.query.add(Q(last_name__icontains=q2), Q.AND)
        if q3 is not None:
            self.query.add(Q(email__icontains=q3), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios'
        context['create_url'] = reverse_lazy('Super:user_create')
        return context

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('Super:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Registro de Usuarios'
        context['grabar'] = 'Registrar Usuario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        self.object = form.save()
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('Super:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de Usuario'
        context['grabar'] = 'Editar Usuario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        password_anterior = form.fields['password'].initial
        self.object = form.save()
        if form.cleaned_data['password'] != password_anterior:
            form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('Super:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Eliminación de Usuario'
        context['grabar'] = 'Eliminar Usuario'
        context['description'] = f'¿Desea Eliminar El Usuario: {self.object.get_full_name}?'
        context['back_url'] = self.success_url
        return context




