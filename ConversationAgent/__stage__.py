from __future__ import annotations
import json
import uuid
import re
import random
from typing import Dict, Any, List, Tuple
from .types.memory import Memory
from .types.stage import StageStatus, StageType
from .types.static import __USER_TEXT__, __PASS_TOKEN__, __SYS_REPLY__, __SYS_STAGE__, __KEEP_VAR__, __KEEP_DEFAULT_VAR__, __PASSED_STAGES__, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__
from .__memory__ import StageStatusOperation, StagePassTokenOperation



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

    

    @staticmethod
    def clear_user_text(data):
        # First Access
        _ = data.pop(__USER_TEXT__, None)
        return data

    @classmethod
    def save_user_text(cls, data, stage_id, label):
        user_text = cls.get_user_text(data)
        data = cls.set_var(data, __KEEP_DEFAULT_VAR__, label, user_text)
        return cls.set_var(data, stage_id, label, user_text)

    @staticmethod
    def get_user_text(data):
        return data.get(__USER_TEXT__, None)

    def is_fit_needs_n_gen_entity(self, kwargs) -> Tuple[bool, dict]:
        kwargs = self.set_default_var(kwargs, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__)
        # if want to reset data, return (True,None) to replace to (True,kwargs)
        return True, kwargs

    @staticmethod
    def is_var_label(label_string):
        return None if re.match("^var\t.*\t.*\tvar$", label_string) is None else label_string.split("\t")

    @staticmethod
    # def is_var_label_human(label_string):
    def get_var_name_from_string(label_string: str) -> str | None:
        head: str="%%"
        tail: str="%%"
        return None if re.match(f"^{head}.*{tail}$", label_string) is None else label_string[len(head):-1*len(tail)]

    @classmethod
    def get_default_var_ticket(cls, label: str) -> Dict[str, str]:
        return cls.get_var_ticket(__KEEP_DEFAULT_VAR__, label)

    def set_default_var(self, data, label, save_text):
        data = self.set_var(data, self.stage_id, label, save_text)
        data = self.set_var(data, __KEEP_DEFAULT_VAR__, label, save_text)
        return data
    
    @classmethod
    def get_default_var(self, data: Memory, label: str) -> any:
        return self.get_var(data, __KEEP_DEFAULT_VAR__, label)

    @staticmethod
    def get_var_ticket(stage_id: str, label: str) -> Dict[str, str]:
        assert "\t" not in stage_id
        assert "\t" not in label
        # return f"var\t{stage_id}\t{label}\tvar"
        return {
            "stage_id": stage_id,
            "label": label
        }

    @classmethod
    def set_var(cls, data, stage_id, label, save_text):
        if __KEEP_VAR__ not in data:
            data[__KEEP_VAR__] = {}
        if stage_id not in data[__KEEP_VAR__]:
            data[__KEEP_VAR__][stage_id] = {}

        data[__KEEP_VAR__][stage_id][label] = save_text
        return data

    @classmethod
    def get_var(cls, data, stage_id, label):
        try:
            return data[__KEEP_VAR__][stage_id][label]
        except KeyError:
            return None

    @staticmethod
    def set_sys_passed_stage(data, stage_name):
        if __PASSED_STAGES__ in data:
            data[__PASSED_STAGES__].append(stage_name)
        else:
            data[__PASSED_STAGES__] = [stage_name]
        return data

    @staticmethod
    def set_sys_reply(data, sys_reply_text):
        if __SYS_REPLY__ in data:
            data[__SYS_REPLY__].append(sys_reply_text)
        else:
            data[__SYS_REPLY__] = [sys_reply_text]
        return data

    @classmethod
    def replace_var_ticket_to_string(cls, kwargs: Dict[str, Any], sys_reply: str) -> str:

        __NEXT_LINE__ = "||n||"

        # 
        completed_texts: List[str] = []
        source_sent = sys_reply.replace("\n", __NEXT_LINE__)

        #
        for text in source_sent.strip().split(" "):


            # check the var is var ticket or not.
            text = text.strip()
            var_ticket_name: str | None = cls.get_var_name_from_string(text)
            if var_ticket_name is None:
                normal_text: str = text.replace(__NEXT_LINE__, "\n")
                completed_texts.append(f"{normal_text}")
                continue

            var_ticket_info = cls.get_default_var_ticket(var_ticket_name)
            
            
            # replace
            stage_id : str = var_ticket_info['stage_id']
            var_label : str = var_ticket_info['label']
            try:
                var_value: Any = kwargs[__KEEP_VAR__][stage_id][var_label]
            except KeyError:
                raise KeyError(f"Not Found Var in Memory: {kwargs[__KEEP_VAR__][{stage_id}][{var_label}]}" )
            
            if isinstance(var_value, float):
                completed_texts.append(str(round(var_value, 4)))
            else:
                completed_texts.append(str(var_value)) 

                
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
            sys_reply = self.__choice_a_reply__(self.sys_reply_q1)

            #
            sys_reply = self.replace_var_ticket_to_string(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        # computer core. the main flow in stage, base on static rule of stage to check rusult is pass or not.
        # return pass_token and data
        # pass_token: [True,  False]
        #     True -> complete
        #     False -> refuse
        is_fit_token, kwargs = self.is_fit_needs_n_gen_entity(kwargs)
        if is_fit_token is False:
            # REFUSE FLOW
            kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.REFUSE)
            sys_reply = self.__choice_a_reply__(self.sys_reply_q2)

            sys_reply = self.replace_var_ticket_to_string(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        elif is_fit_token is True:
            # COMPLETE FLOW
            kwargs = kwargs if kwargs is not None else {}
            kwargs = self.save_user_text(kwargs, self.stage_id, __USER_TEXT__)
            if not self.keep_user_text:
                kwargs = self.clear_user_text(kwargs)
            kwargs = StagePassTokenOperation.set_true_token_pass(kwargs, stage_id=self.stage_id)
            kwargs = StageStatusOperation.set_sys_stage_status(kwargs, StageStatus.COMPLETE)

            # insert ENTITY
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.__choice_a_reply__(self.sys_reply_complete))
            return self.set_sys_reply(kwargs, sys_reply)
        #
        # elif is_fit_token is True and kwargs is None:  # reset route
        #     sys_reply = self.replace_var_ticket_to_string(kwargs, self.__choice_a_reply__(self.sys_reply_complete))
        #     return self.set_sys_reply({}, sys_reply)

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
