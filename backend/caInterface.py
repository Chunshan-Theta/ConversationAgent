from ConversationAgent import mock_client, mock_client_once
from ConversationAgent.types.static import __USER_TEXT__
from ConversationAgent.types.memory import Memory
from ConversationAgent.__stage__ import Stage
from ConversationAgent.__agent__ import Agent, MultiAgent
from ConversationAgent.LibStage import gen_multi_agent
from typing import Dict, Any, Tuple


#
def call_bot(bot_json: Dict[str, Any], m: Memory, userText: str) -> Tuple[str, Memory]:
    agent: MultiAgent = gen_multi_agent(bot_json)

    return mock_client_once(agent, userText, m)


