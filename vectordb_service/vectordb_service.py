import weaviate
import logging
from weaviate.classes.query import MetadataQuery

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class VectorDBService:
    def __init__(self):
        self.client = weaviate.connect_to_local()
        logging.info(f"vectordb client readiness: {self.client.is_ready()}")

    def create_collection(self, collection, properties):
        self.client.collections.create(collection, properties)

    def insert_data(self, name, data):
        collection = self.client.collections.get(name)
        uuid = collection.data.insert(data)
        logging.info(f"inserted data into {name} with uuid: {uuid}")
        return uuid

    def search(self, name, query, limit):
        logging.info(f"collection:{name}, query:{query}, limit:{limit}")
        objects = self.client.collections.get(name).query.near_text(
            query=query,
            limit=limit,
            return_metadata=MetadataQuery(distance=True)
        )
        return objects

    def close(self):
        self.client.close()
