from django.views.generic import TemplateView

from .services import search_database


class GlobalSearchView(TemplateView):
    template_name = 'search/results.html'
    context_object_name = 'results'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        results = search_database(query)

        context['query'] = query
        context['results'] = results

        return context
