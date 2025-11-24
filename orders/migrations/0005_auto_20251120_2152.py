from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_auto_20251120_2151"),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=50, unique=True, blank=True),
        ),
    ]