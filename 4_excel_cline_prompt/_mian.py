from openai import OpenAI
from _functioncalling_list import excel_import_function, mongodb_query_function

# 指定API密钥
client = OpenAI(
    api_key="你的API密钥"
)

functions = [excel_import_function, mongodb_query_function]

# 在OpenAI API调用中使用
response = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "sdadfads"}],
    functions=functions,
    function_call="auto"
)