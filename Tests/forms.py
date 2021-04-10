from django import forms
from .models import Test, TestTask

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'picture']


class TestTaskForm(forms.ModelForm):
    class Meta:
        model = TestTask
        fields = [
            'type', 'title', 'task_statement',
            'correct_answer', 'points'
            ]
