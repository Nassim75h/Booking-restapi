from django import forms
from django.contrib import admin
from .models import Message,Conversation

class MessageAdmin(forms.ModelForm):
    class Meta:
        model=Message
        fields="__all__"
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        if self.instance and self.instance.conversation:
            self.fields['sender'].queryset=self.instance.conversation.participants.all()

