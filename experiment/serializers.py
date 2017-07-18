from rest_framework import serializers
from .models import ExperimentInstance, Experiment, ExperimentRule, UserExperimentInstance, Day

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')


class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day
        fields = ('id', 'name')


class ExperimentRuleSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = ExperimentRule
        fields = ('id', 'device', 'hour', 'minute', 'baseline_target', 'days', 'get_threshold')
        # depth = 1


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
        fields = ('id', 'start', 'end', 'active', 'experiment')
        # fields = '__all__'
        # depth = 1


class ExperimentBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = '__all__'


class ExperimentRuleBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExperimentRule
        fields = '__all__'


class ExperimentInstanceBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExperimentInstance
        fields = '__all__'


class UserExperimentInstanceBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExperimentInstance
        fields = '__all__'
