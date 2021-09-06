import json
import uuid
import re

from .__agent__ import Agent
from .__stage__ import Stage, __USER_TEXT__, __SYS_REPLY__, StageStatus, \
    __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__

__MOCK_STAGES_LABEL_1__ = "__MOCK_STAGES_LABEL_1__"


def mock_client_with_test(agent, says, tests):
    data = {}
    for s, t in zip(says, tests):
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        assert t == reply_text


def mock_client(agent, says, show_data=True, show_user_text=True):
    data = {}
    for s in says:
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        if show_user_text:
            print("\t用戶:", s)
        print("系統:", reply_text)
        if show_data:
            print("\t系統資料:", data)


def mock_client_human(agent):
    data = {}
    while True:
        s = input("請輸入：")
        data[__USER_TEXT__] = s
        if s == "exit":
            break
        reply_text, data = agent.run_all_stages(**data)
        print("系統:", reply_text)


def mock_client_once(agent: Agent, text: str, data: dict):
    data[__USER_TEXT__] = text
    return agent.run_all_stages(**data)


def to_bot(agent: Agent, text: str, data: dict):
    return mock_client_once(agent, text, data)
