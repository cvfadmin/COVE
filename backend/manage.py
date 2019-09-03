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

@manager.command
def prune_tokens():
    from app.auth.blacklist_helpers import prune_database
    prune_database()

# Might want to move the implemention code to another file
@manager.command
def prune_tags():
    '''Delete all tags that are not associated with any datasets'''
    from app.datasets.models import Tag

    # Get the ids of the tags that are being used
    r = db.engine.execute('select tag_id from tags')

    # store tag ids in a list
    tags_to_keep = []
    for tag_id in r:
        tags_to_keep.append(tag_id[0])

    tags_to_delete = Tag.query.filter(Tag.id.notin_(tags_to_keep))
    for tag in tags_to_delete:
        db.session.delete(tag)
    db.session.commit()

# 'python -m flask shell' for quick python shell testing
from app import db
from app.auth.models import User
from app.datasets.models import Dataset, Tag
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dataset': Dataset, 'Tag': Tag}


if __name__ == '__main__':
    manager.run()
