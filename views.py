from main import app
from models import VotesModel, CandidateModel, db, UserModel
from flask import redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user, logout_user
import string


# home page
@app.route("/")
def index():
    return render_template("home.html")


# profile page after login
@app.route("/profile")
@login_required
def profile():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    voter = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    return render_template("profile.html", name=current_user.name, prez=prez, vice=vice, voter=voter)


# form in profile page to cast vote
@app.route("/profile", methods=["POST"])
def post_vote():
    president = request.form.get('president')
    vicepresident = request.form.get('vice-president')

    voted = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    if not voted:
        voter = VotesModel(roll_num=current_user.roll_num, voter_id=current_user.id, post_1=int(president),
                           post_2=int(vicepresident))
        db.session.add(voter)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))


@app.route("/users")
def users():
    use = UserModel.query.all()
    return render_template("users.html", use=use)

# candidate page to know about candidate who are standing in election
@app.route("/candidate")
def candidate():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    return render_template("candidate.html", prez=prez, vice=vice)


# only for admin to register candidate in election
@app.route("/candidate_register")
@login_required
def candidate_register():
    if current_user.admin != 1:
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("candidate_register.html")


# candidate registration form
@app.route("/candidate_register", methods=["POST"])
def candidate_post():
    roll_num = request.form.get('roll_num')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    batch = request.form.get('batch')
    course = request.form.get('course')
    department = request.form.get('department')
    post = request.form.get('post')
    agenda = request.form.get('agenda')

    cand = CandidateModel.query.filter_by(roll_num=roll_num).first()

    error = False

    # if candidate is already register
    if cand:
        flash('Candidate has already been registered.', 'error')
        return redirect(url_for('candidate_register'))

    # first name can contain alphabets
    if not set(first_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.', 'error')
        error = True

    # last name can contain alphabets
    if not set(last_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.', 'error')
        error = True

    # first and last name cannot left blank
    if not first_name and not last_name:
        flash('Name cannot be left blank.', 'error')
        error = True

    if not batch and not course and not department:
        flash('Please fill in all the details. Batch, Course and Department information is neccessary.', 'error')
        error = True

    # if any error then redirect to candidate registration page
    if error:
        return redirect(url_for('candidate_register'))

    # if no error in registration the add candidate to CandidateModel
    else:
        candidate = CandidateModel(roll_num=roll_num, first_name=first_name, last_name=last_name, batch=batch,
                                   course=course, department=department, post=post, agenda=agenda)
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate successfully registered.', 'success')
        return redirect(url_for('candidate_register'))


# live result page
@app.route("/live_result")
def live_result():
    prez = db.session().execute(
        """select c.first_name,c.roll_num,count(v.post_1) as no_of_votes 
        from candidates c left join votes v 
        on c.roll_num = v.post_1 
        where c.post='President' 
        group by c.roll_num,c.first_name""")
    vice = db.session.execute(
        """select c.first_name,c.roll_num,count(v.post_2) as no_of_votes 
        from candidates c left join votes v 
        on c.roll_num = v.post_2 
        where c.post='Vice-President' 
        group by c.roll_num,c.first_name""")

    return render_template("live_result.html", candidate=prez, cand=vice)


# only for admin to update information of register candidate
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    candidates_update = CandidateModel.query.get(id)
    if request.method == 'POST':
        candidates_update.first_name = request.form['first_name']
        candidates_update.last_name = request.form['last_name']
        candidates_update.agenda = request.form['agenda']
        try:
            db.session.commit()
            return redirect('/candidate')
        except:
            return "There was a problem in updating"
    else:
        return render_template('update.html', candidates_update=candidates_update)


# only for admin to remove candidate from election
@app.route('/delete/<int:id>')
def delete(id):
    candidate_delete = CandidateModel.query.get(id)
    try:
        db.session.delete(candidate_delete)
        db.session.commit()
        return redirect('/candidate')
    except:
        return "There was a problem in deleting"

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user_delete = UserModel.query.get(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect('/users')
    except:
        return "There was a problem in deleting"
