from django.shortcuts import render
from finance.forms import FinancialInfoForm
from finance.models import FinancialInfo
from django.views.generic import CreateView, UpdateView, TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.
#Run functions need LoginRequiredMixin and custom check that user has filled financial info

class FinanceIndexView(TemplateView):
    template_name='finance/index.html'
    
    def get_context_data(self, **kwargs):
        storage=messages.get_messages(self.request)
        context=super().get_context_data(**kwargs)
        context['messages']=storage
        return context

class FinanceCreateView(LoginRequiredMixin,CreateView):
    model=FinancialInfo
    form_class=FinancialInfoForm
    template_name='finance/input_financial_info.html'
    #Need to login to user profile page eventually
    success_url=reverse_lazy('finance:index')

    #Associate user with received info
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        messages.success(self.request, "Information Created!")
        return super().form_valid(form)


class FinanceUpdateView(LoginRequiredMixin,UpdateView):
    form_class=FinancialInfoForm
    model=FinancialInfo
    template_name='finance/input_financial_info.html'
    #Need to login to user profile page eventually
    success_url=reverse_lazy('finance:index')
    #Add a success message
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        messages.success(self.request, "Information Updated!")
        return super().form_valid(form)


from finance import health_check

class ReqReturnView(LoginRequiredMixin, TemplateView):
    template_name='finance/req_return.html'
    context_object_name='object'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        q=FinancialInfo.objects.get(user__id=self.request.user.id)
        userIncome=q.income
        incomeGrowth=q.income_growth
        userSpending=q.spending
        inflation=q.inflation
        userSavings=q.savings
        userCurrentAge=q.current_age
        userDeathAge=q.death_age
        userRetirementAge=q.retirement_age
        diagnosis=health_check.reqReturnHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, userCurrentAge, userDeathAge, userRetirementAge)
        context['diagnosis']=diagnosis
        return context

class SimulationView(LoginRequiredMixin, TemplateView):
    template_name='finance/simulation.html'
    context_object_name='object'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        q=FinancialInfo.objects.get(user__id=self.request.user.id)
        userIncome=q.income
        incomeGrowth=q.income_growth
        userSpending=q.spending
        inflation=q.inflation
        userSavings=q.savings
        investmentRisk=q.investment_risk
        userCurrentAge=q.current_age
        userDeathAge=q.death_age
        userRetirementAge=q.retirement_age
        diagnosis=health_check.simHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge)
        context['diagnosis'], context['script'], context['div']=diagnosis
        return context


from finance.prediction import encoding_order,predictor_description,make_prediction
class PredictionView(LoginRequiredMixin, TemplateView):
    template_name='finance/prediction.html'
    context_object_name='object'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        q=FinancialInfo.objects.get(user__id=self.request.user.id)
        
        if q.FWB1_3:
            #Make Predictions
            selection_dict={p:getattr(q,p) for p in encoding_order}
            results=make_prediction(selection_dict, encoding_order)
            #append results to context
            context['diagnosis']=results
        return context

class FinancialProfileView(LoginRequiredMixin,DetailView):
    context_object_name='financial_info'
    model=FinancialInfo
    template_name='finance/profile.html'
    def get_context_data(self, **kwargs):
        
        context=super().get_context_data(**kwargs)
        
        for k,v in predictor_description.items():
            key=k+'_description'
            context[key]=str(v)
            
        return context