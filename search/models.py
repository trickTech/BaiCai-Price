from django.db import models


# Create your models here.
class ItemType(models.Model):
    """
    物品所属类别
    """
    type_name = models.CharField(max_length=16, db_index=True)
    created_at = models.DateTimeField(verbose_name='创建日期', auto_now=True)

    def __str__(self):
        return "<Item Type : {}>".format(self.type_name)


class Item(models.Model):
    """
    物品
    """

    class Meta:
        unique_together = ['item_name', 'item_type']

    item_name = models.CharField(max_length=16, verbose_name='商品名', db_index=True)
    item_unit = models.CharField(max_length=8, verbose_name='商品单位', default='')
    item_type = models.ForeignKey(ItemType, verbose_name='所属类型', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='创建日期', auto_now=True)

    def __str__(self):
        return "id: {} item: {}".format(self.id, self.item_name)


class Record(models.Model):
    """
    记录
    """

    class Meta:
        unique_together = ['item', 'recorded_at']

    # 冗余，是否保留待商议
    item_name = models.CharField(max_length=16, default='', verbose_name='物品名', db_index=True)
    item = models.ForeignKey(Item, verbose_name='所属物品', blank=True, null=True)

    unit = models.CharField(max_length=8, default='', verbose_name='单位')
    lowest_price = models.IntegerField(verbose_name='最低价格')
    avg_price = models.IntegerField(verbose_name='平均价格')
    highest_price = models.IntegerField(verbose_name='最高价格')
    recorded_at = models.DateField(verbose_name='记录日期', auto_now=True)
    created_at = models.DateTimeField(verbose_name='创建日期', auto_now=True)

    def __str__(self):
        return """item record: {}
low: {}\t avg: {}\t high: {}\t
@ {}""".format(self.item_name, self.lowest_price, self.avg_price, self.highest_price, self.created_at)

    def as_dict(self):
        return {
            'id': self.item_id,
            'item_name': self.item_name,
            'lowest_price': self.lowest_price,
            'avg_price': self.avg_price,
            'highest_price': self.highest_price,
            'recorded_at': self.recorded_at
        }
