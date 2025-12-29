from rest_framework import serializers
from .models import School
from rest_framework import serializers
from manager.models import SchoolApplication


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id', 'name', 'address', 'country', 'region', 'locality',
            'principal_name', 'contact_email', 'contact_phone', 'domain',
            'website', 'established_year', 'number_of_students', 'school_type',
            'description', 'logo', 'status', 'comment', 'admin_user',
        ]
        read_only_fields = ['id', 'status', 'admin_user']


class SchoolApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolApplication
        fields = ['id', 'name', 'applicant_name', 'applicant_email', 'applicant_phone', 'status']
        read_only_fields = ['id', 'status']
