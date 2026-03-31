# api/index.py - Vercel官方Python函数入口
import akshare as ak
import pandas as pd

def handler(request):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    
    try:
        # 获取查询参数
        code = request.query.get("code", "005827")
        
        # 获取基金最新持仓
        df = ak.fund_portfolio_hold_em(symbol=code)
        data = df.to_dict(orient="records")
        
        return {
            "fund": code,
            "name": f"基金{code}持仓数据",
            "holdings": data,
            "count": len(data),
            "timestamp": pd.Timestamp.now().isoformat()
        }, 200, headers
        
    except Exception as e:
        return {"error": str(e), "message": "获取基金持仓数据失败"}, 500, headers