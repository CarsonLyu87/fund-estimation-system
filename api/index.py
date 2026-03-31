# api/index.py
import akshare as ak

# 必须写在最外层，不能缩进！！！
def handler(request):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    }

    try:
        code = request.query.get("code", "005827")
        df = ak.fund_portfolio_hold_em(symbol=code)
        data = df.to_dict(orient="records")

        return {
            "fund": code,
            "name": "易方达蓝筹精选混合",
            "hold": data
        }, 200, headers

    except Exception as e:
        return {"error": str(e)}, 500, headers