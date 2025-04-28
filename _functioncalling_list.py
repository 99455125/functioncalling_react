from typing import Dict, List

from _excel_to_mongo import import_excel_to_mongodb
from _query_from_mongo import query_mongodb

# 第一个函数调用定义 - Excel导入MongoDB
excel_import_function = {
    "name": "import_excel_to_mongodb",
    "description": "将Excel文件数据导入到MongoDB数据库中",
    "parameters": {
        "type": "object",
        "properties": {
            "excel_path": {
                "type": "string",
                "description": "Excel文件的完整路径"
            },
            "db_name": {
                "type": "string",
                "description": "MongoDB数据库名称"
            },
            "collection_name": {
                "type": "string",
                "description": "MongoDB集合名称"
            },
            "mongo_uri": {
                "type": "string",
                "description": "MongoDB连接URI",
                "default": "mongodb://localhost:27017/"
            }
        },
        "required": ["excel_path", "db_name", "collection_name"]
    }
}

# 第二个函数调用定义 - MongoDB查询
mongodb_query_function = {
    "name": "query_mongodb",
    "description": "在MongoDB数据库中执行查询操作",
    "parameters": {
        "type": "object",
        "properties": {
            "collection_name": {
                "type": "string",
                "description": "要查询的集合名称"
            },
            "query": {
                "type": "object",
                "description": "MongoDB查询条件"
            },
            "mongo_uri": {
                "type": "string",
                "description": "MongoDB连接URI",
                "default": "mongodb://localhost:27017/"
            },
            "db_name": {
                "type": "string",
                "description": "数据库名称",
                "default": "test"
            }
        },
        "required": ["collection_name", "query"]
    }
}


# 函数实现示例
def handle_function_call(function_name: str, arguments: Dict) -> Dict:
    if function_name == "import_excel_to_mongodb":
        try:
            import_excel_to_mongodb(
                excel_path=arguments["excel_path"],
                db_name=arguments["db_name"],
                collection_name=arguments["collection_name"],
                mongo_uri=arguments.get("mongo_uri", "mongodb://localhost:27017/")
            )
            return {"status": "success", "message": "数据导入成功"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif function_name == "query_mongodb":
        try:
            results = query_mongodb(
                collection_name=arguments["collection_name"],
                query=arguments["query"],
                mongo_uri=arguments.get("mongo_uri", "mongodb://localhost:27017/"),
                db_name=arguments.get("db_name", "test")
            )
            return {"status": "success", "data": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}