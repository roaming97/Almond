# Almond
Video database app made with Python using Flask.

---

## Installing

For this application you require [Python 3.8](https://www.python.org/downloads/) or higher and [ffmpeg](https://ffmpeg.org/download.html) installed on your computer.

Install the required dependencies.
```bash
$ pip install -r requirements.txt
```
Create an environment variables (`.env`) file.
```python
PORT=5000
SECRET='246795da7515a315db4988f48477cf4c'
PRIVATE_PASS='almond123'
DATABASE_URI='sqlite:///database.db'
```

Adding the ``PRIVATE_PASS`` variable is required if your app is going to be private.
You can check whether your app is private or not in ``settings.py``.

Finally, run the app with `run.py`.

---

## Using

This app mainly functions as an app to archive YouTube videos on a database of your own in case they disappear from the site.

Clicking the *Quick add* button and inserting a YouTube URL should be enough.

---

## Contributing

If you encounter any errors or bugs, open an issue.
Pull requests are welcome.