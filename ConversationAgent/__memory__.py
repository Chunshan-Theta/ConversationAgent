from __future__ import annotations
from .types.memory import Memory
from .types.static import __SYS_STAGE__, __PASS_TOKEN__
from .types.stage import StageStatus, StageId




class StageOperation:

  @staticmethod
  def set_sys_stage_status(data: Memory, label: StageStatus) -> Memory:
    data.update({__SYS_STAGE__: label})
    return data

  @staticmethod
  def get_sys_stage_status(data: Memory) -> StageStatus:
    return data.get(__SYS_STAGE__, None)



class StagePassToken:
  @staticmethod
  def is_first_access(data: Memory, stage_id: StageId):
      # First Access
      if __PASS_TOKEN__ not in data:
          return True
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
