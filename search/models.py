from django.db import models


# Create your models here.
class Vegetable(models.Model):
    UNIT_TYPE = (
        ('n', '普通'),
        ('w', '水菜')
    )
    veg_name = models.CharField(max_length=16, verbose_name='蔬菜名', db_index=True)
    veg_type = models.CharField(max_length=1, choices=UNIT_TYPE, default='n')

    def __str__(self):
        return "id: {} veg_name: {}".format(self.id, self.veg_name)


class Record(models.Model):
    veg_name = models.CharField(max_length=16, default='', verbose_name='蔬菜名')
    vegetable = models.ForeignKey(Vegetable, verbose_name='所属蔬菜')

    lowest_price = models.IntegerField(verbose_name='最低价格')
    avg_price = models.IntegerField(verbose_name='平均价格')
    highest_price = models.IntegerField(verbose_name='最高价格')
    created_at = models.DateField(verbose_name='日期', auto_now=True)

    def __str__(self):
        return """veg: {}
low: {}\t avg: {}\t high: {}\t
@ {}""".format(self.veg_name, self.lowest_price, self.avg_price, self.highest_price, self.created_at)

    def as_dict(self):
        return {
            'veg_name': self.veg_name,
            'lowest_price': self.lowest_price,
            'avg_price': self.avg_price,
            'highest_price': self.highest_price,
            'created_at': self.created_at
        }
