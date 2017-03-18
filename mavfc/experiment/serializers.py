from rest_framework import serializers

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')
