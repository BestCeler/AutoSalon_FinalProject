from django.forms import ModelForm

from orders.models import Order, OrderLine


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["number", "date","shop_address"]

    labels = {
        "client" : "client"
    }

class OrderLineForm(ModelForm):
    class Meta:
        model = OrderLine
        exclude = ["order", "product", "price", "warranty"]

        labels = {
            "quantity" : "number of items",
        }