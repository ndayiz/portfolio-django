from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_skill_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='issued_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='year',
        ),
    ]
