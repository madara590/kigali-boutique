"""
models/database.py - PostgreSQL schema definition
Tables: Product, Customer, Order, OrderItem
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    category    = db.Column(db.String(60), nullable=False)
    image_url   = db.Column(db.String(255), nullable=True)
    stock       = db.Column(db.Integer, default=50)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship("OrderItem", back_populates="product")

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "price":       float(self.price),
            "category":    self.category,
            "image_url":   self.image_url,
            "stock":       self.stock,
        }


class Customer(db.Model):
    __tablename__ = "customers"
    id         = db.Column(db.Integer, primary_key=True)
    full_name  = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(20), nullable=False)
    address    = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders     = db.relationship("Order", back_populates="customer")


class Order(db.Model):
    __tablename__ = "orders"
    id             = db.Column(db.Integer, primary_key=True)
    customer_id    = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    total_amount   = db.Column(db.Numeric(12, 2), nullable=False)
    status         = db.Column(db.String(30), default="pending")
    payment_method = db.Column(db.String(30), default="momo")
    momo_ref       = db.Column(db.String(60), nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    customer       = db.relationship("Customer", back_populates="orders")
    items          = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    order      = db.relationship("Order", back_populates="items")
    product    = db.relationship("Product", back_populates="order_items")

    @property
    def subtotal(self):
        return float(self.quantity) * float(self.unit_price)


def init_db():
    db.create_all()
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Ankara Wrap Dress", category="Dresses", price=35000, stock=20,
                    description="Vibrant Ankara print wrap dress, perfect for celebrations.",
                    image_url="https://images.unsplash.com/photo-1594938298603-c8148c4b4389?w=400"),
            Product(name="Kente Print Blouse", category="Tops", price=18000, stock=35,
                    description="Light cotton blouse with traditional Kente-inspired print.",
                    image_url="https://images.unsplash.com/photo-1551163943-3f6a855d1153?w=400"),
            Product(name="Modern Kitenge Skirt", category="Skirts", price=22000, stock=15,
                    description="A-line skirt in bold Kitenge fabric, midi length.",
                    image_url="https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400"),
            Product(name="Men's Safari Shirt", category="Men", price=25000, stock=25,
                    description="Breathable linen safari shirt with two chest pockets.",
                    image_url="https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400"),
            Product(name="Beaded Clutch Bag", category="Accessories", price=12000, stock=40,
                    description="Hand-beaded clutch bag made by Kigali artisans.",
                    image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400"),
            Product(name="African Print Sneakers", category="Footwear", price=45000, stock=18,
                    description="Canvas sneakers with unique African wax-print uppers.",
                    image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
            Product(name="Satin Dashiki Top", category="Tops", price=15000, stock=30,
                    description="Flowy satin Dashiki in jewel tones, unisex fit.",
                    image_url="https://images.unsplash.com/photo-1618886614638-80e3c103d31a?w=400"),
            Product(name="Tie-Dye Maxi Dress", category="Dresses", price=28000, stock=22,
                    description="Hand-dyed maxi dress using traditional Rwandan techniques.",
                    image_url="https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400"),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()
        print("✅ Database seeded with sample products.")