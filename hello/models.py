from dateutil.parser import parse
from django.db import models
import pytz


class PayinsManager(models.Manager):
    def create_payin(self, amount, timestamp, transaction_id):
        timestamp = pytz.utc.localize(parse(timestamp))
        return self.create(amount=amount, timestamp=timestamp, transaction_id=transaction_id)


class Payins(models.Model):
    timestamp = models.DateTimeField()
    transaction_id = models.BigIntegerField()
    amount = models.FloatField()

    objects = PayinsManager()


class PayoutsManager(models.Manager):
    def create_payout(self, amount, timestamp, transaction_id):
        timestamp = pytz.utc.localize(parse(timestamp))
        return self.create(amount=amount, timestamp=timestamp, transaction_id=transaction_id)


class Payouts(models.Model):
    timestamp = models.DateTimeField()
    transaction_id = models.BigIntegerField()
    amount = models.FloatField()

    objects = PayoutsManager()
