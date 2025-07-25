from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance. This will be bound to the Flask app later.
db = SQLAlchemy()

class Category(db.Model):
    """
    Represents a product category in the database.
    Products are associated with categories.
    """
    __tablename__ = 'categories' # Explicitly set table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Define a relationship with the Product model.
    # 'products' will be a list of Product objects associated with this category.
    # backref='category' creates a 'category' attribute on the Product model
    # that refers back to the parent Category object.
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        """Converts the Category object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        """String representation for debugging."""
        return f"<Category {self.name}>"

class Product(db.Model):
    """
    Represents a product in the database.
    Each product belongs to a category.
    """
    __tablename__ = 'products' # Explicitly set table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text) # Text type for longer descriptions
    price = db.Column(db.Float, nullable=False) # Float for decimal prices
    image_url = db.Column(db.String(255)) # URL or path to the product image
    # Foreign Key: Links to the 'id' column of the 'categories' table
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Timestamp for last update

    def to_dict(self):
        """Converts the Product object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category_id': self.category_id,
            # Include category name for easier frontend display
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        """String representation for debugging."""
        return f"<Product {self.name} (Ksh {self.price})>"

class ContactMessage(db.Model):
    """
    Represents a message submitted through the contact form.
    """
    __tablename__ = 'contact_messages' # Explicitly set table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Timestamp for submission

    def to_dict(self):
        """Converts the ContactMessage object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        """String representation for debugging."""
        return f"<ContactMessage from {self.name} ({self.email})>"