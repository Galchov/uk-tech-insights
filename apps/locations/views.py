from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DeleteView


from .models import Country, City
from .forms import LocationForm
from .mixins import ModeratorAccessMixin


class LocationListView(ModeratorAccessMixin, View):
    def get(self, request):
        cities = City.objects.select_related('country').order_by('country__name', 'name')
        return render(request, 'locations/location_list.html', {'cities': cities})


class LocationCreateView(ModeratorAccessMixin, View):
    def get(self, request):
        form = LocationForm()
        return render(request, 'locations/location_form.html', {
            'form': form,
            'is_new': True
        })

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country_name'].strip()
            city_name = form.cleaned_data['city_name'].strip()

            country, created = Country.objects.get_or_create(name__iexact=country_name, defaults={'name': country_name})

            if City.objects.filter(name__iexact=city_name, country=country).exists():
                form.add_error('city_name', 'This city already exists for the given country.')
            else:
                City.objects.create(name=city_name, country=country)
                return redirect('locations:location_list')

        return render(request, 'locations/location_form.html', {
            'form': form,
            'is_new': True
        })


class LocationEditView(ModeratorAccessMixin, View):
    def get(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        form = LocationForm(initial={
            'city_name': city.name,
            'country_name': city.country.name
        })
        return render(request, 'locations/location_form.html', {
            'form': form,
            'city': city,
            'is_new': False
        })

    def post(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        form = LocationForm(request.POST)

        if form.is_valid():
            country_name = form.cleaned_data['country_name'].strip()
            city_name = form.cleaned_data['city_name'].strip()

            country, created = Country.objects.get_or_create(name__iexact=country_name, defaults={'name': country_name})
            city.name = city_name
            city.country = country
            city.save()
            return redirect('locations:location_list')

        return render(request, 'locations/location_form.html', {
            'form': form,
            'city': city,
            'is_new': False
        })


class LocationDeleteView(ModeratorAccessMixin, DeleteView):
    model = City
    template_name = 'locations/location_confirm_delete.html'
    context_object_name = 'location'
    success_url = reverse_lazy('locations:location_list')
    