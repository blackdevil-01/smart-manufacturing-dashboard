from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_units = db.Column(db.Integer)
    defective_units = db.Column(db.Integer)
    quality_rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/")
def dashboard():
    total_units = random.randint(900, 1100)
    defective_units = random.randint(0, 60)
    quality_rate = round(((total_units - defective_units) / total_units) * 100, 2)
    shift = random.choice(["Morning", "Evening", "Night"])

    record = Production(
    total_units=total_units,
    defective_units=defective_units,
    quality_rate=quality_rate,
    shift=shift
)

    db.session.add(record)
    db.session.commit()
    shift = db.Column(db.String(20))

    alert = "Normal"
    if quality_rate < 95:
        alert = "Quality Warning"

    logs = Production.query.order_by(Production.timestamp.desc()).limit(10).all()

    return render_template("index.html",
                           total=total_units,
                           defective=defective_units,
                           quality=quality_rate,
                           alert=alert,
                           logs=logs
                           defect_rate=defect_rate)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
if quality_rate >= 97:
    alert = "Optimal"
elif quality_rate >= 95:
    alert = "Stable"
elif quality_rate >= 90:
    alert = "Warning"
else:
    alert = "Critical"    
defect_rate = round((defective_units / total_units) * 100, 2)   