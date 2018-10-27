from flask_script import Manager
from app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    pass


if __name__ == '__main__':
    manager.run()

