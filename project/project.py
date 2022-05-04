from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from email_send import send_email
import datetime as dt
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

days_counter = 0
res = []
name = ''
room = ''
in_date = ''
out_date = ''
people = ''
room_cost = {'burgua': 2400, 'camelot': 2400, 'origami': 2400, 'mexicana': 2400, 'sakura': 2400,
             'retro': 2100, '1001night': 2100, 'nefertiti': 2100, 'sparta': 2100, 'dali': 2100}


class Burgua(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<burgua {self.id}>"


class Camelot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<camelot {self.id}>"


class Nefertiti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<nefertiti {self.id}>"


class Night(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<night1001 {self.id}>"


class Sakura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<sakura {self.id}>"


class Mexicana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<mexicana {self.id}>"


class Retro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<retro {self.id}>"


class Sparta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<sparta {self.id}>"


class Origami(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<origami {self.id}>"


class Dali(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<dali {self.id}>"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String, nullable=False)
    date1 = db.Column(db.String, nullable=False)
    date2 = db.Column(db.String, nullable=False)
    people_amount = db.Column(db.Integer, nullable=False)
    surname = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    in_time = db.Column(db.String)
    out_time = db.Column(db.String)
    comments = db.Column(db.Text)

    def __repr__(self):
        return f"<profile {self.id}>"

# from project.project import db
# db.create_all()


def add_date():
    if name == 'burgua':
        for i in res:
            d = Burgua(date=i)
            db.session.add(d)
    elif name == 'camelot':
        for i in res:
            d = Camelot(date=i)
            db.session.add(d)
    elif name == 'origami':
        for i in res:
            d = Origami(date=i)
            db.session.add(d)
    elif name == 'mexicana':
        for i in res:
            d = Mexicana(date=i)
            db.session.add(d)
    elif name == 'sakura':
        for i in res:
            d = Sakura(date=i)
            db.session.add(d)
    elif name == 'retro':
        for i in res:
            d = Retro(date=i)
            db.session.add(d)
    elif name == '1001night':
        for i in res:
            d = Night(date=i)
            db.session.add(d)
    elif name == 'nefertiti':
        for i in res:
            d = Nefertiti(date=i)
            db.session.add(d)
    elif name == 'sparta':
        for i in res:
            d = Sparta(date=i)
            db.session.add(d)
    else:
        for i in res:
            d = Dali(date=i)
            db.session.add(d)
    db.session.commit()


def list_date():
    y1 = in_date.split('.')
    y2 = out_date.split('.')
    start_date = dt.date(int(y1[2]), int(y1[1]), int(y1[0]))
    end_date = dt.date(int(y2[2]), int(y2[1]), int(y2[0]))
    today = dt.date.today()
    if start_date > end_date:
        return 'Дата заезда должна быть раньше даты выезда!'
    elif start_date < today:
        return 'Дата заезда должна быть не раньше сегодняшней даты!'
    return pd.date_range(start_date, end_date).strftime('%d.%m.%Y').tolist()


@app.route('/')
@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/book', methods=['POST', 'GET'])
def book():
    day = days_counter
    cost = day * room_cost[name]
    if people == '2':
        cost += (300 * day)
    elif people == '3':
        if name == 'origami':
            cost += (1200 * day)
        else:
            cost += (1000 * day)
    if request.method == 'GET':
        return render_template('form.html', room=room, in_date=in_date,
                               out_date=out_date, people=people,
                               cost=str(cost)+"₽")
    else:
        try:
            d = Profile(room=room, date1=in_date, date2=out_date, people_amount=int(people),
                        surname=request.form['surname'], name=request.form['name'],
                        father_name=request.form['father'], email=request.form['email'],
                        phone=request.form['phone'], in_time=request.form['time-in'],
                        out_time=request.form['time-out'], comments=request.form['comment'])
            db.session.add(d)
            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Пожалуйста, заполните все поля!')
            return render_template('form.html', room=room, in_date=in_date,
                                   out_date=out_date, people=people,
                                   cost=str(cost)+"₽")
        add_date()
        if 'gmail' in request.form['email']:
            template = 'email_template.html'
        else:
            template = 'email_template2.html'
        if not request.form['comment']:
            comment = '-'
        else:
            comment = request.form['comment']
        if not request.form['father']:
            father = '-'
        else:
            father = request.form['father']

        if len(request.form['time-out']) > 6:
            tmp = int((''.join(request.form['time-out'].split(' - ')[1])).split()[0][:-1])
            total_cost = tmp + cost
        else:
            total_cost = cost
        msg = render_template(template, surname=request.form['surname'],
                              name=request.form['name'], father_name=father,
                              room=room, in_date=in_date, out_date=out_date, people=people,
                              cost=cost, phone=request.form['phone'], time_in=request.form['time-in'],
                              time_out=request.form['time-out'], comments=comment, total=total_cost)
        send_email(msg, request.form['email'])
        return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('last.html')


@app.route('/1001-night', methods=['POST', 'GET'])
def night():
    global room, name
    room = '1001 ночь'
    name = '1001night'
    if request.method == 'GET':
        return render_template('room.html', name='1001night', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='1001night', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Night(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='1001night', room=room, ext='jpeg')

        else:
            flash(res)
            return render_template('room.html', name='1001night', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/burgua', methods=['POST', 'GET'])
def burgua():
    global room, name
    room = 'Буржуа'
    name = 'burgua'
    if request.method == 'GET':
        return render_template('room.html', name='burgua', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='burgua', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Burgua(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='burgua', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='burgua', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/camelot', methods=['POST', 'GET'])
def camelot():
    global room, name
    room = 'Камелот'
    name = 'camelot'
    if request.method == 'GET':
        return render_template('room.html', name='camelot', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='camelot', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Camelot(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='camelot', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='camelot', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/dali', methods=['POST', 'GET'])
def dali():
    global room, name
    room = 'Дали'
    name = 'dali'
    if request.method == 'GET':
        return render_template('room.html', name='dali', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='dali', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Dali(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='dali', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='dali', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/mexicana', methods=['POST', 'GET'])
def mexicana():
    global room, name
    room = 'Мексикана'
    name = 'mexicana'
    if request.method == 'GET':
        return render_template('room.html', name='mexicana', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='mexicana', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Mexicana(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='mexicana', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='mexicana', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/nefertiti', methods=['POST', 'GET'])
def nefertiti():
    global room, name
    room = 'Нефертити'
    name = 'nefertiti'
    if request.method == 'GET':
        return render_template('room.html', name='nefertiti', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='nefertiti', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Nefertiti(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='nefertiti', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='nefertiti', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/origami', methods=['POST', 'GET'])
def origami():
    global room, name
    room = 'Оригами'
    name = 'origami'
    if request.method == 'GET':
        return render_template('room.html', name='origami', room=room, ext='jpeg')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='origami', room=room, ext='jpeg')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Origami(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='origami', room=room, ext='jpeg')
        else:
            flash(res)
            return render_template('room.html', name='origami', room=room, ext='jpeg')

        return redirect(url_for('book'))


@app.route('/retro', methods=['POST', 'GET'])
def retro():
    global room, name
    room = 'Ретро'
    name = 'retro'
    if request.method == 'GET':
        return render_template('room.html', name='retro', room=room, ext='png')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='retro', room=room, ext='png')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Retro(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='retro', room=room, ext='png')
        else:
            flash(res)
            return render_template('room.html', name='retro', room=room, ext='png')

        return redirect(url_for('book'))


@app.route('/sakura', methods=['POST', 'GET'])
def sakura():
    global room, name
    room = 'Сакура'
    name = 'sakura'
    if request.method == 'GET':
        return render_template('room.html', name='sakura', room=room, ext='png')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='sakura', room=room, ext='png')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Sakura(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='sakura', room=room, ext='png')
        else:
            flash(res)
            return render_template('room.html', name='sakura', room=room, ext='png')

        return redirect(url_for('book'))


@app.route('/sparta', methods=['POST', 'GET'])
def sparta():
    global room, name
    room = 'Спарта'
    name = 'sparta'
    if request.method == 'GET':
        return render_template('room.html', name='sparta', room=room, ext='png')
    elif request.method == 'POST':
        if request.form['in'] == request.form['out']:
            flash('Минимальное время проживания - 1 сутки')
            return render_template('room.html', name='sparta', room=room, ext='png')

        global in_date, out_date, people, res
        in_date = '.'.join(reversed(request.form['in'].split('-')))
        out_date = '.'.join(reversed(request.form['out'].split('-')))
        people = request.form['people']
        res = list_date()
        if type(res) == list:
            try:
                global days_counter
                days_counter = len(res) - 1
                for i in res:
                    d = Sparta(date=i)
                    db.session.add(d)
                    db.session.flush()
            except Exception:
                flash('К сожалению, в эти даты номер уже занят')
                return render_template('room.html', name='sparta', room=room, ext='png')
        else:
            flash(res)
            return render_template('room.html', name='sparta', room=room, ext='png')

        return redirect(url_for('book'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=False)
