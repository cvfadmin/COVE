from flask import current_app
from app import db


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def remove_index(index):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.indices.delete(index)


# Returns two things: a list of numeric IDS found with pagination filtering,
#                     the total number of results from query without pagination
def query_index(index, query, offset, limit):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body=
        {
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['*', 'name^2']
                }
            },
            'from': offset,
            'size': limit
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


# The base class for all searchable models.
# A model inheriting from SearchableMixin does the following:
#   1) Defines __searchable__ as a list of all fields the user wants indexed.
#   2) Automatically indexes any new model instances when it is commited to the db.
#   3) Can call Model.reindex() to reindex model instances. This needs to be done if there
#       are model instances in the db that have not indexed.
class SearchableMixin(object):
    @classmethod
    def search(cls, expression, offset, limit):
        ids, total = query_index(cls.__tablename__, expression, offset, limit)
        if len(ids) == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        remove_index(cls.__tablename__)
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# Automatically updates ElasticSearch indexes after every database commit
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
