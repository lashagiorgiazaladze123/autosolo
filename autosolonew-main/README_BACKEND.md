# CarMarket Backend - Upload System

This is a Python Flask backend that handles car uploads from the HTML form. It includes a SQLite database to store car information and uploaded images.

## Features

- ✅ Car upload with all form fields
- ✅ Image upload and storage
- ✅ SQLite database for data persistence
- ✅ RESTful API endpoints
- ✅ CORS enabled for frontend integration
- ✅ Automatic database creation
- ✅ File upload handling

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Backend Server

```bash
python run_backend.py
```

Or directly:
```bash
python app.py
```

The server will start on `http://localhost:5001`

### 3. Database Structure

The system automatically creates two tables:

**Car Table:**
- id (Primary Key)
- manufacturer
- model
- year
- category
- fuel_type
- price
- description
- title
- location
- contact_name
- contact_email
- contact_phone
- created_at

**CarPhoto Table:**
- id (Primary Key)
- car_id (Foreign Key to Car)
- filename
- file_path
- is_primary

### 4. API Endpoints

#### Upload a Car
```
POST /api/cars
Content-Type: application/json

{
  "manufacturer": "Toyota",
  "model": "Camry",
  "year": 2020,
  "category": "sedan",
  "fuelType": "petrol",
  "price": 25000,
  "description": "Great condition car...",
  "title": "2020 Toyota Camry",
  "location": "New York, NY",
  "contact": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890"
  },
  "photos": ["base64_encoded_image_data"]
}
```

#### Get All Cars
```
GET /api/cars?page=1&per_page=10
```

#### Get Specific Car
```
GET /api/cars/{car_id}
```

#### Get Uploaded Images
```
GET /uploads/{filename}
```

### 5. File Structure

```
autosolonew-main/
├── app.py                 # Main Flask application
├── run_backend.py         # Server startup script
├── requirements.txt       # Python dependencies
├── carmarket.db          # SQLite database (created automatically)
├── uploads/              # Uploaded images folder (created automatically)
├── upload.html           # Frontend upload form
└── ... (other HTML files)
```

### 6. Integration with Frontend

The frontend (`upload.html`) is already configured to send data to `http://localhost:5001/api/cars`. The backend will:

1. Receive the form data
2. Save car information to the database
3. Process and save uploaded images
4. Return a success response

### 7. Error Handling

The backend includes error handling for:
- Missing required fields
- Invalid file uploads
- Database errors
- File system errors

### 8. Security Features

- File size limits (50MB max)
- File type validation (images only)
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration for frontend access

## Troubleshooting

### Common Issues:

1. **Port already in use**: Change the port in `app.py` line 89
2. **Database errors**: Delete `carmarket.db` and restart the server
3. **Upload folder issues**: Check permissions on the `uploads` folder
4. **CORS errors**: Ensure the frontend URL is allowed in CORS configuration

### Logs

The server runs in debug mode, so you'll see detailed logs in the console including:
- Request details
- Database operations
- File upload progress
- Error messages

## Next Steps

To enhance the system, consider adding:
- User authentication
- Image compression
- Search and filtering
- Admin panel
- Email notifications
- Payment integration 