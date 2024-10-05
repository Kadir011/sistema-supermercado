from django.views.generic import TemplateView

class SectionView(TemplateView):
    template_name = "options/section.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Secciones'
        return context 
    

