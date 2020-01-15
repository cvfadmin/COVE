from .models import Tag, Dataset


def dataset_tag_filter(request, query):
    topics = request.args.get('topics')
    tasks = request.args.get('tasks')
    data_types = request.args.get('data_types')

    name_list = []
    if topics is not None:
        name_list.extend(ensure_arg_is_list(topics.split(",")))

    if tasks is not None:
        name_list.extend(ensure_arg_is_list(tasks.split(",")))

    if data_types is not None:
        name_list.extend(ensure_arg_is_list(data_types.split(",")))

    if len(name_list) < 1:
        return query

    # This filter assumes tag names are unique across categories
    return query.filter(Dataset.tags.any(Tag.name.in_(name_list)))


def ensure_arg_is_list(var):
    if isinstance(var, str):
        return [var]
    return var
