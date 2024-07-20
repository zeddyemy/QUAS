# QUAS (Quick API Setup) with Flask

## Description
A basic Quick API Setup using Flask, intended for rapid project initiation.

This project is intended to be a starting point for future projects. It includes a structured organization of routes, controllers, models, and utility functions to save development time.

## Prerequisites

- Python 3.12+
- Virtualenv (optional but recommended)
- PostgreSQL (or any other database you prefer)

## Setup
1. Clone the repository

2. **Create and activate a virtual environment**:
    ```sh
    cd project
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. **Set up environment variables**:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```plaintext
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=<your_database_url>
    ```
5. **Run the application**:
    ```sh
    flask run
    ```
---


## Implementing Tests

#### Install PyTest

Add PyTest to your `requirements.txt`:
```plaintext
pytest
pytest-flask
```

#### Test Directory Structure
```
tests/
├── test_models.py
├── test_routes.py
└── test_utils.py
```

#### Example Tests

1. test_models.py:
```python
import pytest
from app.models.user import AppUser

def test_user_creation():
    user = AppUser(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

```
2. test_routes.py:
```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Welcome" in rv.data
```

### Additional Steps
1. Configure Testing Environment:
    - Ensure your create_app function in __init__.py is configured to handle testing.

2. Run Tests:
    - Use pytest to run your tests:
    ```sh
    pytest
    ```

By adding these tests and documentation, you'll make your project more robust and easier to maintain, helping you save even more time in the long run.

---


## Contributing
Feel free to submit issues, fork the repository, and send pull requests!

## License
This project is licensed under the MIT License.