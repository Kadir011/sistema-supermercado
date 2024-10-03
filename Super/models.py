from datetime import datetime
from decimal import Decimal
from django.db import models
from django.forms import model_to_dict
from SisSuper import utils
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    iduser = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código')
    dni = models.CharField(verbose_name='Cédula o RUC', max_length=13, blank=True, null=True)
    image = models.ImageField(
        verbose_name='Archive image',
        upload_to='users',
        max_length=1024,
        blank=True,
        null=True
    )
    email = models.EmailField('Email', unique=True)
    direction = models.CharField('Dirección', max_length=200, blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=50, blank=True, null=True)

    # Sobrescribimos groups y user_permissions con None para eliminarlos
    groups = None
    user_permissions = None

    USERNAME_FIELD = "email"  # cambiar el login al email
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['iduser']

    def __str__(self):
        return '{}'.format(self.username)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def get_image_url(self):
        return utils.get_image(self.image)


class Marca(models.Model):
    idmarca = models.AutoField(primary_key=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, 
                              blank=True, 
                              unique=True, 
                              verbose_name='Marca')
    
    estado = models.BooleanField(blank=True, null=True, default=True, verbose_name='Estado')

    @property
    def id(self):
        return self.idmarca

    def __str__(self):
        return f'Marca N°{self.id}: {self.nombre}'
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['idmarca']


class Categoria(models.Model):
    idcategoria = models.AutoField(primary_key=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, 
                              blank=True, 
                              unique=True, 
                              verbose_name='Categoría')
    
    estado = models.BooleanField(blank=True, null=True, default=True, verbose_name='Estado')

    @property
    def id(self):
        return self.idcategoria

    def __str__(self):
        return f'Categoría N°{self.id}: {self.nombre}'
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['idcategoria']


class Cliente(models.Model):
    class ClienteGenero(models.TextChoices):
        HOMBRE = '1', 'Hombre'
        MUJER = '2', 'Mujer'

    idcliente = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código')
    codigo = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Código Cliente')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, blank=False, null=False, verbose_name='Apellido')
    cedula = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Cédula')
    telefono = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    genero = models.CharField(max_length=1, 
                              choices=ClienteGenero.choices, 
                              default=ClienteGenero.HOMBRE, 
                              blank=True, 
                              null=False,  # Mejor manejarlo como cadena vacía en lugar de NULL
                              verbose_name='Género')
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Usuario') 

    @property
    def id(self):
        return self.idcliente

    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'

    def __str__(self):
        return f'Cliente N°{self.id}: {self.codigo} - {self.get_full_name()}'
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['codigo', 'nombre', 'apellido']


class Vendedor(models.Model):
    class VendedorGenero(models.TextChoices):
        HOMBRE = '1', 'Hombre'
        MUJER = '2', 'Mujer'

    idvendedor = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código')
    codigo = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Código Vendedor') 
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, blank=False, null=False, verbose_name='Apellido')
    cedula = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Cédula')
    telefono = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    genero = models.CharField(max_length=1, 
                              choices=VendedorGenero.choices, 
                              default=VendedorGenero.HOMBRE, 
                              blank=True, 
                              null=False,  # Igual que en Cliente
                              verbose_name='Género') 
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Usuario')

    @property
    def id(self):
        return self.idvendedor

    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'
    
    def __str__(self):
        return f'Vendedor N°{self.id}: {self.codigo} - {self.get_full_name()}' 
    
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['codigo', 'nombre', 'apellido']


class Producto(models.Model):
    idproducto = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código')
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT, blank=True, null=True, related_name='productos')
    categoria = models.ForeignKey(Categoria, verbose_name='Categoría', on_delete=models.PROTECT, blank=True, null=True, related_name='productos')
    imagen = models.ImageField(upload_to='producto', max_length=500, blank=True, null=True, verbose_name='Imagen')
    codigo = models.CharField(max_length=20, unique=True, blank=False, null=False, verbose_name='Código Producto') 
    nombre = models.CharField(max_length=100, blank=True, null=False, verbose_name='Producto')  # Solo se permite vacío, no NULL
    descripcion = models.TextField(max_length=200, blank=True, null=False, verbose_name='Descripción') 
    precio = models.DecimalField(max_digits=10, 
                                 decimal_places=2, 
                                 blank=False,
                                 null=False, 
                                 verbose_name='Precio', 
                                 default=Decimal('0.00'))
    fecha_elaboracion = models.DateField(default=datetime.today, blank=True, null=True, verbose_name='Fecha Elaboración')
    fecha_expiracion = models.DateField(blank=True, null=True, verbose_name='Fecha Expiración')
    estado = models.BooleanField(blank=True, null=True, default=True, verbose_name='Estado') 

    @property
    def id(self):
        return self.idproducto
    
    def get_image_url(self):
        return utils.get_image(self.imagen)
    
    def get_model_dict(self):
        item = model_to_dict(self)
        item['imagen_url'] = self.get_image_url()
        return item

    def __str__(self):
        return f'Producto N°{self.id}: {self.codigo} - {self.nombre}' 
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        constraints = [models.CheckConstraint(check=models.Q(precio__gte=0), name='ck_precio_positivo')]
        ordering = ['codigo', 'nombre', 'descripcion']


class Venta(models.Model):
    idventa = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código')
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', on_delete=models.PROTECT, blank=True, null=True, related_name='ventas') 
    vendedor = models.ForeignKey(Vendedor, verbose_name='Vendedor', on_delete=models.PROTECT, blank=True, null=True, related_name='ventas')
    fecha = models.DateField(default=datetime.today, blank=True, null=False, verbose_name='Fecha de Venta')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False, default=Decimal('0.00'), verbose_name='Subtotal')
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False, default=0.15, verbose_name='Iva')
    dscto = models.FloatField(blank=True, null=False, default=0.00, verbose_name='Descuento') 
    total = models.DecimalField(max_digits=10, 
                                decimal_places=2, 
                                blank=True, 
                                null=False, 
                                default=Decimal('0.00'), 
                                verbose_name='Total') 
    
    @property
    def id(self):
        return self.idventa 
    
    def __str__(self):
        return f'Venta N°{self.id} - {self.fecha}' 
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        constraints = [models.CheckConstraint(check=models.Q(subtotal__gte=0), name='check_subtotal_positivo'),
                       models.CheckConstraint(check=models.Q(iva__gte=0), name='check_iva_positivo'),
                       models.CheckConstraint(check=models.Q(dscto__gte=0), name='check_dscto_positivo'),
                       models.CheckConstraint(check=models.Q(total__gte=0), name='check_total_positivo')]
        
        ordering = ['idventa', 'cliente', 'vendedor', 'fecha'] 


class VentaDetalle(models.Model):
    iddetalle = models.AutoField(primary_key=True, blank=False, null=False, verbose_name='Código') 
    venta = models.ForeignKey(Venta, verbose_name='Venta', on_delete=models.PROTECT, blank=True, null=True, related_name='detalles') 
    producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.PROTECT, blank=True, null=True, related_name='detalles') 
    cantidad = models.IntegerField(blank=False, null=False, default=0, verbose_name='Cantidad') 
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=False, null=False, verbose_name='Precio') 
    subtotal = models.DecimalField(max_digits=10, 
                                   decimal_places=2, 
                                   default=Decimal('0.00'), 
                                   blank=False, 
                                   null=False, 
                                   verbose_name='Subtotal')

    @property
    def id(self):
        return self.iddetalle
    
    def __str__(self):
        return f'Venta Detalle N°{self.id}: Venta N°{self.venta.id} - {self.venta.fecha} - {self.producto.nombre}'
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
        constraints = [models.CheckConstraint(check=models.Q(cantidad__gte=0), name='check_cantidad_positivo'),
                       models.CheckConstraint(check=models.Q(precio__gte=0), name='check_precio_positivo'),
                       models.CheckConstraint(check=models.Q(subtotal__gte=0), name='check_subtotal_detalle_positivo')]
        
        ordering = ['iddetalle', 'venta', 'producto']



