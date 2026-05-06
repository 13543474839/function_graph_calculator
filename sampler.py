#坐标点生成器作用：在指定范围内，对函数进行采样，生成一堆 (x, y) 坐标点
import math
from expr_parser import parse_expression

def generate_points(
    expr_str: str,
    x_min: float = -10,
    x_max: float = 10,
    num_points: int = 500,
) -> list[dict]:
    """
    根据表达式和范围，生成坐标点列表

    参数:
        expr_str: 数学表达式字符串
        x_min: x 轴最小值
        x_max: x 轴最大值
        num_points: 采样点数量（越多曲线越平滑）

    返回:
        [{"x": -10.0, "y": 100.0}, {"x": -9.96, "y": 99.2}, ...]
        y 为 NaN 的点会保留（前端需要用它来断开曲线）
    """
    # 第1步：解析表达式，得到可调用的函数
    f = parse_expression(expr_str)

    # 第2步：计算 x 的步长（均匀采样）
    step = (x_max - x_min) / (num_points - 1)

    # 第3步：逐个计算每个 x 对应的 y
    points = []
    for i in range(num_points):
        x = x_min + i * step
        y = f(x)

        # 过滤掉无穷大的值，保留 NaN（NaN 用于断线）
        if math.isinf(y):
            y = float("nan")

        points.append({"x": round(x, 6), "y": y})

    return points



