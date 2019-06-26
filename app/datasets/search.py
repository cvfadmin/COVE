from flask import current_app
from app import db


def create_index(model):
    '''Creates an index for a model.'''
    if not current_app.elasticsearch:
        return
    if hasattr(model, '__doc__'):
        current_app.elasticsearch.indices.create(index=model.__tablename__, body=model.__doc__)
    else:
        current_app.elasticsearch.indices.create(index=model.__tablename__)


def add_to_index(index, model):
    '''Index every field in model.__searchable__.'''
    if not current_app.elasticsearch:
        return
    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(model)
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    '''Deletes a model from an index.'''
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def remove_index(index):
    '''Removes an index if it exists.'''
    if not current_app.elasticsearch:
        return
    if current_app.elasticsearch.indices.exists(index=index):
        current_app.elasticsearch.indices.delete(index)


# Note: The search query's body is currently specific to the Database model.
# If you want to use this method for other models, the body must be modified.
def query_index(index, query):
    '''
    Searches through <index> for a text matching <query>.

    Args:
        index (str): The index name to be searched.
        query (str): The expression being searched for.

    Returns:
        List of ints: Each int corresponds to an ID of a model that satisfies the query.
        int:          The total number of models that satisfy the query
    '''

    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body=
        {
            'query': {
                'multi_match': {
                    'query':                query,
                    'type':                 'most_fields',
                    'fields':               ['name^10', '*']
                    # 'operator':             'and'
            }}
        },
        search_type='dfs_query_then_fetch' # remove to increase search speed, but decrease accuracy
                                           # can be removed once database has enough data
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


class SearchableMixin(object):
    '''
    The base class for all searchable models.

    A model inheriting from SearchableMixin does the following:
      1) Defines __searchable__ as a list of all fields desired to be indexed.
      2) Optionally defines __doc__, which will be used for creating the index for the model.
      2) Automatically indexes any new model instances when it is commited to the db.
      3) Can call Model.reindex() to reindex model instances. This needs to be done if there
          are model instances in the db that have not indexed.
    '''

    @classmethod
    def search(cls, expression):
        ids, total = query_index(cls.__tablename__, expression)
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

    # For some reason, after db.session.query(Model).update(...), the changes are not saved
    # in session.dirty in the before_commit() function.
    # So we'll just update our indicies in the 'after_bulk_update()' event.
    @classmethod
    def after_bulk_update(cls, session, query, query_context, result):
        '''Update all indices modifies by db.session.query(Model).update(...).'''
        for obj in query.all():
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls):
        '''Deletes and recreates an index and re-adds all its docs. '''
        remove_index(cls.__tablename__)
        create_index(cls)
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# Automatically updates ElasticSearch indexes after every database commit
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

# Automatically updates indices when a dataset is edited / updated.
db.event.listen(db.session, 'after_bulk_update', SearchableMixin.after_bulk_update)
