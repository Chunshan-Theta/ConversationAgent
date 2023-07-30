import unittest
from ConversationAgent.LibStage import gen_multi_agent
from ConversationAgent import __agent__, mock_client_once, to_bot
from typing import Dict, Any
from ConversationAgent.LibStage import QAStage

"""
##########
__NEW QAWorkerSTAGE__
##########
"""

# The test class
class TestREStage(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        

    def test_tickets(self):

        bot_json = {
            "__MAIN_STAGES__": [
                {
                    "stage_type": "__Classify_STAGE__",
                    "__STAGE_NAME__": "標籤抓取",
                    "question": {
                        "sys_welcome": "共抓取5種標籤： 生氣 開心 難過 愉快 悲傷 ",
                        "sys_refuse": "拒絕： %%result%% ",
                        "sys_complete": "完成： %%result%% "
                    },
                    "__Classify_THRESHOLD__": 1.0,
                    "is_fits": [
                        [".*生氣.*", "生氣"],
                        [".*開心.*", "開心"],
                        [".*難過.*", "難過"],
                        [".*愉快.*", "愉快"],
                        [".*悲傷.*", "悲傷"],
                    ],
                    "__SAVED_NAME__": {
                        "__SAVE_Classify_THRESHOLD__": "__SAVE_Classify_THRESHOLD__",
                        "__SAVE_Classify_PASS__": "__SAVE_Classify_PASS__",
                        "__SAVE_Classify_Best__": "__SAVE_Classify_Best__",
                        "__SAVE_Classify_result__": "result"
                    }
                }
            ]
        }
        agent = gen_multi_agent(bot_json)

        #
        text = "hi"
        reply_text, data = mock_client_once(agent, text, {})
        self.assertTrue(['共抓取5種標籤： 生氣 開心 難過 愉快 悲傷'] == reply_text)

        #
        text = "開心"
        reply_text, data = mock_client_once(agent, text, data)
        self.assertTrue(["完成： {'生氣': 0.0, '開心': 1.0, '難過': 0.0, '愉快': 0.0, '悲傷': 0.0}"] == reply_text)

        #
        text = "hi"
        reply_text, data = mock_client_once(agent, text, {})
        text = "請拒絕"
        reply_text, data = mock_client_once(agent, text, data)
        self.assertTrue(["拒絕： {'生氣': 0.0, '開心': 0.0, '難過': 0.0, '愉快': 0.0, '悲傷': 0.0}"] == reply_text)
