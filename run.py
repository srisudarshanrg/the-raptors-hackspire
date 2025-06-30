from raptor_hackspire import app, db
from raptor_hackspire import models

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=4000)