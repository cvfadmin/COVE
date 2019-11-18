from .models import Tag, Dataset
from sqlalchemy import or_


def dataset_tag_filter(request, query):
    print(query)
    topics = request.args.get('topics')
    tasks = request.args.get('tasks')
    data_types = request.args.get('data_types')

    name_list = []
    if topics is not None:
        name_list.extend(ensure_arg_is_list(topics))

    if tasks is not None:
        name_list.extend(ensure_arg_is_list(tasks))

    if data_types is not None:
        name_list.extend(ensure_arg_is_list(data_types))

    if len(name_list) < 1:
        return query

    # This filter assumes tag names are unique
    print(name_list)
    return query.filter(
        Dataset.tags.any(
            or_(
                Tag.name.in_(name_list),
            )
        )
    )


def ensure_arg_is_list(var):
    if isinstance(var, str):
        return [var]
