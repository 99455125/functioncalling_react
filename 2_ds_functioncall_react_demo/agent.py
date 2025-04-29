import json
from _prompt import REACT_PROMPT
from _ds_client import client
from _functioncalling_list import excel_import_function, mongodb_query_function, handle_function_call

functions = [excel_import_function, mongodb_query_function]


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )
    return response.choices[0].message


if __name__ == "__main__":
    instructions = (
        "你是一个excel查询工具。用户提供excel路径后，你需要先将数据存入MongoDB，"
        "再根据用户需求生成查询SQL。函数调用成功后，根据返回状态生成SQL。"
        "默认集合名为'excel_data'，参数缺省时使用默认值。"
    )
    query = "excel路径：D:\dingzhen.xlsx，请帮我查出所有外号中带有丁真但姓名不是丁真的人"

    messages = [
        {"role": "system", "content": REACT_PROMPT.format(instructions=instructions)},
        {"role": "user", "content": query}
    ]

    while True:
        response_message = send_messages(messages)

        # 添加助手的回复到对话历史
        assistant_message = {
            "role": response_message.role,
            "content": response_message.content or None  # 确保content不为空字符串
        }
        if response_message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in response_message.tool_calls
            ]
        messages.append(assistant_message)

        # 处理工具调用
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:

                print(f"\n=== 大模型回复函数调用 ===")
                print(f"参数名称：" + tool_call.function.name)
                print("参数明细：")
                print(json.dumps(tool_call.function.arguments, indent=2, ensure_ascii=False))


                # 执行函数调用
                result = handle_function_call(
                    tool_call.function.name,
                    json.loads(tool_call.function.arguments))

                print("函数调用结果：")
                print(json.dumps(result, ensure_ascii=False))

                # 添加函数调用结果到对话历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(result, ensure_ascii=False)
                })

                # 继续循环处理后续响应
            continue

        # 处理最终回复
        if response_message.content:
            print("\n=== 最终答案 ===")
            print(response_message.content)
            break