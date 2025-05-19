import time
from typing import Dict, Tuple
from datetime import datetime

# 使用字典存储验证码，格式: {email: (code, expire_time)}
_email_code_store: Dict[str, Tuple[str, float]] = {}

# 使用字典存储发送频率限制，格式: {email: last_send_time}
_email_send_limit: Dict[str, float] = {}

# 配置
CODE_EXPIRE_SECONDS = 300  # 验证码有效期5分钟
SEND_INTERVAL_SECONDS = 60  # 发送间隔1分钟
MAX_ATTEMPTS = 5  # 最大尝试次数
ATTEMPT_WINDOW = 300  # 尝试窗口期5分钟

# 使用字典存储尝试次数，格式: {email: [(attempt_time, is_success), ...]}
_attempt_records: Dict[str, list] = {}

def set_email_code(email: str, code: str, expire: int = CODE_EXPIRE_SECONDS) -> None:
    """
    存储邮箱验证码
    :param email: 邮箱地址
    :param code: 验证码
    :param expire: 过期时间（秒）
    """
    _email_code_store[email] = (code, time.time() + expire)

def get_email_code(email: str) -> str | None:
    """
    获取邮箱验证码
    :param email: 邮箱地址
    :return: 验证码或None（如果不存在或已过期）
    """
    if email not in _email_code_store:
        return None
    
    code, expire_time = _email_code_store[email]
    if time.time() > expire_time:
        del _email_code_store[email]
        return None
    return code

def can_send_code(email: str) -> Tuple[bool, str]:
    """
    检查是否可以发送验证码
    :param email: 邮箱地址
    :return: (是否可以发送, 原因)
    """
    current_time = time.time()
    
    # 检查发送频率
    if email in _email_send_limit:
        last_send_time = _email_send_limit[email]
        if current_time - last_send_time < SEND_INTERVAL_SECONDS:
            remaining = int(SEND_INTERVAL_SECONDS - (current_time - last_send_time))
            return False, f"Please wait {remaining} seconds before requesting a new code"
    
    # 检查尝试次数
    if email in _attempt_records:
        # 清理过期的尝试记录
        _attempt_records[email] = [
            (t, s) for t, s in _attempt_records[email] 
            if current_time - t < ATTEMPT_WINDOW
        ]
        
        if len(_attempt_records[email]) >= MAX_ATTEMPTS:
            return False, "Too many attempts, please try again later"
    
    return True, ""

def record_send_code(email: str) -> None:
    """
    记录验证码发送时间
    :param email: 邮箱地址
    """
    _email_send_limit[email] = time.time()

def record_attempt(email: str, is_success: bool) -> None:
    """
    记录验证码尝试
    :param email: 邮箱地址
    :param is_success: 是否验证成功
    """
    if email not in _attempt_records:
        _attempt_records[email] = []
    _attempt_records[email].append((time.time(), is_success))

def clear_expired_data() -> None:
    """
    清理过期的数据
    """
    current_time = time.time()
    
    # 清理过期的验证码
    expired_emails = [
        email for email, (_, expire_time) in _email_code_store.items()
        if current_time > expire_time
    ]
    for email in expired_emails:
        del _email_code_store[email]
    
    # 清理过期的发送限制
    expired_sends = [
        email for email, last_send in _email_send_limit.items()
        if current_time - last_send > SEND_INTERVAL_SECONDS * 2
    ]
    for email in expired_sends:
        del _email_send_limit[email]
    
    # 清理过期的尝试记录
    for email in _attempt_records:
        _attempt_records[email] = [
            (t, s) for t, s in _attempt_records[email]
            if current_time - t < ATTEMPT_WINDOW
        ]
        if not _attempt_records[email]:
            del _attempt_records[email] 