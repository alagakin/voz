from typing import List, Dict

from config import MEILI_MASTER_KEY, MEILISEARCH_URL
from meilisearch import Client
from meilisearch.errors import MeilisearchApiError
from meilisearch.index import Index


def get_client() -> Client:
    return Client(MEILISEARCH_URL,
                  MEILI_MASTER_KEY)


def get_index(index_name: str, client: Client) -> Index or False:
    try:
        return client.get_index(index_name)
    except MeilisearchApiError:
        return False


def create_index(index_name: str, client: Client):
    task = client.create_index(index_name)
    task = client.wait_for_task(task.task_uid)

    if task.status == "succeeded" or task.status == "failed":
        return get_index(index_name, client)


def delete_index(index_name: str, client: Client):
    task = client.delete_index(index_name)
    return client.wait_for_task(task.task_uid)


def fill_index(index_name: str, documents: List[Dict]):
    client = get_client()
    delete_index(index_name, client)
    index = create_index(index_name, client)
    task = index.add_documents(documents)
    result = client.wait_for_task(task.task_uid)
    if result.status == 'succeeded':
        return True
    else:
        return False
