from rest_framework import serializers
from .models import ExperimentInstance, Experiment, ExperimentRule

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')


class ExperimentRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExperimentRule
        fields = ('id', 'device', 'hour', 'minute', 'baseline_target', 'days')
        depth = 1


class ExperimentSerializer(serializers.ModelSerializer):
    experiment_rules = ExperimentRuleSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment
        fields = ('id', 'name', 'pi', 'collection_interval', 'experiment_rules')
        # depth = 1


class ExperimentInstanceSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer(read_only=True)

    class Meta:
        model = ExperimentInstance
        fields = ('id', 'start', 'end', 'current', 'experiment')
        # fields = '__all__'
        # depth = 1