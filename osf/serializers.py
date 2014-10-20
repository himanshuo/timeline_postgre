__author__ = 'himanshu'
from django.forms import widgets
from rest_framework import serializers
from osf.models import Timeline


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ('id','title', 'author', 'wiki','project_id', 'date' )
