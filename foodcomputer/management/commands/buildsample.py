from django.core.management.base import BaseCommand

from foodcomputer.models import *
from foodcomputer.serializers import *
from experiment.serializers import *

from ._sample_data import data


class Command(BaseCommand):
    help = 'adds all needed records to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample food computer to the database.')

        p1a = Address(name='UNO PKI', street_line_1='1110 S 67th St', city='Omaha', state='NE', zip='68182').save()
        p1 = Pi(id=1, name='Sample Food Computer', pi_SN='abcaseasyas123', address=p1a, manual_control=False).save()


        self.stdout.write('Sample food computer devices to the database.')
        device_data = [
            {"id": 1, "pi": 1, "device_id": "pH Sensor", "residual_threshold": 0.2, "device_type": 1},
            {"id": 2, "pi": 1, "device_id": "EC Sensor", "residual_threshold": 0.3, "device_type": 2},
            {"id": 3, "pi": 1, "device_id": "Water Temp Sensor", "residual_threshold": 0.1, "device_type": 3},
            {"id": 4, "pi": 1, "device_id": "Light Intensity Sensor", "residual_threshold": 0, "device_type": 4},
            {"id": 5, "pi": 1, "device_id": "PAR", "residual_threshold": 3.5, "device_type": 5},
            {"id": 6, "pi": 1, "device_id": "Air Temperature Sensor", "residual_threshold": 0.3, "device_type": 6},
            {"id": 7, "pi": 1, "device_id": "Humidity Sensor", "residual_threshold": 0.2, "device_type": 7},
            {"id": 8, "pi": 1, "device_id": "CO2 Sensor", "residual_threshold": 0, "device_type": 8},
            {"id": 9, "pi": 1, "device_id": "Shell", "residual_threshold": 0, "device_type": 9},
            {"id": 10, "pi": 1, "device_id": "Window", "residual_threshold": 0, "device_type": 10},
            {"id": 12, "pi": 1, "device_id": "Heater", "residual_threshold": 0, "device_type": 19},
            {"id": 13, "pi": 1, "device_id": "AC", "residual_threshold": 0, "device_type": 11},
            {"id": 14, "pi": 1, "device_id": "Humidity Spray", "residual_threshold": 0, "device_type": 12},
            {"id": 15, "pi": 1, "device_id": "Ventilation", "residual_threshold": 0, "device_type": 13},
            {"id": 16, "pi": 1, "device_id": "Circulation", "residual_threshold": 0, "device_type": 14},
            {"id": 17, "pi": 1, "device_id": "MB Light", "residual_threshold": 0, "device_type": 15},
            {"id": 18, "pi": 1, "device_id": "Red Light", "residual_threshold": 0, "device_type": 16},
            {"id": 19, "pi": 1, "device_id": "Blue Light", "residual_threshold": 0, "device_type": 23},
            {"id": 20, "pi": 1, "device_id": "Green Light", "residual_threshold": 0, "device_type": 22},
            {"id": 21, "pi": 1, "device_id": "Left Light", "residual_threshold": 0, "device_type": 17},
            {"id": 22, "pi": 1, "device_id": "Right Light", "residual_threshold": 0, "device_type": 21},
            {"id": 23, "pi": 1, "device_id": "Air Pump", "residual_threshold": 0, "device_type": 18},
        ]

        device_serializer = deviceSerializer(data=device_data, many=True)
        if device_serializer.is_valid():
            device_serializer.save()

            self.stdout.write('Adding sample food computer device data (22,000 records) to the database. This may take about 30 - 40 minutes to complete.')

            data_serializer = dataSerializer(data=data, many=True)
            if data_serializer.is_valid():
                data_serializer.save()
                self.stdout.write('The sample food computer was added to the database successfully.')
            else:
                self.stdout.write('The sample food computer\'s data failed to be added to the database.')
        else:
            self.stdout.write('The sample food computer\'s devices failed to be added to the database.')



        self.stdout.write('Adding sample experiments to the database.')
        experiments = [
            {"id": 1,"name": "Basil","descr": "15 hour day growth cycle.","collection_interval": 5,"pi": 1},
            {"id": 2,"name": "Large Strawberries","descr": "Grow large strawberries","collection_interval": 5,"pi": 1},
            {"id": 3,"name": "Juicy Strawberries","descr": "Grow Juicy Strawberries","collection_interval": 5,"pi": 1},
            {"id": 4,"name": "Fast Mint","descr": "Grow Mint quickly","collection_interval": 5,"pi": 1},
            {"id": 5,"name": "Strong Mint","descr": "Grow Stronger Quality Mint leaves.","collection_interval": 5,"pi": 1}
        ]
        exp_serializer = ExperimentBasicSerializer(data=experiments, many=True)
        if exp_serializer.is_valid():
            exp_serializer.save()
            self.stdout.write('The sample experiments were added to the database successfully.')

            self.stdout.write('Adding sample experiments rules to the database.')
            rules = [
                {
                    "id": 3,
                    "hour": 10,
                    "minute": 15,
                    "baseline_target": 1.0,
                    "device": 6,
                    "experiment": 1,
                    "days": [
                        1,
                        2,
                        3,
                        4,
                        5
                    ]
                },
                {
                    "id": 4,
                    "hour": 18,
                    "minute": 45,
                    "baseline_target": 65.0,
                    "device": 5,
                    "experiment": 1,
                    "days": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ]
                }
            ]
            rule_serializer = ExperimentRuleBasicSerializer(data=rules, many=True)
            if rule_serializer.is_valid():
                rule_serializer.save()
                self.stdout.write('The sample experiment rules were added to the database successfully.')

                instances = [
                    {
                        "id": 1,
                        "start": "2017-03-05T18:26:39Z",
                        "end": "2017-03-05T18:26:42Z",
                        "active": False,
                        "experiment": 2
                    },
                    {
                        "id": 2,
                        "start": "2017-03-08T06:00:00Z",
                        "end": "2017-03-10T06:00:00Z",
                        "active": False,
                        "experiment": 5
                    },
                    {
                        "id": 3,
                        "start": "2017-03-22T05:00:00Z",
                        "end": "2017-03-24T05:00:00Z",
                        "active": True,
                        "experiment": 1
                    }
                ]
                rule_serializer = ExperimentInstanceBasicSerializer(data=instances, many=True)
                if rule_serializer.is_valid():
                    rule_serializer.save()
                    self.stdout.write('The sample experiment instances were added to the database successfully.')

                else:
                    self.stdout.write('The sample experiments instances failed to be added to the database.')
            else:
                self.stdout.write('The sample experiments rules failed to be added to the database.')
        else:
            self.stdout.write('The sample experiments failed to be added to the database.')


        self.stdout.write(self.style.SUCCESS('Successfully built all required data records.'))
