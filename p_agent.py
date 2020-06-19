from flask import Flask, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy import exc
import string, random


app= Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/evote'
db = SQLAlchemy(app)

class Polling_table(db.Model):
    Regid = db.Column(db.String(20),primary_key=True)
    #Name = db.Column(db.String(1000),nullable = False)
    Attendence = db.Column(db.Integer,nullable = True)
    AuthKey = db.Column(db.String(50),nullable=False)
    #AutenticationKey = db.Column(db.String(1000),nullable = False)
    #hasVoted = db.Column(db.Integer,nullable = False)


class Elect_record(db.Model):
    El_id = db.Column(db.Integer,primary_key=True)
    Participant = db.Column(db.String(50),nullable = False)
    Position = db.Column(db.String(50), nullable=False)
    Party = db.Column(db.String(50), nullable=False)
    Vote_count = db.Column(db.Integer,nullable = True)




@app.route('/pollingagent' , methods = ["POST","GET"])
def pollingagent():
    if request.method == "POST":
        regid = request.form.get("rid")
        present = request.form.get("attend")

        print(regid)


        entry = Polling_table(Regid=regid , Attendence=present , AuthKey="0000")
        #entry = db.query.filter_by(Regid='regid').update(dict(Attendence='1'))
        #db.session.update(entry.Attendence =present )

        try:
            db.session.add(entry)
            #db.session.flush()
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return render_template('already_present.html')

    return render_template('pollingagent.html')




@app.route('/pollingofficer' , methods = ["POST","GET"])
def pollingofficer():
    if request.method == "POST":
        regid = request.form.get("rid")


        print(regid)

        update_this = Polling_table.query.filter_by(Regid=regid).first()

        if(update_this != None):
            print(update_this.Attendence)

            varib = update_this.Attendence
            print(varib)

            if (varib == 1):
                uniq_key = key_generator(6)
                update_this.AuthKey = uniq_key
                db.session.commit()

                key2 = pollingofficerres(regid)
                # return redirect('/pollingofficerres')
                return render_template('pollingofficer.html', checked=varib, message=key2)

            if (varib == 0):
                return render_template('pollingofficer.html', message="Not Authenticated Voter")

        else:
            return render_template('pollingofficer.html', message="Not Authenticated Voter")

    else:
        return render_template('pollingofficer.html')


    return render_template('pollingofficer.html')


def key_generator(stringLength=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@app.route('/pollingofficerres' , methods = ["POST","GET"])
def pollingofficerres(regid):


    update_this = Polling_table.query.filter_by(Regid=regid).first()
    print(update_this.AuthKey)

    key = update_this.AuthKey+'  ----generated id'

    return key




@app.route('/login' , methods = ["POST","GET"])
def login():
    if request.method == "POST":
        regid = request.form.get("rid")
        auth = request.form.get("authkey")

        update_this = Polling_table.query.filter_by(Regid=regid).first()

        retreived_regid = update_this.Regid
        retreived_authkey = update_this.AuthKey




        if(regid == retreived_regid):
            if(auth == retreived_authkey):
                msg = getmsg()
                return redirect('/vote')


        else:
            return render_template('login.html', checked ="Please try again")



    else:
        return  render_template('login.html', message = "Please Vote")


def getmsg():
    return "Successfully logged in!"




@app.route('/vote' , methods = ["POST","GET"])
def vote():
    if request.method == "POST":
        pres_id = request.form.get("President")
        vpres_id = request.form.get("Vice_President")
        js_id = request.form.get("Joint_sec")
        gsc_id = request.form.get("GSCash")

        update1_this = Elect_record.query.filter_by(El_id=pres_id).first()

        print(update1_this.Vote_count)

        p_vote = update1_this.Vote_count

        update1_this.Vote_count = p_vote+1
        db.session.commit()
        print(update1_this.Vote_count)

        update2_this = Elect_record.query.filter_by(El_id=vpres_id).first()

        print(update2_this.Vote_count)

        p_vote = update2_this.Vote_count

        update2_this.Vote_count = p_vote + 1
        db.session.commit()
        print(update2_this.Vote_count)

        update3_this = Elect_record.query.filter_by(El_id=js_id).first()

        print(update3_this.Vote_count)

        p_vote = update3_this.Vote_count

        update3_this.Vote_count = p_vote + 1
        db.session.commit()
        print(update3_this.Vote_count)

        update4_this = Elect_record.query.filter_by(El_id=gsc_id).first()

        print(update4_this.Vote_count)

        p_vote = update4_this.Vote_count

        update4_this.Vote_count = p_vote + 1
        db.session.commit()
        print(update4_this.Vote_count)

    return  render_template('vote.html', message = "Thankyou for Voting")



app.run(debug = True)


