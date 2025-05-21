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

def extract_email_domain(email: str) -> str:
    """
    从邮箱地址中提取域名部分
    
    Args:
        email: 邮箱地址
        
    Returns:
        str: 域名部分，如果邮箱格式无效则返回空字符串
    """
    if not verify_email(email):
        return ""
    
    try:
        return email.split('@')[1].lower()
    except IndexError:
        return ""