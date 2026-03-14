from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            password=make_password('admin123'),
            is_superuser=True,
            is_staff=True,
            is_verified=True,
            role='super_admin',
            email='admin@example.com'
        )

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_agentinvitation'),
    ]
    operations = [
        migrations.RunPython(create_admin),
    ]
