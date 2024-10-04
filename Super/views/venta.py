import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View 
from Super.form.venta import VentaForm 
from Super.models import Venta, VentaDetalle, Producto 
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta 
    template_name = 'ventas/list.html' 
    context_object_name = 'ventas'
    paginate_by = 2 

    def get_queryset(self):
        q = self.request.GET.get('q') 
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(Q(cliente__nombre__icontains=q)|
                                       Q(cliente__apellido__icontains=q)|
                                       Q(vendedor__nombre__icontains=q)|
                                       Q(vendedor__apellido__icontains=q)|
                                       Q(fecha__icontains=q))  
        return queryset.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Lista de Ventas'
        context['create_url'] = reverse_lazy('Super:venta_create')
        return context 
    

class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta 
    template_name = 'ventas/form.html'
    form_class = VentaForm
    success_url = reverse_lazy('Super:venta_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Registro de Ventas'
        context['grabar'] = 'Registrar Venta'
        context['back_url'] = self.success_url 
        context['productos'] = Producto.objects.all().order_by('id')
        return context 
    
    def post(self, request, *args, **kwargs): 
        form = self.get_form() 

        if not form.is_valid():
            return JsonResponse({'errors': form.errors, 'form_data': request.POST}, status=400) 
        
        data = request.POST 
        venta = form.save() 
        detalles = json.loads(data['detalles'])

        for detalle in detalles:
            VentaDetalle.objects.create(
                venta=venta,
                idproducto=detalle['idproducto'],
                cantidad=detalle['cantidad'],
                precio=detalle['precio'],
                subtotal=detalle['subtotal']
            ) 
        return JsonResponse({}, status=200)


class VentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Venta 
    template_name = 'ventas/form.html'
    form_class = VentaForm 
    success_url = reverse_lazy('Super:venta_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data() 
        context['title'] = 'Edición de Venta'
        context['grabar'] = 'Editar Venta' 
        context['back_url'] = self.success_url 
        context['productos'] = Producto.objects.all() 
        detalles = list(VentaDetalle.objects.filter(venta=self.object).values()) 
        context['detalles'] = json.dumps(detalles)
        return context 
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return JsonResponse({'errors': form.errors, 'form_data': request.POST}, status=400) 
        
        data = request.POST
        venta = form.save()
        VentaDetalle.objects.filter(venta=venta).delete()
        detalles = json.loads(data['detalles'])

        for detalle in detalles:
            VentaDetalle.objects.create(
                venta=venta,
                idproducto=detalle['idproducto'],
                cantidad=detalle['cantidad'],
                precio=detalle['precio'],
                subtotal=detalle['subtotal']
            )
        return JsonResponse({}, status=200) 


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venta 
    template_name = 'ventas/delete.html' 
    success_url = reverse_lazy('Super:venta_list') 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data() 
        context['title'] = 'Eliminación de Venta'
        context['grabar'] = 'Eliminar Venta' 
        context['description'] = f'¿Desea eliminar la venta N°{self.object.id}: {self.object.fecha}?' 
        context['back_url'] = self.success_url 
        return context 
    

class VentaDetailView(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs):
        try:
            venta = Venta.objects.get(idventa=request.GET.get('id')) 
            detalles = list(VentaDetalle.objects.filter(venta=venta).values()) 

            return JsonResponse({
                'venta': {
                    'id': venta.idventa,
                    'cliente': venta.cliente.get_full_name() if venta.cliente else None,
                    'vendedor': venta.vendedor.get_full_name() if venta.vendedor else None, 
                    'fecha': venta.fecha, 
                    'subtotal': venta.subtotal,
                    'iva': venta.iva,
                    'dscto': venta.dscto,
                    'total': venta.total
                },
                'detalles': detalles
            }, status=200)
        except Venta.DoesNotExist:
            return JsonResponse({'error': 'Venta no encontrada'}, status=404) 
        

class VentaPDFView(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs):
        idventa = self.kwargs.get('pk') 
        
        try:
            venta = Venta.objects.get(pk=idventa)  
        except Venta.DoesNotExist:
            return HttpResponse('Venta no encontrada', status=404)

        detalles = VentaDetalle.objects.filter(venta=venta)

        context = {
            'venta': venta,
            'detalles': detalles,
        } 

        template = get_template('ventas/factura_pdf.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="factura_{idventa}.pdf"' 

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF', status=500)
        return response






