from django.urls import path

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("duplicates", hello.views.duplicates, name="duplicates"),
    path("payins", hello.views.payin, name="payins"),
    path("payouts", hello.views.payout, name="payouts"),
    path("revenue", hello.views.revenue, name="revenue"),
    path("transactions/<int:transaction_id>", hello.views.transactions, name="transactions")
]
