from __future__ import annotations
import json
import uuid
import re
import random
from typing import Dict, Any, List, Tuple
from .types.memory import Memory
from .types.stage import StageStatus, StageType, BotSpeech, UserSpeech
from .types.static import __USER_TEXT__, __PASS_TOKEN__, __SYS_REPLY__, __SYS_STAGE__, __KEEP_VAR__, __KEEP_DEFAULT_VAR__, __PASSED_STAGES__, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__
from .__memory__ import StageStatusOperation, StagePassTokenOperation, StageUserTextOperation, StageMemoryFragOperation



class Stage:
    def __init__(self, **kwargs):
        self.stage_type = StageType.BASE
        self.stage_uuid_name = kwargs.get("__STAGE_NAME__", str(uuid.uuid4())[:15])
        self.stage_id = f"{self.stage_type}:{self.stage_uuid_name}"
        self.data = kwargs
        self.sys_reply_q1 = "init sys reply"  # init
        self.sys_reply_q2 = "refuse sys reply"  # refuse
        self.sys_reply_complete = "complete sys reply"  # complete
        self.keep_user_text = kwargs.get("__KEEP_USER_TEXT__", False)
        self.switch_welcome = True
        self.switch_refuse = True
        self.switch_completed = True


    def is_fit_needs_n_gen_entity(self, kwargs: Memory) -> Tuple[bool, M]:
        kwargs = StageMemoryFragOperation.set_default_frag(kwargs, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__)
        # if want to reset data, return (True,None) to replace to (True,kwargs)
        kwargs = StageMemoryFragOperation.set_frag(kwargs, self.stage_id, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__)
        return True, kwargs


    @staticmethod
    def set_sys_passed_stage(data, stage_name):
        if __PASSED_STAGES__ in data:
            data[__PASSED_STAGES__].append(stage_name)
        else:
            data[__PASSED_STAGES__] = [stage_name]
        return data

    @staticmethod
    def set_sys_reply(data: Memory, sys_reply_text: BotSpeech) -> Memory:
        if __SYS_REPLY__ in data:
            data[__SYS_REPLY__].append(sys_reply_text)
        else:
            data[__SYS_REPLY__] = [sys_reply_text]
        return data

    @staticmethod
    def transform_mf_ticket(kwargs: Memory, sys_reply: BotSpeech) -> BotSpeech:

        # 
        completed_texts: List[str] = []
        source_sent = StageMemoryFragOperation.encode_NextLineToken(sys_reply)

        #
        for text in source_sent.strip().split(" "):
            var_ticket_name: str | None = StageMemoryFragOperation.get_mf_ticket(text.strip()) # comfirm the string is MF or not. 
            if var_ticket_name is None:
                normal_text: str = StageMemoryFragOperation.decode_NextLineToken(text)
                completed_texts.append(normal_text)
                continue

            ticket_value = StageMemoryFragOperation.get_default_frag(kwargs, var_ticket_name)
            
            
            # replace
            # stage_id : str = var_ticket_info['stage_id']
            # var_label : str = var_ticket_info['label']，
            if ticket_value is None:
              raise KeyError(f"Not Found Var in Memory: {var_ticket_name}" )
            
            if isinstance(ticket_value, float):
                completed_texts.append(str(round(ticket_value, 4)))
            else:
                completed_texts.append(str(ticket_value)) 

                
        finallySent: str = " ".join(completed_texts)
        return finallySent

    def run(self, **kwargs):

        kwargs = self.set_sys_passed_stage(kwargs,self.stage_uuid_name)

        # the user had passed or not.
        if StagePassTokenOperation.had_the_token_was_pass(data=kwargs, stage_id=self.stage_id) is True:
            kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.COMPLETE)
            return kwargs

        # the user had is first time to coming
        if StagePassTokenOperation.is_first_access(kwargs, self.stage_id) is True and self.switch_welcome is True:
            kwargs = StagePassTokenOperation.set_none_token_pass(data=kwargs, stage_id=self.stage_id)
            kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.FIRST)

            # random reply from welcome corpus (q1)
            sys_reply: BotSpeech = self.__choice_a_reply__(self.sys_reply_q1)

            #
            sys_reply: BotSpeech = self.transform_mf_ticket(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        # computer core. the main flow in stage, base on static rule of stage to check rusult is pass or not.
        # return pass_token and data
        # pass_token: [True,  False]
        #     True -> complete
        #     False -> refuse
        is_fit_token, kwargs = self.is_fit_needs_n_gen_entity(kwargs)
        if is_fit_token is False and self.switch_refuse is True:
            # REFUSE FLOW
            kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.REFUSE)
            sys_reply = self.__choice_a_reply__(self.sys_reply_q2)

            sys_reply = self.transform_mf_ticket(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        
        # COMPLETE FLOW
        kwargs = kwargs if kwargs is not None else {}
        kwargs = StageUserTextOperation.save_user_text(kwargs, self.stage_id)
        if not self.keep_user_text:
            kwargs = StageUserTextOperation.clear_user_text(kwargs)
        kwargs = StagePassTokenOperation.set_true_token_pass(kwargs, stage_id=self.stage_id)
        kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.COMPLETE)

        # insert ENTITY
        sys_reply = self.transform_mf_ticket(kwargs, self.__choice_a_reply__(self.sys_reply_complete))
        return self.set_sys_reply(kwargs, sys_reply)

    @staticmethod
    def __choice_a_reply__(sys_reply):
        if isinstance(sys_reply, list):
            sys_reply = random.choice(sys_reply)
            return sys_reply
        return sys_reply


a = Stage()
res = a.run()
assert res.get(__SYS_STAGE__, None) == StageStatus.FIRST
res[__USER_TEXT__] = "hi"
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE
