import weaviate
from dotenv import load_dotenv
from sample_data import reports
from weaviate.classes.config import Property, DataType


if __name__ == '__main__':
    load_dotenv()

    client = weaviate.connect_to_local()

    print(client.is_ready())

    client.collections.create(
        "Articles",
        properties=[  # properties configuration is optional
            Property(name="name", data_type=DataType.TEXT),
            Property(name="summary", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
            Property(name="year", data_type=DataType.INT),
        ]
    )

    articles = client.collections.get("Articles")
    articles.data.insert_many(reports)

    client.close()
