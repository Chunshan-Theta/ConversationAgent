import unittest
from ConversationAgent.LibStage import gen_multi_agent
from ConversationAgent import __agent__, mock_client_once
from typing import Dict, Any
from ConversationAgent.__nlp_tool__ import similar_text_distance, SimilarResult



# The test class
class TestREStage(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        

    def test_tickets(self):
                
        corpus= [
            "我想去醫院",
            "我想去大學",
            "我想去台北",
            "我想去跑步",
            "我想去公園"
        ]
        sentence="我想去大公園"
        ans: SimilarResult = SimilarResult(sentence='我想去大公園', corpus=['我想去醫院', '我想去大學', '我想去台北', '我想去跑步', '我想去公園'], ans='我想去公園', score=0.6666666666666667)
        res: SimilarResult = similar_text_distance(sentence,corpus)
        self.assertTrue(res.ans == "我想去公園" , f"{res.ans} != 我想去公園")
        self.assertTrue(res.score > 0.5, f"{res.score} !> 0.5")

    def test_question(self):
                
        corpus= ['廁所在哪裡', '詢問處在哪裡', '診所在哪裡']
        sentence="附近有廁所嗎"
        res: SimilarResult = similar_text_distance(sentence,corpus)
        # ans: SimilarResult = SimilarResult(sentence='我想去大公園', corpus=['我想去醫院', '我想去大學', '我想去台北', '我想去跑步', '我想去公園'], ans='我想去公園', score=0.6666666666666667)
        # self.assertTrue(ans, similar_text_distance(sentence,corpus))
        self.assertTrue(res.ans == "廁所在哪裡", f"{res.ans} != 廁所在哪裡")
        # self.assertTrue(res.score > 0.5, f"{res.score} !> 0.5")
        






