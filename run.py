from os import getenv
from dotenv import load_dotenv
load_dotenv()
from app import app

if __name__ == "__main__":
    app.run(debug=True, port=getenv('PORT') or 5000)
