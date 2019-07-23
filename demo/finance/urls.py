from django.urls import path
from finance import views

app_name='finance'
urlpatterns = [
    path('', views.FinanceIndexView.as_view(), name='index'),
    path('create/', views.FinanceCreateView.as_view(), name='create'),
    path('update/<slug>/', views.FinanceUpdateView.as_view(), name='update'),
    path('req_return_analysis/<slug>/', views.ReqReturnView.as_view(), name='req_return'),
    path('simulation_analysis/<slug>/', views.SimulationView.as_view(), name='simulation'),
    path('prediction/<slug>/', views.PredictionView.as_view(), name='prediction'),
    path('profile/<slug>/',views.FinancialProfileView.as_view(),name='profile')
]