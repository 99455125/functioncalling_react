import logging

import pandas as pd
from pymongo import MongoClient


def import_excel_to_mongodb(
        excel_path: str,
        db_name: str,
        collection_name: str,
        mongo_uri: str = "mongodb://localhost:27017/"
) -> None:
    """
    将Excel文件数据导入到MongoDB数据库
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_path)

        # 将DataFrame转换为字典列表
        records = df.to_dict('records')

        # 连接MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # 插入数据
        result = collection.insert_many(records)

        logging.info(f"成功导入 {len(result.inserted_ids)} 条记录到 {db_name}.{collection_name}")

        # 关闭连接
        client.close()

    except Exception as e:
        logging.error(f"导入数据时发生错误: {str(e)}")
        raise