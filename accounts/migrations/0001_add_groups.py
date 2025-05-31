from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for name in ["Sales", "Warehouse", "Customer"]:
        Group.objects.get_or_create(name=name)

class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(create_groups),
    ]
