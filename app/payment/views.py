from flask import Blueprint, flash
from flask import request, render_template

from .forms import PaymentForm
from .methods import MethodRequestResponseError
from .services import do_payment
from .settings import CurrencyCode

payment_bp = Blueprint("payment", __name__, template_folder="templates",)


@payment_bp.route("/", methods=["POST", "GET"])
def payment_main():
    form = PaymentForm(request.form)

    if request.method == "POST" and form.validate():
        currency_code = CurrencyCode(int(form.currency.data))

        try:
            return do_payment(
                form.amount.data, currency_code, form.description.data
            )
        except MethodRequestResponseError as e:
            flash(str(e))

    return render_template("main.html", form=form)
