from pydantic import BaseModel
 
class Msg(BaseModel):
    """通用消息响应模型"""
    msg: str  # 消息内容 