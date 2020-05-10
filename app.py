from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#Init database
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Company Class / Model
class Company(db.Model):
    __tablename__ = 'Companies'   
    
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(50), unique=True)
    permalink = db.Column(db.String(100))
    crunchbase_url = db.Column(db.String(150))
    homepage_url = db.Column(db.String(150))
    category_code = db.Column(db.String(50))
    number_of_employees = db.Column(db.Integer)
    founded_year = db.Column(db.Integer)
    founded_month = db.Column(db.Integer)
    founded_day = db.Column(db.Integer)
    deadpooled_year = db.Column(db.Integer) 
    deadpooled_month = db.Column(db.Integer)
    deadpooled_day = db.Column(db.Integer)
    tag_list = db.Column(db.String(300))
    email_address =db.Column(db.String(100))
    overview = db.Column(db.String(3000))
    total_money_raised = db.Column(db.String(50))

    def __init__(self, id, name, permalink, crunchbase_url, homepage_url, category_code, number_of_employees, founded_year, founded_month, founded_day, deadpooled_year, deadpooled_month, deadpooled_day, tag_list, email_address, overview, total_money_raised):
        self.id = id
        self.name = name
        self.permalink = permalink
        self.crunchbase_url = crunchbase_url
        self.homepage_url = homepage_url
        self.category_code = category_code
        self.number_of_employees = number_of_employees
        self.founded_year = founded_year
        self.founded_month = founded_month
        self.founded_day = founded_day
        self.deadpooled_year = deadpooled_year
        self.deadpooled_month = deadpooled_month
        self.deadpooled_day = deadpooled_day
        self.tag_list = tag_list
        self.email_address = email_address
        self.overview = overview
        self.total_money_raised = total_money_raised

# Company Scheme
class CompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'permalink', 'crunchbase_url', 'homepage_url', 'category_code', 'number_of_employees', 'founded_year', 'founded_month', 'founded_day', 'deadpooled_year', 'deadpooled_month', 'deadpooled_day', 'tag_list', 'email_address', 'overview', 'total_money_raised')


# Init schema
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

#Creating a company
@app.route('/company', methods=['POST'])
def add_company():
    
    id = request.json['_id']["$oid"]
    name = request.json['name']
    permalink = request.json.get('permalink')
    crunchbase_url = request.json.get('crunchbase_url')
    homepage_url = request.json.get('homepage_url')
    category_code = request.json.get('category_code')
    number_of_employees = request.json.get('number_of_employees')
    founded_year = request.json.get('founded_year')
    founded_month = request.json.get('founded_month')
    founded_day = request.json.get('founded_day')
    deadpooled_year = request.json.get('deadpooled_year') 
    deadpooled_month = request.json.get('deadpooled_month') 
    deadpooled_day = request.json.get('deadpooled_day')
    tag_list = request.json.get('tag_list')
    email_address = request.json.get('email_address')
    overview = request.json.get('overview')
    total_money_raised = request.json.get('total_money_raised')

    new_company = Company(id, name, permalink, crunchbase_url, homepage_url, category_code,number_of_employees, founded_year, founded_month, founded_day, deadpooled_year, deadpooled_month, deadpooled_day, tag_list, email_address, overview, total_money_raised)

    db.session.add(new_company)
    db.session.commit()

    return company_schema.jsonify(new_company)

# Get All Companies
@app.route('/company', methods=['GET'])
def get_companies():
    all_companies = Company.query.all()
    result = companies_schema.dump(all_companies)
    return jsonify(result)

# Get Single Company based on company ID
@app.route('/company/<id>', methods=['GET'])
def get_company(id):
    company = Company.query.get(id)
    return company_schema.jsonify(company)

#Update a Company and its relationships
@app.route('/company/<id>', methods=['PUT'])
def update_company(id): 

    company = Company.query.get(id)
    name = request.json['name'] 
    permalink = request.json['permalink']
    crunchbase_url = request.json['crunchbase_url']
    homepage_url = request.json['homepage_url']
    category_code = request.json['category_code'] 
    number_of_employees = request.json['number_of_employees']
    founded_year = request.json['founded_year']
    founded_month = request.json['founded_month']
    founded_day = request.json['founded_day']
    deadpooled_year = request.json['deadpooled_year']
    deadpooled_month = request.json['deadpooled_month']
    deadpooled_day = request.json['deadpooled_day']
    tag_list = request.json['tag_list']
    email_address = request.json['email_address']
    overview = request.json['overview']
    total_money_raised = request.json['total_money_raised']


    company.name = name
    company.permalink = permalink
    company.crunchbase_url = crunchbase_url
    company.homepage_url = homepage_url
    company.category_code = category_code
    company.number_of_employees = number_of_employees
    company.founded_year = founded_year
    company.founded_month = founded_month
    company.founded_day = founded_day
    company.deadpooled_year = deadpooled_year
    company.deadpooled_month = deadpooled_month
    company.deadpooled_day = deadpooled_day
    company.tag_list = tag_list
    company.email_address = email_address
    company.overview = overview
    company.total_money_raised = total_money_raised
    
    db.session.commit()

    return company_schema.jsonify(company)

# Delete Company
@app.route('/company/<id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get(id)
    db.session.delete(company)
    db.session.commit()

    return company_schema.jsonify(company)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)