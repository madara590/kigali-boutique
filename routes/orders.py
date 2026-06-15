"""
routes/orders.py - Checkout, MoMo payment, order saving
"""

import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.database import db, Customer, Order, OrderItem
from routes.cart import get_cart, cart_total

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout")
def checkout():
    cart = get_cart()
    if not cart:
        return redirect(url_for("cart.view_cart"))
    total = cart_total(cart)
    return render_template("checkout.html", cart=cart, total=total)


@orders_bp.route("/checkout", methods=["POST"])
def place_order():
    cart = get_cart()
    if not cart:
        return redirect(url_for("cart.view_cart"))

    customer = Customer(
        full_name = request.form.get("full_name"),
        email     = request.form.get("email"),
        phone     = request.form.get("phone"),
        address   = request.form.get("address"),
    )
    db.session.add(customer)
    db.session.flush()

    total = cart_total(cart)
    order = Order(
        customer_id    = customer.id,
        total_amount   = total,
        status         = "pending",
        payment_method = "momo",
    )
    db.session.add(order)
    db.session.flush()

    for pid, item in cart.items():
        order_item = OrderItem(
            order_id   = order.id,
            product_id = item["product_id"],
            quantity   = item["quantity"],
            unit_price = item["price"],
        )
        db.session.add(order_item)

    db.session.commit()
    session["pending_order_id"] = order.id

    return redirect(url_for("orders.payment_screen", order_id=order.id))


@orders_bp.route("/payment/<int:order_id>")
def payment_screen(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("payment.html", order=order)


@orders_bp.route("/payment/confirm", methods=["POST"])
def confirm_payment():
    order_id = session.get("pending_order_id")
    if not order_id:
        return redirect(url_for("main.index"))

    order = Order.query.get_or_404(order_id)
    mock_ref = "MOMO-" + uuid.uuid4().hex[:6].upper()
    order.status   = "paid"
    order.momo_ref = mock_ref
    db.session.commit()

    session.pop("cart", None)
    session.pop("pending_order_id", None)

    return redirect(url_for("orders.order_confirmation", order_id=order.id))


@orders_bp.route("/order/<int:order_id>")
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("confirmation.html", order=order)