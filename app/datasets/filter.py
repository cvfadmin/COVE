from .models import Tag, Dataset
from sqlalchemy import and_


def dataset_tag_filter(request, query):
    topics = request.args.get('topics')
    tasks = request.args.get('tasks')
    data_types = request.args.get('data_types')

    if topics is not None:
        query = tag_query_filter(query, 'topics', topics)

    if tasks is not None:
        query = tag_query_filter(query, 'tasks', tasks)

    if data_types is not None:
        query = tag_query_filter(query, 'data_types', data_types)

    return query


def tag_query_filter(query, category, name_list):
    # Tag name is in list and categories match
    name_list = ensure_arg_is_list(name_list)

    return query.filter(
        Dataset.tags.any(
            and_(
                Tag.name.in_(name_list),
                Tag.category == category
            )
        )
    )


def ensure_arg_is_list(var):
    if isinstance(var, str):
        return [var]
