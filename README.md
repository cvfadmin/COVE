## COVE Backend update branch

**What this branch is working on:**

* Keeping codebase within project scope (Users add database information and admins approve submission requests)
* Update to Python 3.6
* Focus on RESTful principles
* Modular code

**To run:** `python manage.py run`

**To update database: **
 1. `alembic revision --autogenerate -m "describe_your_model_changes_here"`
 2. `alembic upgrade head`

**Some documentation: ** https://documenter.getpostman.com/view/5085455/RzZ6JgVf
