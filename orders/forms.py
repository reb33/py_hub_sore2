import re

from django import forms
from django.core.exceptions import ValidationError


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ]
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ]
    )

    def clean_phone_number(self):  # валидатор для phone_number, автоматически подтягивается по названию метода clean_
        data = self.cleaned_data["phone_number"]

        if not data.isdigit():
            raise ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r"\d{10}")
        if not pattern.match(data):
            raise ValidationError("Неверный формат номера")

        return data
