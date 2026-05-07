import json
from typing import Dict, List

from _shared import load_config
from openai import OpenAI

from gitcode_api.llm import GitCodeOpenAITool

MESSAGE_SEP = "\n" + "=" * 60 + "\n"
USER_QUERY = "List the repos owned by SushiNinja."
CONVERSATION: List[Dict[str, str]] = [dict(role="user", content=USER_QUERY)]

config = load_config()
tools = {"gitcode_api_tool": GitCodeOpenAITool(api_key=config.api_key)}
client = OpenAI(api_key=config.llm_api_key, base_url=config.llm_api_base)

print("U:\n" + USER_QUERY + MESSAGE_SEP)
while True:
    response = (
        client.chat.completions.create(
            model="gpt-5.4-nano",
            messages=CONVERSATION,
            tools=[tools["gitcode_api_tool"].tool],
        )
        .choices[0]
        .message
    )
    CONVERSATION.append(response.to_dict())
    print("A:\n" + (response.content or ""))
    for tool_call in response.tool_calls or []:
        selected_tool = tools[tool_call.function.name]
        result = selected_tool(**json.loads(tool_call.function.arguments))
        CONVERSATION.append(dict(role="tool", tool_call_id=tool_call.id, content=result))
        print(f"<Calling tool {tool_call.function.name}({tool_call.function.arguments})>")
    print(MESSAGE_SEP)
    if not response.tool_calls:
        break
