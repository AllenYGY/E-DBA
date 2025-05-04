import re

def verify_email(email: str) -> bool:
    """验证邮箱格式的有效性
    
    Args:
        email: 需要验证的邮箱地址
        
    Returns:
        bool: 邮箱格式是否有效
    """
    # 邮箱格式的正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # 验证邮箱格式
    if re.match(pattern, email):
        return True
    return False