from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    InvItem = apps.get_model("inv", "InventoryItem")
    
    admin_group, _ = Group.objects.get_or_create(name="Admin")


    ct = ContentType.objects.get_for_model(InvItem)
    needed_codenames = ["view_inv", "change_inv"]

    perms = Permission.objects.filter(content_type=ct, codename__in=needed_codenames)
    admin_group.permissions.add(*perms)

def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Admin").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0005_inventoryitem_calibration_date_and_more'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]