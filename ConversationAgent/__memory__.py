from __future__ import annotations
from .types.memory import Memory, MemoryFrag, MemoryValue
from .types.static import __SYS_STAGE__, __PASS_TOKEN__, __USER_TEXT__, __KEEP_DEFAULT_VAR__, __KEEP_VAR__
from .types.stage import StageStatus, StageId, UserSpeech
import re


class StageMemoryFragOperation:
    @staticmethod
    def set_frag(data: Memory, stage_id: StageId, mf: MemoryFrag, mv: MemoryValue) -> Memory:
        if __KEEP_VAR__ not in data:
            data[__KEEP_VAR__] = {}
        if stage_id not in data[__KEEP_VAR__]:
            data[__KEEP_VAR__][stage_id] = {}
        data[__KEEP_VAR__][stage_id][mf] = mv
        return data
      
    @staticmethod
    def get_frag(data: Memory, stage_id: StageId, mf: MemoryFrag) -> MemoryValue | None:
        try:
            return data[__KEEP_VAR__][stage_id][mf]
        except KeyError:
            return None

    @staticmethod
    def set_default_frag(data: Memory, mf: MemoryFrag, mv: MemoryValue) -> Memory:
        data = StageMemoryFragOperation.set_frag(data, __KEEP_DEFAULT_VAR__, mf, mv)
        return data
    
    @staticmethod
    def get_default_frag(data: Memory, mf: MemoryFrag) -> MemoryValue | None:
        return StageMemoryFragOperation.get_frag(data, __KEEP_DEFAULT_VAR__, mf)


    ## Frags: PickUpTicket
    __NEXT_LINE__ = "||n||"
    @staticmethod
    def encode_NextLineToken(sent: UserSpeech) -> str:
        return sent.replace("\n", StageMemoryFragOperation.__NEXT_LINE__)
    @staticmethod
    def decode_NextLineToken(sent: UserSpeech) -> str:
        return sent.replace(StageMemoryFragOperation.__NEXT_LINE__, "\n")

    def get_mf_ticket(sent: UserSpeech) -> MemoryFrag: 
        head: str="%%"
        tail: str="%%"
        return None if re.match(f"^{head}.*{tail}$", sent) is None else sent[len(head):-1*len(tail)]
        
    # def get_mv_by_default_ticket(mf: MemoryFrag) -> MemoryValue | None: 
    #    # return StageMemoryFragOperation.get_default_frag(mf)
  
    # @staticmethod
    # def get_var_name_from_string(label_string: str) -> str | None:
    #     head: str="%%"
    #     tail: str="%%"
    #     return None if re.match(f"^{head}.*{tail}$", label_string) is None else label_string[len(head):-1*len(tail)]

    # @classmethod
    # def get_default_var_ticket(cls, label: str) -> Dict[str, str]:
    #     return cls.get_var_ticket(__KEEP_DEFAULT_VAR__, label)


    # @staticmethod
    # def get_var_ticket(stage_id: str, label: str) -> Dict[str, str]:
    #     assert "\t" not in stage_id
    #     assert "\t" not in label
    #     # return f"var\t{stage_id}\t{label}\tvar"
    #     return {
    #         "stage_id": stage_id,
    #         "label": label
    #     }

class StageUserTextOperation:
    @staticmethod
    def clear_user_text(data: Memory) -> Memory:
        _ = data.pop(__USER_TEXT__, None)
        return data

    @staticmethod
    def save_user_text(data: Memory, stage_id: StageId) -> Memory:
        user_text = StageUserTextOperation.get_user_text(data)
        data = StageMemoryFragOperation.set_frag(data, __KEEP_DEFAULT_VAR__, __USER_TEXT__, user_text)
        return StageMemoryFragOperation.set_frag(data, stage_id, __USER_TEXT__ , user_text)

    @staticmethod
    def get_user_text(data) -> str | None:
        return data.get(__USER_TEXT__, None)


class StageStatusOperation:

  @staticmethod
  def set_sys_stage_status(data: Memory, label: StageStatus) -> Memory:
    data.update({__SYS_STAGE__: label})
    return data

  @staticmethod
  def get_sys_stage_status(data: Memory) -> StageStatus:
    return data.get(__SYS_STAGE__, None)



class StagePassTokenOperation:
  @staticmethod
  def is_first_access(data: Memory, stage_id: StageId):
      # First Access
      if __PASS_TOKEN__ not in data:
          return True
      # print(f"{data[__PASS_TOKEN__]}: {stage_id}")  
      if stage_id not in data[__PASS_TOKEN__]:
          return True
      return False
  
  @staticmethod
  def had_the_token_was_pass(data: Memory, stage_id: StageId) -> bool:
      token = data.get(__PASS_TOKEN__, None)
      if token is None:
          return False
      if isinstance(token, dict) and token.get(stage_id, None) is True:
          return True
      else:
          return False

  @staticmethod
  def set_none_token_pass(data: Memory, stage_id: StageId):
      if __PASS_TOKEN__ not in data:
          data[__PASS_TOKEN__] = {}
      data[__PASS_TOKEN__][stage_id] = None
      return data

  @staticmethod
  def set_true_token_pass(data: Memory, stage_id: StageId):
      if __PASS_TOKEN__ not in data:
          data[__PASS_TOKEN__] = {}
      data[__PASS_TOKEN__][stage_id] = True
      return data
