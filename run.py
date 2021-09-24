from dotenv import load_dotenv
load_dotenv()
from app import app
from os import getenv

if __name__ == "__main__":
    app.run(debug=True, port=getenv('PORT'))
