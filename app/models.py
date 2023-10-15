from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=255, verbose_name='First Name')
    last_name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Last Name')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Username')
    chat_id = models.IntegerField(unique=True, verbose_name='Chat ID')
    status = models.BooleanField(default=False, verbose_name='Status')

    def __str__(self):
        return str(self.chat_id)

    class Meta:
        verbose_name = 'TelegramUser'
        verbose_name_plural = 'TelegramUsers'


class Brokers(models.Model):
    fullname = models.CharField(max_length=512, verbose_name='Full Name')
    mail = models.EmailField(verbose_name='Email')
    iscompany = models.BooleanField(default=False, verbose_name='Is Company')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Broker'
        verbose_name_plural = 'Brokers'


class Update(models.Model):
    name = models.CharField(null=True, blank=True,max_length=128, verbose_name='Name')
    vehicle_id = models.CharField(null=True, blank=True, max_length=256, verbose_name='Vehicle ID')
    current_location = models.CharField(null=True, blank=True,max_length=256, verbose_name='Current Location')
    destination = models.CharField(null=True, blank=True, default='-', max_length=256, verbose_name='Destination')
    eta = models.CharField(null=True, blank=True,max_length=256, verbose_name='ETA')
    planned_time = models.DateTimeField(null=True, blank=True, verbose_name='Planned Time')
    eta_status = models.CharField(null=True, blank=True,max_length=20, verbose_name='ETA Status')
    status = models.CharField(null=True, blank=True,max_length=20, verbose_name='Status')
    fuel = models.CharField(null=True, blank=True,max_length=30, verbose_name='Fuel Percent')
    link = models.URLField(null=True, blank=True,verbose_name='Link')
    live_share = models.URLField(null=True, blank=True,verbose_name='Live Share')
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name='Updated At')
    broker = models.ForeignKey(Brokers, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Broker')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'


class MailTemplate(models.Model):
    title = models.CharField(max_length=128, verbose_name='Title', help_text='Max Length 128 symbols')
    subject = models.CharField(max_length=128, verbose_name='Subject', help_text='Max Length 128 symbols')
    context = models.TextField(verbose_name='Context')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mail Template'
        verbose_name_plural = 'Mail Templates'
