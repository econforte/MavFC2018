from django.core.management.base import BaseCommand
from ._build_handler import DataBuilder


class Command(BaseCommand):
    help = 'adds all needed records to the database'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing tables. Please note this will also delete any devices, '
                          'all device data, controller update records, and experiment rules. '
                          'It will not delete Pis or experiemnts but pis will need to re-init all their devices.')
        db = DataBuilder()
        num = db.clear_tables()
        if num:
            self.stdout.write(str(num[0]) + ' days were deleted and ' + str(num[1]) + ' device types were deleted.')
        if db.build_days():
            self.stdout.write('days built')
        if db.build_unit_types():
            self.stdout.write('unit types built')
        if db.build_data_types():
            self.stdout.write('data types built')
        if db.build_device_types():
            self.stdout.write('device types built')
        k = db.build_fc_user()
        if k:
            self.stdout.write('Generic food computer user was built and assigned the token: ' + k)
        self.stdout.write(self.style.SUCCESS('Successfully built all required data records.'))
