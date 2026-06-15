"""
routes/main.py - Home page route
"""

from flask import Blueprint, render_template
from models.database import Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    featured = Product.query.order_by(Product.id.desc()).limit(4).all()
    return render_template("index.html", featured_products=featured)