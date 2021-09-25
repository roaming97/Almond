# Almond
Flask video database for archival purposes.

---

## Usage
Install the required dependencies.
```bash
$ pip install -r requirements.txt
```
Create an environment variables (`.env`) file
```python
PORT=5000
SECRET='secret_key'
PRIVATE_PASS='almond_private_pass'
DATABASE_URI='sqlite:///database.db'
```

Adding the ``PRIVATE_PASS`` variable is required if your app is going to be private.

You can check whether your app is private or not in ``settings.py``.