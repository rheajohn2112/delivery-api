from flask import Flask,request,jsonify
from datetime import datetime,timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
jwt = JWTManager(app)


database_url = os.environ.get('DATABASE_URL')

if not database_url:
    raise RuntimeError("DATABASE_URL environment variable not set!")

# Handle common issue with PostgreSQL URLs on Render
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
else:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

# SQLite DB path inside instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("Connecting to database:", database_url)

db = SQLAlchemy(app)

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.String(80), unique=True, nullable=False)
    client_name = db.Column(db.String(120))
    origin = db.Column(db.String(120))
    destination = db.Column(db.String(120))
    status = db.Column(db.String(120))
    expected_delivery_date = db.Column(db.Date, nullable=False)
    actual_delivery_date = db.Column(db.Date, nullable=True)
    on_time=db.Column(db.Boolean,nullable=False)


class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")


    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

@app.route('/')
def home():
    return {"message": "Delivery API is running successfully!"}

@app.route('/register',methods=['POST'])
def add_user():
    data=request.get_json()
    if not data:
        return jsonify({'error':"No data"}),404
    
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({'error': f'Missing or empty field: {field}'}), 400

    username=data['username']
    password=data['password']
    role=data.get('role','user')
    data_exist=User.query.filter_by(username=username).first()
    if data_exist:
        return jsonify({'error':'User Exist!'})
    else:
        userDetails = User(username=username,role=role)
        userDetails.set_password(password) 
    db.session.add(userDetails)
    db.session.commit()
    return {'message': f'User {username} added with role {role}!'}

@app.route('/login',methods=['POST'])
def check_login():
    data=request.get_json()
    if not data:
        return jsonify({'error':"No data"}),404
    
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({'error': f'Missing or empty field: {field}'}), 400

    username=data['username']
    password=data['password']
    data_exist=User.query.filter_by(username=username).first()
    if data_exist:
        chk=data_exist.check_password(password)
        if chk:
            print("Username value:", username, "Type:", type(username))

            access_token = create_access_token(
    identity=str(username), 
    additional_claims={"role": data_exist.role}
)

            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404


    





@app.route('/delivery', methods=['POST'])
@jwt_required()
def add_delivery_data():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Access denied. Admins only!'}), 403
    data_list = request.get_json()  # This will be a list of deliveries
    added_ids = []

    if not data_list:
        return jsonify({"error":"No data"})
    
    required_fields = ['packageid', 'client_name','origin','destination','status','expected_delivery_date','actual_delivery_date','on_time']
    for item in data_list:
        for field in required_fields:
            if field not in item or item[field] in [None, ""]:
                return jsonify({'error': f'Missing or empty field: {field}'}), 400



    for data in data_list:
        newDelivery = Delivery(
            packageid=data['packageid'],
            client_name=data['client_name'],
            origin=data['origin'],
            destination=data['destination'],
            status=data['status'],
            expected_delivery_date=datetime.strptime(data['expected_delivery_date'], "%Y-%m-%d").date(),
            actual_delivery_date=datetime.strptime(data['actual_delivery_date'], "%Y-%m-%d").date() if data['actual_delivery_date'] else None,
            on_time=data['on_time']
        )
        db.session.add(newDelivery)
        db.session.flush()  # gets the id before commit
        added_ids.append(newDelivery.id)

    db.session.commit()
    return jsonify({'message': 'Deliveries added successfully!', 'ids': added_ids})


@app.route('/delivery',methods=['GET'])
@jwt_required()
def get_delivery_details():
    query=Delivery.query

    status=request.args.get('status')
    client_name = request.args.get('client_name')
    on_time = request.args.get('on_time')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if status:
        query=query.filter(Delivery.status.ilike(f"%{status}%"))
    if client_name:
        query=query.filter(Delivery.client_name.ilike(f"%{client_name}%"))
    if origin:
        query=query.filter(Delivery.origin.ilike(f"%{origin}%"))
    if destination:
        query=query.filter(Delivery.destination.ilike(f"%{destination}%"))
    if on_time:
        on_time_bool=on_time.lower()=='true'
        query=query.filter(Delivery.on_time== on_time_bool)

    sort_by=request.args.get('sort_by')
    sort_order=request.args.get('sort_order','asc')

    if sort_by and hasattr(Delivery, sort_by):
        
        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Delivery, sort_by)))
        else:
            query = query.order_by(db.asc(getattr(Delivery, sort_by)))

        


    deliveries=query.all()
    output=[]
    for d in deliveries:
        delivery_data = {
            'id': d.id,
            'packageid': d.packageid,
            'client_name': d.client_name,
            'origin': d.origin,
            'destination': d.destination,
            'status': d.status,
            'expected_delivery_date': d.expected_delivery_date.strftime("%Y-%m-%d") if d.expected_delivery_date else None,
            'actual_delivery_date': d.actual_delivery_date.strftime("%Y-%m-%d") if d.actual_delivery_date else None,
            'on_time': d.on_time
        }
        output.append(delivery_data)

    return jsonify({'deliveries': output})

@app.route('/delivery/<id>',methods=['GET'])
@jwt_required()
def get_delivery_details_by_id(id):
    delivery=Delivery.query.get(id)
    if not delivery:
        return jsonify({'error':"ID not found"}),404
    
    delivery_data = {
        'id': delivery.id,
        'packageid': delivery.packageid,
        'client_name': delivery.client_name,
        'origin': delivery.origin,
        'destination': delivery.destination,
        'status': delivery.status,
        'expected_delivery_date': delivery.expected_delivery_date.strftime('%Y-%m-%d'),
        'actual_delivery_date': delivery.actual_delivery_date.strftime('%Y-%m-%d') if delivery.actual_delivery_date else None,
        'on_time': delivery.on_time
    }
    
    return jsonify(delivery_data)

@app.route('/delivery/<id>',methods=['PUT'])
@jwt_required()
def update_delivery_details(id):
    claims=get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Access denied. Admins only!'}), 403
    delivery=Delivery.query.get(id)
    if not delivery:
        return jsonify({'error':'ID not found'}),404

    data=request.get_json()
    
    if 'status' in data:
        delivery.status=data['status']
    if 'actual_delivery_date' in data:
        if data['actual_delivery_date']:
            delivery.actual_delivery_date = datetime.strptime(data['actual_delivery_date'], "%Y-%m-%d").date()
        else:
            delivery.actual_delivery_date = None

    if 'on_time' in data:
         delivery.on_time = data['on_time']

    db.session.commit()
    return jsonify({'message': 'Delivery updated successfully!'})

@app.route('/delivery/<id>',methods=['DELETE'])
@jwt_required()
def delete_delivery_details(id):
    claims=get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Access denied. Admins only!'}), 403
    delivery=Delivery.query.get(id)
    if not delivery:
        return jsonify({'error':'ID not found'}),404
    db.session.delete(delivery)
    db.session.commit()
    return jsonify({'message': 'Delivery deleted successfully!'})
