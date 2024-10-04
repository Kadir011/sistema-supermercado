from django.urls import path 
from Super.views import ux, cliente, vendedor, producto, user


app_name = 'Super'
urlpatterns = []

#urls de ux
urlpatterns += [
    path('sign_up/', ux.RegisterView.as_view(), name='register'),
    path('sign_in/', ux.LoginView.as_view(), name='login')
]

#urls de cliente
urlpatterns += [
    path('clientes/', cliente.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/create', cliente.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/update/<int:pk>', cliente.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/delete/<int:pk>', cliente.ClienteDeleteView.as_view(),  name='cliente_delete')
] 

#urls de vendedor
urlpatterns += [
    path('vendedores/', vendedor.VendedorListView.as_view(), name='vendedor_list'),
    path('vendedores/create', vendedor.VendedorCreateView.as_view(), name='vendedor_create'),
    path('vendedores/update/<int:pk>', vendedor.VendedorUpdateView.as_view(), name='vendedor_update'),
    path('vendedores/delete/<int:pk>', vendedor.VendedorDeleteView.as_view(), name='vendedor_delete') 
] 

#urls de producto
urlpatterns += [
    path('productos/', producto.ProductoListView.as_view(), name='producto_list'),
    path('productos/create', producto.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/update/<int:pk>', producto.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/delete/<int:pk>', producto.ProductoDeleteView.as_view(), name='producto_delete'),
    path('producto/<int:pk>/estado', producto.ProductoEstadoDetailView.as_view(), name='producto_estado'),
    path('productos/<int:pk>', producto.ProductoDetailView.as_view(), name='producto_detail')
] 

#urls de usuario
urlpatterns += [
    path('users/', user.UserListView.as_view(), name='user_list'),
    path('users/create', user.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>', user.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>', user.UserDeleteView.as_view(), name='user_delete') 
]



