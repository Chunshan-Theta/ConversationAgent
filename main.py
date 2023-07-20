from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import NamedTuple, List, Dict, Any, Union
from ConversationAgent.types.memory import Memory
from static.mockBotJson import mockBotJson
from caInterface import call_bot
import os
import json
# import openai
# openai.api_key  = os.environ.get('chatgpt_api_key')




app = FastAPI()



# 資料模型
class Input(BaseModel):
    botJson: Dict[str, Any] = mockBotJson
    memory: Union[ Memory, Any] = {}
    userSay: str = "hi"
class Output(BaseModel):
    memory: Union[ Memory, Any] =  {}
    botSay: str = "hello !"

# 路由
@app.post("/callBot")
async def read_item(item: Input) -> Output:

        botSay, m = call_bot(item.botJson, item.memory, item.userSay)
        # print(f"botSay: {botSay}")
        # print(f"m: {m}")

        return Output(memory=m,botSay="\n".join(botSay))
        # return Output(memory=item.botJson,botSay="123")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)