from django.db import migrations


def set_domain(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Sites = apps.get_model('sites', 'Site')
    Sites.objects.all().delete()
    # Generate SITE_ID = 1
    Sites.objects.create(domain="127.0.0.1:8000", name="Main site")


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(set_domain),
    ]
