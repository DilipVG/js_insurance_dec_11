from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:SaiPrasanth@localhost:5432/js'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key in a real application
db = SQLAlchemy(app)
migrate = Migrate(app , db)
# db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

admin = Admin(app)

#DATABASE MODELS

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    full_name = db.Column(db.Text, nullable = False)
    mobile = db.Column(db.Text, nullable = False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=True, unique=True)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), default=None)
    address = db.Column(db.Text, default = None)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<users {self.full_name}>'


class Policy(db.Model):
    policy_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    category = db.Column(db.String(255), nullable=False)
    policy_type = db.Column(db.String(255), nullable= False)
    insurance_company = db.Column(db.String(255), nullable=False)
    policy_name = db.Column(db.String(255), nullable = False)
    policy_no = db.Column(db.String(255), nullable= False)
    due_date = db.Column(db.Date, nullable=False)
    emi_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self):
        return f'<Policy {self.policy_no}>'


class MotorInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    motor_type = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<MotorInsurance {self.name}>'


class HealthInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<HealthInsurance {self.name}>'
    

class TravelInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    travelling_to = db.Column(db.Text, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    days_count = db.Column(db.Integer, nullable=False)
    passenger_count = db.Column(db.Integer, nullable=False)

    def __rep__(self):
        return f'<TravelInsurance {self.name}>'


class WorkmenInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable = False)
    company_name = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f'<WorkmenInsurance {self.name}>'


class PropertyInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    city = db.Column(db.Text, nullable = False)
    
    def __repr__(self):
        return f'<PropertyInsurance {self.name}>'


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    insurance_type = db.Column(db.Text)
    company_name = db.Column(db.Text)
    policy_np = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Claim {self.policy_no}>'


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_name = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer)
    mobile = db.Column(db.Text, nullable=False)
    updates = db.Column(db.Boolean, default = False, nullable=False)
    email = db.Column(db.Text)
    appointment = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Appointment {self.customer_name}>'


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


class AdminModelView(ModelView):
    column_exclude_list = ['password']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(AdminModelView(users, db.session, name= 'My Customers'))
admin.add_view(AdminModelView(Policy, db.session, name= 'Policies'))

admin.add_view(AdminModelView(Appointments, db.session, name='My Appointments'))
admin.add_view(AdminModelView(Claim, db.session, name='Claims'))

admin.add_view(AdminModelView(HealthInsurance, db.session, category="Interests"))
admin.add_view(AdminModelView(MotorInsurance, db.session, category="Interests"))
admin.add_view(AdminModelView(TravelInsurance, db.session, category="Interests"))
admin.add_view(AdminModelView(WorkmenInsurance, db.session, category="Interests"))
admin.add_view(AdminModelView(PropertyInsurance, db.session, category="Interests"))

# ROUTING CODE FOR VIEWS


@app.route("/")
def hello():
    if request.method == 'POST':
        customer_name = request.form['username']
        dob = request.form['dob']
        age = request.form['age']
        mobile = request.form['mobile']
        updates = request.form.get('updates') == "True"
        email = request.form['email']
        appointment = request.form['appointment_date']
        try:

            new_appointment = Appointments(
                customer_name = customer_name,
                dob = dob,
                age = age,
                mobile = mobile,
                updates = updates,
                email = email,
                appointment = appointment)
            db.session.add(new_appointment)
            db.session.commit()

            flash('User details are saved successfully', 'success')
        except Exception as e:
            flash('User Details are not saved', 'error')
        return redirect(url_for('home'))
    return render_template('home.html')


# Saving Appointment Requests
@app.route('/appointments', methods=['GET', 'POST'])
def appointments(): 
    if request.method == 'POST':
        customer_name = request.form['username']
        dob = request.form['dob']
        age = request.form['age']
        mobile = request.form['mobile']
        updates = request.form.get('updates') == "True"
        email = request.form['email']
        appointment = request.form['appointment_date']

        new_appointment = Appointments(
            customer_name = customer_name,
            dob = dob,
            age = age,
            mobile = mobile,
            updates = updates,
            email = email,
            appointment = appointment)
        db.session.add(new_appointment)
        db.session.commit()
    
    all_appointments = Appointments.query.all()
    return render_template('appointments.html', appointments = all_appointments)



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    print("request type method:", request.method)
    if request.method == 'POST':
        print("request type method:", request.method)
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        email = request.form['email']
        dob = request.form['dob']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = users(full_name=username ,mobile = mobile, password=hashed_password, dob = dob, email = email)

        db.session.add(new_user)
        db.session.commit()

        # flash("Sign up Successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']

        user = users.query.filter_by(mobile=mobile).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            # flash("Login Successful!", 'success')
            return redirect(url_for('dashboard'))
        else:
            # flash('Login failed. Please check your username and password.', 'error')
            return "Login failed"

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_policies = Policy.query.filter_by(user_id = current_user.id).all()
    return render_template('dashboard.html', user_policies = user_policies)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('Logout successful!', 'success')
    return redirect(url_for('hello'))

# Saving Policy Claim Requests
@app.route('/claims', methods=['GET','POST'])
def claims():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        mobile = request.form['mobile']
        insurance_type = request.form['insurance_type']
        company_name = request.form['company_name']
        policy_no = request.form['policy_no']

        new_claim = Claim(customer_name = customer_name, mobile = mobile, insurance_type = insurance_type, company_name = company_name, policy_np = policy_no)

        db.session.add(new_claim)
        db.session.commit()

        return "<h2> Claims Saved! </h2>"

    return render_template('claims.html')





@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin.html', user=current_user)

def create_tables():
    with app.app_context():
        db.create_all()

#User Profile or Dashboard Page
@app.route('/profile/<int:id>/', methods=['GET','POST'])
@login_required
def profile(id):
    new_user = users.query.get(id = id).first()
    return render_template('dashboard.html', user_id = new_user)


if __name__ == "__main__":
    # db.create_all()
    create_tables()
    app.run(debug=True)