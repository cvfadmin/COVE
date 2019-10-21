# COVE Backend

*Please Note:* Without configuring `MAIL_USERNAME` and `MAIL_PASSWORD` properly in your own `.env` (to be accessed through `config.py`) a lot of core functionality will fail.

## Using
**Installation:** `pip install -r requirements.txt`

**Update database:**

1. `alembic revision --autogenerate -m "describe_your_model_changes_here"`

2. `alembic upgrade head`


**To run:** `python manage.py run`


## Other useful commands:

**To reindex datasets for search:** `python manage.py reindex`

**To prune tokens:** `python manage.py prune_tokens`

**To prune tags:** `python manage.py prune_tags`

**To run unit tests:** `python tests.py`


## Some Documentation:
https://documenter.getpostman.com/view/5085455/RzZ6JgVf
