# Almond
Flask video database for archival purposes.

---

## Usage
Install the required dependencies.
```bash
$ pip install -r requirements.txt
```
Create an environment variables (`.env`) file.
```python
PORT=5000
SECRET='246795da7515a315db4988f48477cf4c'
PRIVATE_PASS='private_almond_password'
DATABASE_URI='sqlite:///database.db'
```

Adding the ``PRIVATE_PASS`` variable is required if your app is going to be private.
You can check whether your app is private or not in ``settings.py``.

Finally, run the app with `run.py`.