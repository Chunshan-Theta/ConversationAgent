import unittest
from ConversationAgent.LibStage import gen_multi_agent
from ConversationAgent import __agent__, mock_client_once, to_bot
from typing import Dict, Any
from ConversationAgent.LibStage import QAStage
from ConversationAgent.__memory__ import StageMemoryFragOperation 

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
                    "stage_type": "__RE_STAGE__",
                    "question": {
                        "sys_reply_q1": "哈囉請問要做什麼？",
                        "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
                        "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
                    },
                    "is_fits": [
                        [
                            "(問答|問題|詢問)+",
                            "selected_service"
                        ]
                    ]
                },
                {
                    "stage_type": "Switch",
                    "stages_filter": [
                        [
                            "selected_service",
                            "問答",
                            "_問答_", "="

                        ],
                        [
                            "selected_service",
                            "問題",
                            "_問答_", "="
                        ],
                        [
                            "selected_service",
                            "詢問",
                            "_問答_", "="
                        ]
                    ]
                }
            ],
            
            "_問答_": [
                {
                    "stage_type": "__QA_STAGE__",
                    "corpus": {
                        "廁所在哪裡": "這裡沒有廁所",
                        "詢問處在哪裡": "這裡沒有詢問處",
                        "診所在哪裡": "這裡沒有診所",
                    },
                    "question": {
                        "sys_reply_q1": "請問有什麼問題呢？",
                        "sys_reply_q2": "",
                        "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
                    },
                    "is_fits": []
                }

            ],
            "_訂票_": [
                {
                    "stage_type": "__RE_STAGE__",
                    "question": {
                        "sys_reply_q1": "",
                        "sys_reply_q2": "",
                        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
                    },
                    "is_fits": [],
                    "__DISSABLE_Q1__": True
                }
            ]
        }
        data = {}
        agent = gen_multi_agent(bot_json)

        #
        text = "hi"
        reply_text, data = to_bot(agent, text, data)
        # print(f"data: {data}")
        self.assertTrue(reply_text==["哈囉請問要做什麼？"], f"{reply_text}!='哈囉請問要做什麼？'")
        self.assertTrue(len(data["__PASSED_STAGES__"])==1)

        # #
        text = "我有點問題"
        reply_text, data = to_bot(agent, text, data)
        # print(f"data: {data}")
        # print(f"reply_text: {reply_text}")
        self.assertTrue(reply_text==['好的，將開始 『 問題 』', '請問有什麼問題呢？'], f"{reply_text}!=['好的，將開始 『 問題 』', '請問有什麼問題呢？']")
        self.assertTrue(len(data["__PASSED_STAGES__"])==3)
        self.assertTrue(data["KEEP_VAR"]["DEFAULT_VAR"]["selected_service"]=='問題')
        
        

        # #
        text = "附近有廁所嗎"
        reply_text, data = to_bot(agent, text, data)
        # print(f"data: {data}")
        # print(f"reply_text: {reply_text}")
        self.assertTrue(StageMemoryFragOperation.get_default_frag(data, QAStage.__QA_RESPOND_QUESTION__[0])=='廁所在哪裡')










