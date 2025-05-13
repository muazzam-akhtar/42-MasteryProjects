import pandas as pd
import sqlalchemy
from tqdm import tqdm
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine


def table_exists(engine: Engine, tableName: str) -> bool:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if tableName in metadata.tables:
        print(f"Table {tableName} already exist")
    return tableName in metadata.tables


def load(path: str, tableName: str) -> None:
    try:
        engine = create_engine("postgresql://makhtar:mysecretpassword@postgres"
                               + ":5432/piscineds")
        if not table_exists(engine, tableName):
            print(f"\033[1;33mTable {tableName} doesn't exist, creating..."
                  + "\033[;39m]")
            chunkSize = 10000
            data_types = {
                "event_time": sqlalchemy.DateTime(),
                "event_type": sqlalchemy.types.String(length=255),
                "product_id": sqlalchemy.types.Integer(),
                "price": sqlalchemy.Float(),
                "user_id": sqlalchemy.types.BigInteger(),
                "user_session": sqlalchemy.types.UUID(as_uuid=True)
                }
            data = pd.read_csv(path)
            totalRows = len(data)
            chunkSize = totalRows // 100
            chunkCount = totalRows // chunkSize
            remainder = totalRows % chunkSize
            with tqdm(total=totalRows, position=0, leave=True) as pbar:
                for i in range(chunkCount):
                    chunk = data.iloc[i * chunkSize:(i + 1) * chunkSize]
                    chunk.to_sql(tableName, engine, index=False,
                                 dtype=data_types,
                                 if_exists='append')
                    pbar.update(chunkSize)
                if remainder > 0:
                    remainderChunk = data.iloc[chunkCount * chunkSize:]
                    remainderChunk.to_sql(tableName, engine, index=False,
                                          dtype=data_types,
                                          if_exists='append')
                    pbar.update(remainder)
            tqdm.write(f"\033[1;32mTable {tableName} created\033[0;39m")
        engine.dispose()
    except Exception as error:
        print(f"\033[1;31mAn error occured: {error}\033[0;39m")


if __name__ == '__main__':
    load("/app/data_2022_nov.csv", "data_2022_nov")
