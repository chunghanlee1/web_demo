from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.
User = get_user_model()

class FinancialInfo(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='financial_info')
    slug=models.SlugField(allow_unicode=True, null=True, default=None)
    income=models.PositiveIntegerField()
    income_growth=models.FloatField()
    spending=models.PositiveIntegerField()
    inflation=models.FloatField()
    savings=models.PositiveIntegerField()
    current_age=models.PositiveIntegerField()
    death_age=models.PositiveIntegerField()
    retirement_age=models.PositiveIntegerField()

    #Specify possible choices
    investment_risk_choices=[(1,'Extremely Safe'),
                             (3, 'Low Risk'),
                             (5, 'Moderate Risk'),
                             (7, 'Risky'),
                             (9, 'Very Risky')
                            ]
    investment_risk=models.PositiveIntegerField(choices=investment_risk_choices, default=1)

    FWB1_3_choices= list(zip(['Not at all','Very little','Somewhat','Very well','Completely','Refused'],['Not at all','Very little','Somewhat','Very well','Completely','Refused']))
    FWB1_5_choices= list(zip(['Not at all','Very little','Somewhat','Very well','Completely','Refused'],['Not at all','Very little','Somewhat','Very well','Completely','Refused']))
    FWB1_6_choices= list(zip(['Not at all','Very little','Somewhat','Very well','Completely','Refused'],['Not at all','Very little','Somewhat','Very well','Completely','Refused']))
    FWB2_1_choices= list(zip(['Never','Rarely', 'Sometimes', 'Often', 'Always', 'Refused'],['Never','Rarely', 'Sometimes', 'Often', 'Always', 'Refused']))
    FWB2_3_choices= list(zip(['Never','Rarely', 'Sometimes', 'Often', 'Always', 'Refused'],['Never','Rarely', 'Sometimes', 'Often', 'Always', 'Refused']))
    
    FWB1_3=models.CharField(max_length=300, choices=FWB1_3_choices, default='Refused')
    FWB1_5=models.CharField(max_length=300, choices=FWB1_5_choices, default='Refused')
    FWB1_6=models.CharField(max_length=300, choices=FWB1_6_choices, default='Refused')
    FWB2_1=models.CharField(max_length=300, choices=FWB2_1_choices, default='Refused')
    FWB2_3=models.CharField(max_length=300, choices=FWB2_3_choices, default='Refused')

    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        self.slug=slugify(self.user.username)
        super().save(*args, **kwargs)