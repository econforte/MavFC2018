from rest_framework import serializers
from .models import ExperimentInstance

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')


class ExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExperimentInstance
        fields = ('id', 'name', 'pi', 'collection_interval', 'experiment_rules')
        depth = 1


class ExperimentInstanceSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer

    class Meta:
        model = ExperimentInstance
        fields = '__all__'
        depth = 1