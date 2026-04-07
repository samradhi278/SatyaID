PROJECT OVERVIEW
================================================================================

A document verification system backend for verifying PAN (Permanent Account Number) 
documents and Aadhaar cards using computer vision and OCR technologies.

SatyaID is a Flask-based backend application that provides document verification 
services through a multi-step validation process:
1. Text Verification - OCR-based text extraction and validation
2. Template Matching - Document structure and format verification
3. Face Matching - Biometric face matching against documents


This system is implemented as a sandbox-style simulation inspired by DigiLocker APIs for
academic and development purposes, and does not integrate with any official DigiLocker 
infrastructure.

================================================================================
PROJECT STRUCTURE
================================================================================

backend/
├── modules/                    # Core verification modules
│   ├── text_verification.py   # OCR and text validation
│   ├── template_matching.py   # Document template validation
│   ├── face_matching.py       # Face recognition and matching
│   └── report_generator.py    # Report generation (empty)
├── utils/                      # Utility functions
│   ├── helpers.py             # Helper functions (empty)
│   └── preprocessing.py       # Image preprocessing (empty)
├── database/                   # Database-related files
├── models/                     # ML models directory
├── aadhar_verification.py     # Aadhaar verification module
└── pan_verification.py        # PAN verification module


================================================================================
FEATURES
================================================================================

1. User Management
   - User registration and authentication
   - Official/Verifier role management
   - Admin dashboard for user approval
   - Email notifications for status updates

2. Document Verification
   - Multi-step verification process
   - Text extraction using OCR (Tesseract)
   - Template matching for document authenticity
   - Face verification against stored documents

3. Role-Based Access
   - Users: Submit documents for verification
   - Officials: Manage user accounts and approvals
   - Admins: Manage official accounts and approvals

4. Email Integration
   - Gmail SMTP configuration for notifications
   - Automated approval/rejection emails
   - Login link distribution


================================================================================
TECHNOLOGY STACK
================================================================================

Framework & Libraries
   - Flask: Web framework
   - Flask-CORS: Cross-origin request handling
   - Flask-Mail: Email functionality

Computer Vision & OCR
   - OpenCV (cv2): Image processing
   - Tesseract: Optical character recognition
   - pytesseract: Python wrapper for Tesseract
   - Pillow: Image manipulation
   - ImageHash: Image hashing and comparison
   - SciPy: Scientific computing

Other Dependencies
   - NumPy: Numerical operations
   - PyWavelets: Wavelet transforms


================================================================================
INSTALLATION
================================================================================

Prerequisites
   - Python 3.1+
   - Tesseract-OCR installed on system
     Windows: C:\Program Files\Tesseract-OCR\tesseract.exe
     Linux: sudo apt-get install tesseract-ocr
     macOS: brew install tesseract

Setup Steps

1. Clone the repository
   git clone https://github.com/samradhi278/SatyaID.git
   cd SatyaID

2. Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Configure Tesseract path (if needed)
   Edit app.py and update the path:
   pytesseract.pytesseract.tesseract_cmd = r"path/to/tesseract.exe"

5. Run the application
   python app.py

The application will start at http://localhost:5000


================================================================================
API ENDPOINTS
================================================================================

Document Verification
   POST /verify
   - Request: Multipart form-data with image file
   - Response: JSON with verification status

Authentication
   POST /login - User/Official login
   POST /register - User registration
   POST /official_register - Official registration
   GET /logout - Session logout

User Management
   GET /user-details - User details page
   POST /user-details - Save user details
   GET /dashboard - User dashboard

Official Management
   GET /official-details - Official details page
   POST /official-details - Save official details
   GET /official_dashboard - Official verification dashboard
   POST /accept-user/<index> - Approve user
   POST /reject-user/<index> - Reject user
   GET /official_login - Official login

Admin Management
   GET /admin_dashboard - Admin dashboard
   GET /accept/<index> - Approve official
   GET /reject/<index> - Reject official


================================================================================
VERIFICATION PROCESS
================================================================================

The document verification endpoint (/verify) follows this workflow:

1. File Upload
   ↓
2. Text Verification (text_verification.py)
   ↓ (Check: Text validity, format, required fields)
   ↓
3. Template Matching (template_matching.py)
   ↓ (Check: Document structure, template validity)
   ↓
4. Face Verification (face_matching.py)
   ↓ (Check: Face matching with document)
   ↓
5. Result: PASSED or FAILED


================================================================================
CONFIGURATION
================================================================================

Mail Configuration
   Update email settings in app.py:
   
   app.config['MAIL_SERVER'] = 'smtp.gmail.com'
   app.config['MAIL_PORT'] = 587
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'

Flask Configuration
   - Secret Key: satyaid_secret_key (change in production)
   - CORS: Enabled for cross-origin requests
   - Debug Mode: Currently enabled (disable in production)


================================================================================
FILE HANDLING
================================================================================

Uploaded documents are saved to: backend/uploads/
Current filename: user_upload.jpg (single file, overwrites on each upload)


================================================================================
SECURITY NOTES - FOR PRODUCTION USE
================================================================================

⚠️ IMPORTANT:
   - Change the secret key to a secure random string
   - Move sensitive credentials to environment variables
   - Disable debug mode (debug=False)
   - Use HTTPS instead of HTTP
   - Implement proper password hashing
   - Add database instead of in-memory lists
   - Add CSRF protection


================================================================================
DEVELOPMENT ROADMAP
================================================================================

   - Complete aadhar_verification.py module
   - Complete pan_verification.py module
   - Implement helpers.py utility functions
   - Implement preprocessing.py image preprocessing
   - Implement report_generator.py for verification reports
   - Database integration (replace in-memory storage)
   - Enhanced security and authentication
   - Unit tests and integration tests
   - API documentation (Swagger/OpenAPI)


================================================================================
CONTRIBUTING
================================================================================

1. Fork the repository
2. Create a feature branch: git checkout -b feature/your-feature
3. Commit changes: git commit -am 'Add feature'
4. Push to branch: git push origin feature/your-feature
5. Submit a pull request


================================================================================
SUPPORT
================================================================================

For issues, questions, or contributions, please open an issue on the GitHub 
repository.

Repository: https://github.com/samradhi278/SatyaID
