# API 接口将函数解析器和坐标点生成器组合在一起，提供一个简单的接口，供用户调用。
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sampler import generate_points

app = FastAPI(title="图形计算器 API")
# 允许跨域请求（前端可能在不同的端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#接受表达式返回坐标点列表的接口
@app.get("/api/plot")
def plot_expression(
    expr: str = Query(..., description="数学表达式，例如 'sin(x)', 'x^2 + 3*x - 5'"),
    x_min: float = Query(-10.0, description="x 轴最小值"),
    x_max: float = Query(10.0, description="x 轴最大值"),
    points: int = Query(500, description="采样点数量，越多曲线越平滑"),
):
    try:
        data = generate_points(expr, x_min, x_max, points)
        return {
            "expression": expr,
            "points": data,
            "count": len(data),
            "error": None,
        }
    except ValueError as e:
        return {
            "expression": expr,
            "points": [],
            "count": 0,
            "error": str(e),
        }

#返回预设表达式列表的接口
@app.get("/api/presets")
def get_presets():
    return {
        "presets": [
            {"name": "正弦波", "expr": "sin(x)"},
            {"name": "余弦波", "expr": "cos(x)"},
            {"name": "抛物线", "expr": "x^2"},
            {"name": "三次曲线", "expr": "x^3 - 3*x"},
            {"name": "指数增长", "expr": "exp(x/3)"},
            {"name": "对数曲线", "expr": "log(abs(x)+1)"},
            {"name": "阻尼振荡", "expr": "exp(-abs(x)/5) * sin(3*x)"},
            {"name": "绝对值", "expr": "abs(x)"},
            {"name": "高斯曲线", "expr": "exp(-x^2/2)"},
            {"name": "S型曲线", "expr": "1/(1+exp(-x))"},
        ]
    }

    presets = [
            {"name": "正弦波", "expr": "sin(x)"},
            {"name": "余弦波", "expr": "cos(x)"},
            {"name": "抛物线", "expr": "x^2"},
            {"name": "三次曲线", "expr": "x^3 - 3*x"},
            {"name": "指数增长", "expr": "exp(x/3)"},
            {"name": "对数曲线", "expr": "log(abs(x)+1)"},
            {"name": "阻尼振荡", "expr": "exp(-abs(x)/5) * sin(3*x)"},
            {"name": "绝对值", "expr": "abs(x)"},
            {"name": "高斯曲线", "expr": "exp(-x^2/2)"},
            {"name": "S型曲线", "expr": "1/(1+exp(-x))"},
    ]
    return {"presets": presets}