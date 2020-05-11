import data_manager as dm
import data

from flask import Flask, session, redirect, url_for, flash, request, render_template

app = Flask(__name__)
app.secret_key = dm.random_api_key()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if dm.is_logged_in():
        return redirect('/') #de schimbat cu url pentru cont utilizator
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        if dm.check_login(username, typed_password):
            session['username'] = username
            session['logged_in'] = True
            return redirect('/')        #de schimbat cu url pentru cont utilizator
        else:
            flash('invalid Username or Password')
            return redirect('/login')
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('logged_in')
    return redirect(url_for('index'))


@app.route('/test', methods=["GET", "POST"])
def test():
    if 'username' not in session:
        return redirect('/login')
    test_data = data.questions
    number_of_questions = len(test_data)
    if request.method == 'GET':
        session['question_nr'] = 0
        session['correct_answers'] = 0
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == 'True':
            session['correct_answers'] += 1
        session['question_nr'] += 1
    if session['question_nr'] == len(test_data):
        return redirect("/result")
    question = list(test_data.keys())[session['question_nr']]
    return render_template("test.html", test_data=test_data, question=question, number_of_questions=number_of_questions)


@app.route("/result")
def result():
    if 'username' not in session:
        return redirect("/login")
    number_of_questions = len(data.questions)
    return render_template("result.html", number_of_questions=number_of_questions)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )


