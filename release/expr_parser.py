#表达式解析器（把用户输入的字符串转换为可调用的数学函数）
import math

#允许用户使用的数学函数白名单
SAFE_DICT = {
   "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,    
    "acos": math.acos,    
    "atan": math.atan,
    "sqrt": math.sqrt,
    "abs": abs,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
}

def parse_expression(expr_str: str):
     # 第1步：数学中常见写法替换为python可识别的形式
    cleaned = expr_str.strip()
    cleaned =  cleaned.replace("^", "**")
    cleaned = cleaned.replace("ln( ", "math.log(")
     # 第2步：安全检查 —— 只允许数字、字母、运算符、括号、空格、小数点
    allowed_chars = set("0123456789+-*/.() xyzXYZsincotagqlrbeEPp ")
    for char in cleaned:
        if char not in allowed_chars:
            raise ValueError(f"表达式包含不允许的字符: '{char}'")

    # 第3步：构建安全的执行环境（只有白名单里的函数，没有危险操作）
    safe_env = dict(SAFE_DICT)  # 复制一份，避免污染全局

    # 第4步：试运行一次，验证表达式是否合法
    try:
        # 用 eval 执行，但环境是受控的 safe_env
        code = compile(cleaned, "<expression>", "eval")
        safe_env["x"] = 0  # 先给 x 一个默认值，看看能不能算出来
        eval(code, {"__builtins__": {}}, safe_env)  # 先用 x=0 试一下
    except Exception as e:
        raise ValueError(f"表达式无法解析: {e}")

    # 第5步：返回一个真正的函数，以后调用 f(3.14) 就能算出 y 值
    def f(x: float) -> float:
        safe_env["x"] = x
        try:
            result = eval(code, {"__builtins__": {}}, safe_env)
            return float(result)
        except (ValueError, ZeroDivisionError, OverflowError):
            return float("nan")  # 算不出来就返回 NaN，绘图时跳过

    return f
