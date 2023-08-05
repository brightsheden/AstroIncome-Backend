
from django.core.management.base import BaseCommand
from ...models import Investment, Profile
from django.contrib.auth.models import User
from datetime import date, timedelta, timezone

class Command(BaseCommand):
 
    def handle(self, *args, **kwargs):
        today = date.today()
        user = request.user
        profile = user.profile
        print(profile)
        print(today)
        investments = Investment.objects.filter(completed=False)

        for x in investments:
            start_date = x.createdAt.date()
            end_date = start_date + timedelta(days=7)

            if end_date < today :
                investment = Investment.objects.get(pk=x._id)
                investment.completed = True
                investment.endAt = date.now()
                investment.save()

                profile.balance += 10/100 * investment.amount
                profile.investment_wallet = 0
                profile.save()







