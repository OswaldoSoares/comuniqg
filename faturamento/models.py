from django.db import models


# Create your models here.
class Fatura(models.Model):
    id = models.AutoField(primary_key=True)
    fatura = models.IntegerField(default=0)

    db_table = "faturamento_fatura"
