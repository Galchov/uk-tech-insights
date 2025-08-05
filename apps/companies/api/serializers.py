from rest_framework import serializers

from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    operating_countries = serializers.SerializerMethodField()
    industries = serializers.SerializerMethodField()
    tech_stack = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'name', 'slug', 'logo', 'description', 'website',
            'foundation_date', 'formatted_foundation_date', 'location',
            'address', 'operating_countries', 'industries', 'tech_stack'
        ]
        read_only_fields = ['slug', 'formatted_foundation_date']

    def get_location(self, obj):
        if obj.location:
            return str(obj.location)
        return None

    def get_operating_countries(self, obj):
        return [str(country) for country in obj.operating_countries.all()]

    def get_industries(self, obj):
        return [str(industry) for industry in obj.industries.all()]

    def get_tech_stack(self, obj):
        return [str(tech) for tech in obj.tech_stack.all()]
    