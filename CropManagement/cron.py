



from CropManagement.models import MobileRemainder
from django_cron import CronJobBase,Schedule

from twilio.rest import Client
class RemindJob(CronJobBase):
    RUN_EVERY_MINS = 0.1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CropManagement.remind_job'

    def do(self):
        remind = MobileRemainder.objects.first()
        mobile_number = remind.mobile_no
        mobile_number = '+91'+mobile_number
        water_time = remind.water_remind
        print(water_time)
        print(mobile_number)
        account_sid = 'AC062178d3463fafaf0a8b544ae9601c19'
        auth_token = 'b433c64321419877897401b57a6a5632'
        client = Client(account_sid, auth_token)
        client.messages.create(from_='+12568278181', to=[mobile_number], body="Reminder for war=tering")


