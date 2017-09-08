# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class StockInfo(models.Model):
    reportCode = models.CharField(max_length=10)
    marketNo = models.IntegerField()

    class Meta:
        unique_together=("reportCode", "marketNo")
