
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


#configure postgreSQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Create SQLALchemy database

db = SQLAlchemy(app)


@app.route("/")
def home():
    return {"message": "Tuition Centre API is running"}



@app.route("/db-test")
def db_test():
    try:
        db.session.execute(db.text("Select 1"))

        return {
            "message": "Database connection successful"
        }

    except Exception as error: 

        return{
            "message": "Database connection failed",
            "error": str(error)
        }, 500