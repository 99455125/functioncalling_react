import json
from _prompt import REACT_PROMPT
from _ds_client import client
from _functioncalling_list import excel_import_function, mongodb_query_function, handle_function_call

functions = [excel_import_function, mongodb_query_function]

def send_messages(messages):
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    return response

if __name__ == "__main__":
    instructions = ("你是一个excel查询工具, 用户给你excel路径， 你帮助用户获取excel内符合用户要求的数据。因为excle数据量过大, 不方便将所有数据喂给你来进行数据分析, 所以你在处理用户excel查询时，先将excel数据保存至mongodb，再根据用户生成sql，将查询到符合要求的mongodb中的数据返回给用户。"
                    "如果用户没有给出使用mongodb时的集合名称， 你使用默认集合名称为 'excel_data'。")
    query = "excel路径：D:\dingzhen.xlsx, 请帮我查出所有外号中带有丁真的人"

    prompt = REACT_PROMPT.format(instructions=instructions)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query}
    ]


    while True:
        response_message = send_messages(messages)

        # 检查是否需要函数调用
        if response_message.get("function_call"):
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)
            result = handle_function_call(function_name, function_args)
            # 将函数调用结果反馈给大模型
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(result, ensure_ascii=False)
            })
            continue

        # 输出最终答案
        print("最终答案:", response_message.content)
        break



