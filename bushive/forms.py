from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit

class busform(ModelForm):
    class Meta:
        model=Bus
        fields='__all__'
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        

class RouteSearchForm(forms.Form):
    start_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'From Station', 'style': 'padding: 15px; border: 2px solid black; border-radius: 5px; width: 100%;'
    }))
    end_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'To Station', 'style': 'padding: 15px; border: 2px solid black; border-radius: 5px; width: 100%;'
    }))
    departure_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local', 'placeholder': 'Departure Time', 'style': 'padding: 15px; border: 2px solid black; border-radius: 5px; width: 100%;'
    }))

class BuspaymentForm(forms.ModelForm):
   class Meta:
        model = Buspayment
        fields = '__all__'

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'amount',
            Submit('submit', 'Submit', css_class='button_white btn-block btn-primary')
        )
        self.helper.form_show_labels = True

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'trip', 'seat_number',]
        widgets = {
            'reservation_status': forms.Select(choices=Reservation.STATUS_CHOICES),
        }

    # class Meta:
    #     model=Buspayment
    #     fields='__all__' 
        
    # def __init__(self,*args, **kwargs):
    #         super().__init__(*args,**kwargs)
    #         self.helper = FormHelper(self)
    #         self.helper.layout=Layout(
    #             'name',
    #             'amount',
    #             Submit('submit',css_class='button_white btn-block btn-primary')
    #         )
    #         self.helper.form_show_labels = False

# class Busform(forms.ModelForm):
#     class Meta:
#         model=Bus
#         fields = ['bus_number']
        
# class RouteForm(forms.ModelForm):
#     class Meta:
#         model=Route
#         fields=['start_location','end_']