from pymongo import MongoClient
from typing import Dict, List, Any
import logging


def query_mongodb(
        collection_name: str,
        query: Dict,
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name: str = "test"
) -> List[Dict[str, Any]]:
    """
    在MongoDB中执行查询操作

    Args:
        collection_name: 集合名称
        query: MongoDB查询条件
        mongo_uri: MongoDB连接URI
        db_name: 数据库名称

    Returns:
        查询结果列表
    """
    try:
        # 连接MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # 执行查询
        results = list(collection.find(query))

        # 处理ObjectId（将其转换为字符串）
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        logging.info(f"从 {db_name}.{collection_name} 成功查询到 {len(results)} 条记录")

        # 关闭连接
        client.close()

        return results

    except Exception as e:
        logging.error(f"查询数据时发生错误: {str(e)}")
        raise