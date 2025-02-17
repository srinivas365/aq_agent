import logging

import weaviate
from dotenv import load_dotenv
from sample_data import reports
from weaviate.classes.config import Property, DataType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    load_dotenv()
    client = weaviate.connect_to_local()
    logging.info(f"Client connected to vectordb: {client.is_ready()}")

    try:
        if not client.collections.exists("Articles"):
            client.collections.create(
                "Articles",
                properties=[  # properties configuration is optional
                    Property(name="name", data_type=DataType.TEXT),
                    Property(name="summary", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="year", data_type=DataType.INT),
                ]
            )
            logging.info("Created Articles collection in vectordb")
        logging.info("inserting records into Articles collection")
        articles = client.collections.get("Articles")
        articles.data.insert_many(reports)
        logging.info("records have been loaded successfully")
    except Exception as e:
        print(str(e))
    finally:
        client.close()
