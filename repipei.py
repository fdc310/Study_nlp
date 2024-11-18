import re

text = """
openapi-cWC1Y24eg9SlZyTPvzVN3HYmbi7dK5p5iPvvwp0Ric5QArN2GVsMiGF1UO0UdamUj 
## 角色 你是一位智慧的禅师,擅长用温和而富有哲理的语言回答人生困惑。 
## 内容要求 - 围绕[情感/人生/哲理/成长]等主题 - 用小事物阐述大道理 - 结合生活场景和事例进行阐述，增强可信度和代入感 ## 风格要求 - 简介明快、通俗易懂 - 富有哲理性和启发性，兼具生活气息与禅意 - 
"""

# 使用正则表达式匹配
match = re.search(r'(openapi-[^\s]+)', text)
if match:
    openapi_string = match.group(1)
    remaining_text = text.replace(openapi_string, '').strip()
    print(f"匹配到的openapi字符串: {openapi_string}")
    print(f"剩余文本: {remaining_text}")
else:
    print("没有匹配到openapi字符串")
