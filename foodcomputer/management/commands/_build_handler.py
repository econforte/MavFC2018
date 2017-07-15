from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token

from experiment.models import *
from foodcomputer.models import *


class DataBuilder(object):

    def clear_tables(self):
        day_num = Day.objects.all().delete()[0]
        device_num = DeviceType.objects.all().delete()[0]
        return day_num, device_num

    def build_days(self):
        Day(id=1, name='Monday').save()
        Day(id=2, name='Tuesday').save()
        Day(id=3, name='Wednesday').save()
        Day(id=4, name='Thursday').save()
        Day(id=5, name='Friday').save()
        Day(id=6, name='Saturday').save()
        Day(id=7, name='Sunday').save()
        return True

    def build_data_types(self):
        DataType(id=1, name='Boolean', descr='True/False represented by a 1 or a 0').save()
        DataType(id=2, name='Float', descr='decimal number').save()
        return True

    def build_unit_types(self):
        UnitType(id=1, name='Degrees Celsius', abbr='C', descr='Conversion of Celsius to Fahrenheit:   F = C * 9/5 + 32 Measurement of Temperature.', min_limit=-5, max_limit=40).save()
        UnitType(id=2, name='On/Off', abbr='1/0', descr='Describes if something is turned on or off.', min_limit=0, max_limit=1).save()
        UnitType(id=3, name='pH', abbr='pH', descr='It\'s just pH.', min_limit=0, max_limit=14).save()
        UnitType(id=4, name='Electrical Conductivity', abbr='EC', descr='Amount of electrolytes in the water.', min_limit=0, max_limit=10).save()
        UnitType(id=5, name='Luminous Intensity', abbr='CD', descr='Luminous Intensity is the "photometric quantity" as lumens per steradian (lm/sr). '
                                                             'It is abbreviated as CD here to represent candela, another name for Luminous Intensity.', min_limit=0, max_limit=10000).save()
        UnitType(id=6, name='Wavelength', abbr='WAVE', descr='Measured in nanometers (nm), wavelength in the food computer sense usually '
                                                       'refers to the PAR sensor, which measures photosynthesis.', min_limit=0, max_limit=300).save()
        UnitType(id=7, name='Absolute Humidity', abbr='AH', descr='AH is the mass of the water vapor divided by the net volume of both the air and the vapor.', min_limit=0, max_limit=100).save()
        UnitType(id=8, name='Parts Per Million', abbr='PPM', descr='Number of particles of interest divided by total number of particles. '
                                                             'If refering to CO2, it is the number of CO2 molecules divided by the '
                                                             'number of all molecules, in any given volume of the air. '
                                                             'It may also refer to solid or liquid proportions.', min_limit=0, max_limit=100).save()
        return True

    def build_device_types(self):
        DeviceType(name='pH Sensor', model_id='SWPH 1', unit_type_id=3, data_type_id=1, is_controller=False, bio_threshold=0.4).save()
        DeviceType(name='EC Sensor', model_id='SWEC 1', unit_type_id=4, data_type_id=1, is_controller=False, bio_threshold=0.9).save()
        DeviceType(name='Water Thermometer', model_id='SWTM 1', unit_type_id=1, data_type_id=1, is_controller=False, bio_threshold=2).save()
        DeviceType(name='Light Intensity', model_id='SLIN 1', unit_type_id=5, data_type_id=1, is_controller=False, bio_threshold=1).save()
        DeviceType(name='Photosynthetically Active Radiation Sensor', model_id='SLPA 1', unit_type_id=6, data_type_id=1, is_controller=False, bio_threshold=15).save()
        DeviceType(name='Air Thermometer', model_id='SATM 1', unit_type_id=1, data_type_id=1, is_controller=False, bio_threshold=2).save()
        DeviceType(name='Humidity Sensor', model_id='SAHU 1', unit_type_id=7, data_type_id=1, is_controller=False, bio_threshold=0.6).save()
        DeviceType(name='CO2 Sensor', model_id='SACO 1', unit_type_id=8, data_type_id=1, is_controller=False, bio_threshold=1).save()
        DeviceType(name='Shell', model_id='SGSO 1', unit_type_id=2, data_type_id=2, is_controller=False, bio_threshold=0).save()
        DeviceType(name='Window', model_id='SGWO 1', unit_type_id=2, data_type_id=2, is_controller=False, bio_threshold=0).save()
        DeviceType(name='Air Conditioner', model_id='AAAC 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Humidity P', model_id='AAHU 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Ventilation', model_id='AAVE 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Circulation', model_id='AACR 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='MB Light', model_id='ALMI 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='RGB Growth Light Red', model_id='ARGB 2', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='LED Grow Light left', model_id='ALPN 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Air Pump', model_id='AAAP 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Heater', model_id='AAHE 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='Water Pump', model_id='WP', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='LED Grow Light right', model_id='ALPN 2', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='RGB Growth Light Green', model_id='ARGB 1', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        DeviceType(name='RGB Growth Light Blue', model_id='ARGB 3', unit_type_id=2, data_type_id=2, is_controller=True, bio_threshold=0).save()
        return True

    def build_fc_user(self):
        try:
            user = User.objects.get(username='genericFCuser')
        except ObjectDoesNotExist:
            user = User.objects.create_user(username='genericFCuser', password='tempPW-asddsa123321')
        user.is_active=True
        token = Token.objects.get_or_create(user=user)
        user.set_password(token[0].key)
        user.save()
        return token[0].key