from allauth.account.forms import SignupForm 
from django import forms

class CustomSignupForm(SignupForm):
    address = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=25, widget=forms.Textarea)
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        if(self.cleaned_data['address']):
            user.address = str(self.cleaned_data['address'])

        if(self.cleaned_data['contact']):
            user.contact = str(self.cleaned_data['contact'])

        user.save()
        return user