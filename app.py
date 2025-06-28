import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carmarket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

CORS(app)
db = SQLAlchemy(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Models ---

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)
    engine_volume = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.String(20))
    mileage_unit = db.Column(db.String(10))
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    features = db.Column(db.Text)
    transmission = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('CarPhoto', backref='car', lazy=True, cascade='all, delete-orphan')

class CarPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

# --- API Endpoints ---

@app.route('/api/cars', methods=['POST'])
def upload_car():
    try:
        # Get form data
        data = request.form
        features = request.form.getlist('features')
        photos = request.files.getlist('photos')

        car = Car(
            manufacturer=data.get('manufacturer', ''),
            model=data.get('model', ''),
            year=data.get('year', ''),
            category=data.get('category', ''),
            fuel_type=data.get('fuelType', ''),
            engine_volume=data.get('engineVolume', ''),
            price=float(data.get('price', 0)),
            mileage=data.get('mileage', ''),
            mileage_unit=data.get('mileageUnit', ''),
            description=data.get('description', ''),
            title=data.get('title', ''),
            color=data.get('color', ''),
            location=data.get('location', ''),
            contact_name=data.get('contact_name', ''),
            contact_email=data.get('contact_email', ''),
            contact_phone=data.get('contact_phone', ''),
            features=','.join(features),
            transmission=data.get('transmission', '')
        )
        db.session.add(car)
        db.session.flush()  # Get car.id

        # Save photos
        for i, file in enumerate(photos):
            if file and file.filename:
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4().hex}{ext}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                photo = CarPhoto(
                    car_id=car.id,
                    filename=filename,
                    is_primary=(i == 0)
                )
                db.session.add(photo)

        db.session.commit()
        return jsonify({"message": "Car uploaded successfully!", "car_id": car.id}), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()  # <-- Add this line for debugging
        return jsonify({"error": "Failed to upload car", "details": str(e)}), 500

@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.order_by(Car.created_at.desc()).all()
    result = []
    for car in cars:
        photos = [
            f"/uploads/{photo.filename}" for photo in car.photos
        ]
        result.append({
            "id": car.id,
            "manufacturer": car.manufacturer,
            "model": car.model,
            "year": car.year,
            "category": car.category,
            "fuel_type": car.fuel_type,
            "engine_volume": car.engine_volume,
            "price": car.price,
            "mileage": car.mileage,
            "mileage_unit": car.mileage_unit,
            "description": car.description,
            "title": car.title,
            "color": car.color,
            "location": car.location,
            "contact_name": car.contact_name,
            "contact_email": car.contact_email,
            "contact_phone": car.contact_phone,
            "features": car.features.split(',') if car.features else [],
            "transmission": car.transmission,
            "created_at": car.created_at.isoformat(),
            "photos": photos
        })
    return jsonify(result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Serve index.html at root
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve other static files (css, js, html, etc.)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# --- DB Init ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

