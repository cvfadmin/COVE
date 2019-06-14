from flask_script import Manager
from app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run()

@manager.command
def reindex():
    from app.datasets.models import Dataset
    Dataset.reindex()

@manager.command
def test():
    pass


# 'python -m flask shell' for quick python shell testing
from app import db
from app.auth.models import User
from app.datasets.models import Dataset, Tag
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dataset': Dataset, 'Tag': Tag}


if __name__ == '__main__':
    manager.run()
