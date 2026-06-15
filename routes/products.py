"""
routes/products.py - Product catalog routes
"""

from flask import Blueprint, render_template, request, jsonify
from models.database import Product, db

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def catalog():
    category = request.args.get("category", "")
    query = Product.query

    if category:
        query = query.filter_by(category=category)

    products = query.order_by(Product.name).all()
    all_categories = db_distinct_categories()

    return render_template(
        "products.html",
        products=products,
        categories=all_categories,
        active_category=category,
    )


@products_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)


@products_bp.route("/api/products")
def api_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


def db_distinct_categories():
    rows = db.session.query(Product.category).distinct().all()
    return sorted([r[0] for r in rows])