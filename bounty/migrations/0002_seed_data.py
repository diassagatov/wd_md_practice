# Prefills the database with 5 criminals and 10 hunt logs.
# Runs once, automatically, as part of `python manage.py migrate`.
from django.db import migrations

CRIMINALS = [
    dict(name='Vicious', nickname='The Red Dragon Blade', reward=25000000,
         latitude=35.6762, longitude=139.6503, location_note='Tharsis, Mars. Red Dragon syndicate HQ.',
         difficulty=10, armed=True, has_crew=True, escape_master=True),
    dict(name=None, nickname='Mad Pierrot', reward=6000000,
         latitude=None, longitude=None, location_note='Seen near the Callisto amusement park.',
         difficulty=9, armed=True, has_crew=False, escape_master=True),
    dict(name='Asimov Solensan', nickname='Red Eye Dealer', reward=2500000,
         latitude=-12.5, longitude=45.3, location_note='',
         difficulty=6, armed=True, has_crew=False, escape_master=False),
    dict(name='Abdul Hakim', nickname='Thousand Faces', reward=3000,
         latitude=40.7128, longitude=-74.0060, location_note='Changes face often, last seen at Mars spaceport.',
         difficulty=4, armed=False, has_crew=False, escape_master=True),
    dict(name='Twinkle Maria Murdock', nickname='Space Warriors Leader', reward=8000,
         latitude=None, longitude=None, location_note='Old retirement colony on Io.',
         difficulty=3, armed=True, has_crew=True, escape_master=False),
]

# (criminal index in CRIMINALS, success, notes)
HUNTS = [
    (0, False, 'Ambushed at the cathedral. Target had backup and vanished.'),
    (0, False, 'Tracked to Tharsis HQ, too many guards to engage.'),
    (1, False, 'Target escaped through an asteroid field.'),
    (1, False, 'Bullets did not hurt him. Retreated.'),
    (2, False, 'Chased through the space highway gate, lost him.'),
    (2, True, 'Caught after his ship ran out of fuel.'),
    (3, False, 'Arrested the wrong guy, real Hakim swapped faces.'),
    (3, True, 'Recognised by his walk at the casino. Captured.'),
    (4, False, 'Crew of retired pilots outmanoeuvred us.'),
    (4, True, 'Surrendered after a long dogfight.'),
]


def seed(apps, schema_editor):
    WantedCriminal = apps.get_model('bounty', 'WantedCriminal')
    HuntLog = apps.get_model('bounty', 'HuntLog')
    criminals = [WantedCriminal.objects.create(**data) for data in CRIMINALS]
    for index, success, notes in HUNTS:
        HuntLog.objects.create(criminal=criminals[index], success=success, notes=notes)


def unseed(apps, schema_editor):
    apps.get_model('bounty', 'HuntLog').objects.all().delete()
    apps.get_model('bounty', 'WantedCriminal').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('bounty', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]
