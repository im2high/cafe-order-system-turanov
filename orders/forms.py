from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Order, OrderItem


SORT_LABELS = (
    ("oldest", "Сначала старые"),
    ("newest", "Сначала новые"),
    ("employee", "По сотруднику"),
)


class OrderFilterForm(forms.Form):
    q = forms.CharField(label="Поиск по сотруднику или блюду", required=False)
    employee = forms.CharField(label="Имя сотрудника", required=False)
    date = forms.DateField(
        label="Дата заказа",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )
    status = forms.ChoiceField(
        label="Статус", choices=[("", "Все"), *Order.Status.choices], required=False
    )
    hide_cancelled = forms.BooleanField(label="Скрыть отменённые", required=False)
    sort = forms.ChoiceField(label="Сортировка", choices=SORT_LABELS, required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("employee", "order_date")
        widgets = {
            "order_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def clean_order_date(self):
        order_date = self.cleaned_data["order_date"]
        if order_date < timezone.localdate() and order_date != self.instance.order_date:
            raise forms.ValidationError("Дата заказа не может быть в прошлом.")
        return order_date

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        order_date = cleaned_data.get("order_date")
        if not employee or not order_date:
            return cleaned_data

        orders = Order.objects.active().for_date(order_date).filter(employee=employee)
        if self.instance.pk:
            orders = orders.exclude(pk=self.instance.pk)
        if orders.exists():
            raise forms.ValidationError("У сотрудника уже есть активный заказ на эту дату.")
        return cleaned_data


class OrderItemForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Количество", min_value=1)

    class Meta:
        model = OrderItem
        fields = ("dish", "quantity")


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=0, min_num=1, validate_min=True
)
