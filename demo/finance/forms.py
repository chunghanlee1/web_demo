from finance.models import FinancialInfo
from django.core import validators
from django import forms
from finance.prediction import predictor_description, encoding_order

#model form
#form validation
class FinancialInfoForm(forms.ModelForm):
    #age from 1-100
    current_age=forms.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(120)])
    death_age=forms.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(120)])
    retirement_age=forms.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(120)])
    class Meta:
        exclude=['user', 'slug']
        model=FinancialInfo
    
    def clean(self):
        print('validator activated')
        cleaned_data=super().clean()
        c=cleaned_data['current_age']
        r=cleaned_data['retirement_age']
        d=cleaned_data['death_age']
        #current age <= retirement age 
        if c>r:
            raise forms.ValidationError('Your retirement age must be greater than or equal to your current age. If you have retired please set your current and retirement ages equal.')
        #current age < death age
        if c>=d:
            raise forms.ValidationError('Your death age must be greater than your current age. Otherwise the planning functionality is not applicable to you!')

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for p in encoding_order:
            self.fields[p].label='Survey Item: '+predictor_description[p]


