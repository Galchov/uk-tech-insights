from rest_framework import serializers

from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'logo', 'description', 'website',
            'foundation_date', 'formatted_foundation_date', 'location',
            'address', 'operating_countries', 'industries', 'tech_stack'
        ]
        read_only_fields = ['slug', 'formatted_foundation_date']
        