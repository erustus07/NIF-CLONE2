# import os
# import uuid # For unique filenames
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from flask_migrate import Migrate
# from werkzeug.utils import secure_filename # For secure filenames

# from models import db, Category, Product, ContactMessage
# from config import Config

# app = Flask(__name__)
# app.config.from_object(Config)

# # Ensure the upload folder exists
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# # Initialize extensions
# db.init_app(app)
# migrate = Migrate(app, db)
# CORS(app) # Enable CORS for all routes by default

# # Helper function for allowed file extensions
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/')
# def index():
#     return jsonify({"message": "Welcome to NIFTAZ AFRICA ELECTRONICS API!"})

# # Serve uploaded files statically
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # --- API Endpoints ---

# # Categories CRUD
# @app.route('/categories', methods=['GET'])
# def get_categories():
#     categories = Category.query.all()
#     return jsonify([c.to_dict() for c in categories])

# @app.route('/categories', methods=['POST'])
# def add_category():
#     data = request.json
#     name = data.get('name')
#     if not name:
#         return jsonify({"error": "Category name is required"}), 400
#     if Category.query.filter_by(name=name).first():
#         return jsonify({"error": "Category with this name already exists"}), 409

#     new_category = Category(name=name)
#     db.session.add(new_category)
#     db.session.commit()
#     return jsonify(new_category.to_dict()), 201

# @app.route('/categories/<int:id>', methods=['PUT'])
# def update_category(id):
#     category = Category.query.get_or_404(id)
#     data = request.json
#     name = data.get('name')
#     if not name:
#         return jsonify({"error": "Category name is required"}), 400
#     if Category.query.filter(Category.name == name, Category.id != id).first():
#         return jsonify({"error": "Category with this name already exists"}), 409

#     category.name = name
#     db.session.commit()
#     return jsonify(category.to_dict())

# @app.route('/categories/<int:id>', methods=['DELETE'])
# def delete_category(id):
#     category = Category.query.get_or_404(id)
#     if category.products:
#         return jsonify({"error": "Cannot delete category with associated products"}), 400

#     db.session.delete(category)
#     db.session.commit()
#     return jsonify({"message": "Category deleted successfully"}), 204

# # Products CRUD (with image upload)
# @app.route('/products', methods=['GET'])
# def get_products():
#     category_id = request.args.get('category_id')
#     search_term = request.args.get('search')
#     query = Product.query

#     if category_id:
#         query = query.filter_by(category_id=category_id)
#     if search_term:
#         query = query.filter(Product.name.ilike(f'%{search_term}%') | Product.description.ilike(f'%{search_term}%'))

#     products = query.all()
#     return jsonify([p.to_dict() for p in products])

# @app.route('/products/<int:id>', methods=['GET'])
# def get_product(id):
#     product = Product.query.get_or_404(id)
#     return jsonify(product.to_dict())

# @app.route('/products', methods=['POST'])
# def add_product():
#     # Use request.form for text data and request.files for files
#     name = request.form.get('name')
#     description = request.form.get('description')
#     price = request.form.get('price')
#     category_id = request.form.get('category_id')
#     image_file = request.files.get('image')

#     if not all([name, price, category_id]):
#         return jsonify({"error": "Missing required fields: name, price, category_id"}), 400

#     try:
#         price = float(price)
#         category_id = int(category_id)
#     except ValueError:
#         return jsonify({"error": "Invalid price or category_id format"}), 400

#     image_url = None
#     if image_file and allowed_file(image_file.filename):
#         filename = secure_filename(image_file.filename)
#         unique_filename = str(uuid.uuid4()) + '_' + filename
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#         image_file.save(file_path)
#         image_url = f"/uploads/{unique_filename}" # Store relative URL

#     new_product = Product(
#         name=name,
#         description=description,
#         price=price,
#         image_url=image_url,
#         category_id=category_id
#     )
#     db.session.add(new_product)
#     db.session.commit()
#     return jsonify(new_product.to_dict()), 201

# @app.route('/products/<int:id>', methods=['PUT'])
# def update_product(id):
#     product = Product.query.get_or_404(id)
#     # Use request.form for text data and request.files for files
#     name = request.form.get('name')
#     description = request.form.get('description')
#     price = request.form.get('price')
#     category_id = request.form.get('category_id')
#     image_file = request.files.get('image')
#     # Keep existing image_url if no new file is uploaded and no explicit removal
#     current_image_url = request.form.get('current_image_url') # Frontend sends this

#     if name: product.name = name
#     if description: product.description = description
#     if price:
#         try:
#             product.price = float(price)
#         except ValueError:
#             return jsonify({"error": "Invalid price format"}), 400
#     if category_id:
#         try:
#             product.category_id = int(category_id)
#         except ValueError:
#             return jsonify({"error": "Invalid category_id format"}), 400

#     if image_file and allowed_file(image_file.filename):
#         # Delete old image if it exists
#         if product.image_url and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1])):
#             os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1]))
#         filename = secure_filename(image_file.filename)
#         unique_filename = str(uuid.uuid4()) + '_' + filename
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#         image_file.save(file_path)
#         product.image_url = f"/uploads/{unique_filename}"
#     elif current_image_url is not None: # If frontend explicitly sends current_image_url, use it
#         product.image_url = current_image_url
#     elif 'image' in request.files and not image_file: # If image field was sent but empty, clear image
#         if product.image_url and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1])):
#             os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1]))
#         product.image_url = None # Set to None if image is removed

#     db.session.commit()
#     return jsonify(product.to_dict())

# @app.route('/products/<int:id>', methods=['DELETE'])
# def delete_product(id):
#     product = Product.query.get_or_404(id)
#     # Delete associated image file
#     if product.image_url:
#         image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1])
#         if os.path.exists(image_path):
#             os.remove(image_path)

#     db.session.delete(product)
#     db.session.commit()
#     return jsonify({"message": "Product deleted successfully"}), 204 # No Content

# # Contact Messages
# @app.route('/contact', methods=['POST'])
# def save_contact_message():
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     message = data.get('message')

#     if not all([name, email, message]):
#         return jsonify({"error": "Missing required fields: name, email, message"}), 400

#     new_message = ContactMessage(
#         name=name,
#         email=email,
#         message=message
#     )
#     db.session.add(new_message)
#     db.session.commit()
#     return jsonify(new_message.to_dict()), 201

# if __name__ == '__main__':
#     app.run(debug=True)