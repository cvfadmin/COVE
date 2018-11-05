from app import api
from .utils import SingleResourceByIdView, ListResourceView
from .models import Dataset, AddDatasetRequest, DeleteDatasetRequest

from .schemas import (
    dataset_schema,
    add_dataset_request_schema,
    delete_dataset_request_schema,
    add_dataset_request_list_schema,
    delete_dataset_request_list_schema,
    dataset_list_schema,
)


class SingleDatasetView(SingleResourceByIdView):
    Model = Dataset
    Schema = dataset_schema


class SingleAddDatasetRequestView(SingleResourceByIdView):
    Model = AddDatasetRequest
    Schema = add_dataset_request_schema


class SingleDeleteDatasetRequestView(SingleResourceByIdView):
    Model = DeleteDatasetRequest
    Schema = delete_dataset_request_schema


class ListDatasetView(ListResourceView):
    Model = Dataset
    Schema = dataset_list_schema


class ListAddDatasetRequestView(ListResourceView):
    Model = AddDatasetRequest
    Schema = add_dataset_request_list_schema


class ListDeleteDatasetRequestView(ListResourceView):
    Model = DeleteDatasetRequest
    Schema = delete_dataset_request_list_schema


api.add_resource(SingleDatasetView, '/datasets/<_id>')
api.add_resource(SingleAddDatasetRequestView, '/requests/add-dataset/<_id>')
api.add_resource(SingleDeleteDatasetRequestView, '/requests/delete-dataset/<_id>')

api.add_resource(ListDatasetView, '/datasets/')
api.add_resource(ListAddDatasetRequestView, '/requests/add-dataset')
api.add_resource(ListDeleteDatasetRequestView, '/requests/delete-dataset')