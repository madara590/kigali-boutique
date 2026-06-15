"""
routes/cart.py - Shopping cart logic stored in Flask session
"""

from flask import Blueprint, session, request, jsonify, render_template, redirect, url_for
from models.database import Product

cart_bp = Blueprint("cart", __name__)


def get_cart():
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def cart_total(cart):
    return sum(item["price"] * item["quantity"] for item in cart.values())


def cart_count(cart):
    return sum(item["quantity"] for item in cart.values())


@cart_bp.route("/cart")
def view_cart():
    cart = get_cart()
    total = cart_total(cart)
    count = cart_count(cart)
    return render_template("cart.html", cart=cart, total=total, count=count)


@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    data       = request.get_json()
    product_id = str(data.get("product_id"))
    quantity   = int(data.get("quantity", 1))

    product = Product.query.get(int(product_id))
    if not product:
        return jsonify({"success": False, "message": "Product not found."}), 404

    cart = get_cart()

    if product_id in cart:
        cart[product_id]["quantity"] += quantity
    else:
        cart[product_id] = {
            "product_id": product.id,
            "name":       product.name,
            "price":      float(product.price),
            "quantity":   quantity,
            "image_url":  product.image_url or "",
        }

    session.modified = True

    return jsonify({
        "success":    True,
        "message":    f'"{product.name}" added to cart!',
        "cart_count": cart_count(cart),
    })


@cart_bp.route("/cart/update", methods=["POST"])
def update_cart():
    data       = request.get_json()
    product_id = str(data.get("product_id"))
    quantity   = int(data.get("quantity", 0))

    cart = get_cart()

    if product_id in cart:
        if quantity <= 0:
            del cart[product_id]
        else:
            cart[product_id]["quantity"] = quantity

    session.modified = True
    updated_cart = get_cart()

    return jsonify({
        "success":    True,
        "cart_count": cart_count(updated_cart),
        "total":      cart_total(updated_cart),
        "items":      list(updated_cart.values()),
    })


@cart_bp.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session.modified = True
    return jsonify({
        "success":    True,
        "cart_count": cart_count(cart),
        "total":      cart_total(cart),
    })


@cart_bp.route("/api/cart")
def api_cart():
    cart = get_cart()
    return jsonify({
        "items":      list(cart.values()),
        "total":      cart_total(cart),
        "cart_count": cart_count(cart),
    })