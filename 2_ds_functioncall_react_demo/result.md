D:\PycharmProjects\functioncalling_react\.venv\Scripts\python.exe D:\PycharmProjects\functioncalling_react\2_ds_functioncall_react_demo\agent.py 

=== 大模型回复函数调用 ===
参数名称：import_excel_to_mongodb
参数明细：
"{\"excel_path\":\"D:\\\\dingzhen.xlsx\",\"db_name\":\"test\",\"collection_name\":\"excel_data\",\"mongo_uri\":\"mongodb://192.168.2.192:27017/\"}"
函数调用结果：
{"status": "success", "message": "数据导入成功"}

=== 大模型回复函数调用 ===
参数名称：query_mongodb
参数明细：
"{\"collection_name\":\"excel_data\",\"query\":{\"外号\":{\"$regex\":\"丁真\"},\"姓名\":{\"$ne\":\"丁真\"}},\"mongo_uri\":\"mongodb://192.168.2.192:27017/\",\"db_name\":\"test\"}"
函数调用结果：
{"status": "success", "data": [{"_id": "6810ff103f98e7689ba66291", "外号": "篮球丁真", "姓名": "蔡徐坤", "特长": "唱跳rapper"}]}

=== 最终答案 ===
根据查询结果，以下是外号中带有“丁真”但姓名不是“丁真”的人：

- **姓名**: 蔡徐坤  
  **外号**: 篮球丁真  
  **特长**: 唱跳rapper  

对应的查询SQL为：
```sql
SELECT * FROM excel_data WHERE 外号 LIKE '%丁真%' AND 姓名 != '丁真';
```

Process finished with exit code 0
