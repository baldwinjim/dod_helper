import sqlite3
import logging
from pathlib import Path
from flask import Flask, g, request, current_app, send_from_directory, jsonify, url_for, abort
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global Error Handlers
@app.errorhandler(sqlite3.Error)
def handle_database_error(e):
    logger.exception("Database error occurred")
    return jsonify({'error': 'Internal Server Error', 'details': 'A database error occurred.'}), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e.description)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not Found', 'message': str(e.description)}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.exception("An unhandled exception occurred")
    return jsonify({'error': 'Internal Server Error'}), 500



def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_db():
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # To get dict-like rows
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)


@app.route('/images/<path:imagePath>', methods=['GET'])
def image_get(imagePath):
    return send_from_directory('static', imagePath)

@app.route('/speakers', methods=['GET'])
def speakers_all_get():
    db = get_db()
    rows = db.execute("SELECT * FROM speakers").fetchall()
    return jsonify({'speakers': [dict(row) for row in rows]})
    
@app.route('/speakers/<string:conferenceId>', methods=['POST'])
def speakers_post(conferenceId):
    """
    Create a new speaker under the conference identified by conferenceId (from the URL).
    Expects JSON body: { "firstName": "...", "lastName": "..." }
    """
    logger.debug("POST /speakers called for conferenceId=%s", conferenceId)

    # Basic JSON / content-type validation
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    # Pull values and normalize
    firstName = (data.get('firstName') or '').strip()
    lastName = (data.get('lastName') or '').strip()

    # Basic required-field validation
    if not conferenceId or not firstName or not lastName:
        return jsonify({'error': 'conferenceId, firstName and lastName are required'}), 400

    db = get_db()

    # Parameterized query to avoid SQL injection
    cursor = db.execute(
        "INSERT INTO speakers (conferenceId, lastName, firstName) VALUES (?, ?, ?)",
        (conferenceId, lastName, firstName)
    )
    db.commit()

    new_id = cursor.lastrowid
    # Build resource URL (optional). Ensure you have a route to GET the individual speaker.
    location = url_for('speakers_get', conferenceId=conferenceId, _external=False)

    response_body = {
        'id': new_id,
        'conferenceId': conferenceId,
        'firstName': firstName,
        'lastName': lastName
    }
    return jsonify(response_body), 201, {'Location': f'{location}/{new_id}'}

@app.route('/speakers/<string:conferenceId>/<int:id>', methods=['PUT'])
def speakers_put(conferenceId, id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    field_mapping = {
        'firstName': 'firstname',
        'lastName': 'lastname',
        'email': 'email',
        'bio': 'bio', 
        'phone': 'phone',
        'profilepic': 'profilepic'
    }

    updates = {}
    values = []
    
    for json_key, db_col in field_mapping.items():
        if json_key in data:
            updates[db_col] = data[json_key]
            values.append(data[json_key])

    if not updates:
        return jsonify({'error': 'No valid fields to update provided'}), 400

    set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
    values.append(conferenceId)
    values.append(id)

    db = get_db()
    cursor = db.execute(f"UPDATE speakers SET {set_clause} WHERE conferenceId = ? AND id = ?", values)
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': f'No speaker found with id {id} for conference {conferenceId}'}), 404

    return jsonify({'message': 'Speaker updated successfully'}), 200

@app.route('/speakers/<string:conferenceId>/<int:id>', methods=['DELETE'])
def speakers_delete(conferenceId, id):
    # conferenceId and id are guaranteed to be present by the route definition
    # but strictly checking as in original code
    if not conferenceId or not id:
        return jsonify({'error': 'conferenceId and id values are required'}), 400
        
    db = get_db()
    cursor = db.execute("DELETE FROM speakers WHERE conferenceId = ? AND id = ?", (conferenceId, id))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': f'No speaker found with id {id} for conference {conferenceId}'}), 404
        
    return jsonify({'result': f'Speaker with id {id} from conference {conferenceId} deleted successfully.'}), 200

@app.route('/speakers/<string:conferenceId>', methods=['GET'])
def speakers_get(conferenceId):
    if not conferenceId:
        return jsonify({'error': 'conferenceId value is required'}), 400
        
    db = get_db()
    rows = db.execute("SELECT * FROM speakers WHERE conferenceId = ?", (conferenceId,)).fetchall()
    return jsonify({'conferenceId': conferenceId, 'speakers': [dict(row) for row in rows]})




@app.route('/sponsors', methods=['GET'])
def sponsors_get_all():
     # Optional: keep this for getting all, or filter?
    db = get_db()
    rows = db.execute("SELECT * FROM sponsors").fetchall()
    return jsonify({'sponsors': [dict(row) for row in rows]})

@app.route('/sponsors/<string:conferenceId>', methods=['POST'])
def sponsors_post(conferenceId):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400

    logo = data.get('logo', '')
    url = data.get('url', '')
    level = data.get('level', '')

    db = get_db()
    cursor = db.execute(
        "INSERT INTO sponsors (conferenceId, name, logo, url, level) VALUES (?, ?, ?, ?, ?)",
        (conferenceId, name, logo, url, level)
    )
    db.commit()

    return jsonify({
        'id': cursor.lastrowid, 
        'conferenceId': conferenceId,
        'name': name,
        'logo': logo, 
        'url': url, 
        'level': level
    }), 201

@app.route('/sponsors/<string:conferenceId>', methods=['GET'])
def sponsors_get(conferenceId):
    db = get_db()
    rows = db.execute("SELECT * FROM sponsors WHERE conferenceId = ?", (conferenceId,)).fetchall()
    return jsonify({'conferenceId': conferenceId, 'sponsors': [dict(row) for row in rows]})

@app.route('/sponsors/<string:conferenceId>/<int:id>', methods=['PUT'])
def sponsors_put(conferenceId, id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    # Fields that can be updated
    allowed_fields = ['name', 'logo', 'url', 'level']
    updates = {}
    values = []

    for field in allowed_fields:
        if field in data:
            updates[field] = data[field]
            values.append(data[field])

    if not updates:
        return jsonify({'error': 'No valid fields to update provided'}), 400

    set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
    values.append(conferenceId)
    values.append(id)

    db = get_db()
    cursor = db.execute(f"UPDATE sponsors SET {set_clause} WHERE conferenceId = ? AND id = ?", values)
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': f'No sponsor found with id {id} for conference {conferenceId}'}), 404

    return jsonify({'message': 'Sponsor updated successfully'}), 200

@app.route('/sponsors/<string:conferenceId>/<int:id>', methods=['DELETE'])
def sponsors_delete(conferenceId, id):
    db = get_db()
    cursor = db.execute("DELETE FROM sponsors WHERE conferenceId = ? AND id = ?", (conferenceId, id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': f'No sponsor found with id {id} for conference {conferenceId}'}), 404

    return jsonify({'result': f'Sponsor with id {id} from conference {conferenceId} deleted successfully.'}), 200


@app.route('/conferences', methods=['GET', 'POST'])
def conferences():
    db = get_db()
    if request.method == 'GET':
        rows = db.execute('SELECT * FROM conferences').fetchall()
        return jsonify({'conferences': [row[0] for row in rows]})
    else:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON body'}), 400
            
        city = data.get('city', '').lower().replace(' ', '-')
        year = data.get('year')
        
        if not city:
             return jsonify({'error': 'City is required'}), 400
             
        try:
            year_int = int(year)
            if not (1900 <= year_int <= 2100):
                raise ValueError("Year out of range")
        except (ValueError, TypeError):
             return jsonify({'error': 'Invalid year provided'}), 400
            
        confId = f'{year_int}-{city}'
        
        # Check if exists
        if db.execute("SELECT 1 FROM conferences WHERE conferenceId = ?", (confId,)).fetchone():
            return jsonify({'error': f'{confId} already exists!'}), 409
            
        cursor = db.execute("INSERT INTO conferences (conferenceId) VALUES (?)", (confId,))
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'conferenceID': confId}), 201

@app.route('/upload/<string:conferenceId>', methods=['POST'])
def upload_file(conferenceId):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    upload_type = request.form.get('type')
    if upload_type not in ['speaker', 'company']:
        return jsonify({'error': 'Invalid or missing upload type. Must be "speaker" or "company"'}), 400

    if upload_type == 'speaker':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        if not first_name or not last_name:
            return jsonify({'error': 'firstName and lastName are required for speaker uploads'}), 400
        # sanitary inputs
        safe_first = secure_filename(first_name).lower()
        safe_last = secure_filename(last_name).lower()
        filename_base = f"{safe_first}-{safe_last}"
    else: # company
        company_name = request.form.get('companyName')
        if not company_name:
            return jsonify({'error': 'companyName is required for company uploads'}), 400
        safe_company = secure_filename(company_name).lower()
        filename_base = safe_company

    # Preserve extension
    ext = Path(file.filename).suffix.lower()
    if not ext:
         # Default or error? Let's just allow it or warn. 
         # secure_filename might have stripped it if it was weird, but Path(..).suffix should capture it.
         ext = '' 
    
    final_filename = f"{filename_base}{ext}"

    # Directory handling
    # We assume 'static' is in the same dir as this file
    base_dir = Path(current_app.root_path) 
    # If app.root_path points to where api_server.py is (because Flask(name)), then 'static' should be there.
    # Note: app = Flask(__name__) makes root_path the dir of api_server.py
    
    target_dir = base_dir / 'static' / conferenceId
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / final_filename
    file.save(str(target_path))

    return jsonify({
        'message': 'File uploaded successfully', 
        'url': f"/images/{conferenceId}/{final_filename}"
    }), 201

if __name__ == '__main__':
    # Use pathlib to resolve the database path relative to this script
    BASE_DIR = Path(__file__).resolve().parent
    # Database is now in the same directory as api_server.py
    DB_PATH = BASE_DIR / 'dod_helper.db'
    
    app.config['DATABASE'] = str(DB_PATH)
    
    # Ensure the data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    init_app(app) # Register the close_db function
    with app.app_context():
        init_db() # Initialize the database tables
    app.run(debug=True)
