from django.forms import ModelForm
from .models import Expense

class ExpenseForm(ModelForm):

    class Meta:
        model = Expense
        fields = ('name','amount','category')

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
