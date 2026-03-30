"""
基金实时涨跌幅估算核心模块
"""

import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketType(Enum):
    """市场类型枚举"""
    A_SHARE = "A股"
    H_SHARE = "港股"
    US_SHARE = "美股"
    OTHER = "其他"

@dataclass
class StockHolding:
    """股票持仓数据类"""
    code: str
    name: str
    weight: float  # 占净值比例
    market: MarketType
    shares: Optional[int] = None  # 持股数
    value: Optional[float] = None  # 持仓市值
    
    def __post_init__(self):
        """数据验证"""
        if self.weight < 0 or self.weight > 100:
            raise ValueError(f"权重必须在0-100之间: {self.weight}")
        if not isinstance(self.market, MarketType):
            self.market = MarketType(self.market)

@dataclass
class StockData:
    """股票实时数据类"""
    code: str
    name: str
    current_price: float  # 当前价
    prev_close: float  # 昨收价
    change: float  # 涨跌额
    change_percent: float  # 涨跌幅
    volume: Optional[int] = None  # 成交量
    amount: Optional[float] = None  # 成交额
    update_time: Optional[str] = None  # 更新时间
    
    @property
    def is_valid(self) -> bool:
        """数据是否有效"""
        return self.prev_close > 0 and abs(self.change_percent) < 50  # 涨跌幅在合理范围内

@dataclass
class FundEstimationResult:
    """基金估算结果类"""
    fund_code: str
    fund_name: str
    estimation_time: str
    estimated_change: float  # 估算涨跌幅
    stock_weight: float  # 股票仓位
    cash_weight: float  # 现金仓位
    holdings_count: int  # 持仓股票数
    data_quality: str  # 数据质量
    contributions: List[Dict]  # 贡献详情
    raw_data: Optional[Dict] = None  # 原始数据
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'fund_code': self.fund_code,
            'fund_name': self.fund_name,
            'estimation_time': self.estimation_time,
            'estimated_change': self.estimated_change,
            'stock_weight': self.stock_weight,
            'cash_weight': self.cash_weight,
            'holdings_count': self.holdings_count,
            'data_quality': self.data_quality,
            'contributions': self.contributions
        }

class FundEstimator:
    """基金估算器核心类"""
    
    def __init__(self, config: Dict = None):
        """
        初始化估算器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.holdings_cache = {}  # 持仓缓存
        self.stock_data_cache = {}  # 股票数据缓存
        self.cache_ttl = self.config.get('cache_ttl', 300)  # 缓存有效期(秒)
        
    def get_fund_holdings(self, fund_code: str, force_refresh: bool = False) -> List[StockHolding]:
        """
        获取基金持仓
        
        Args:
            fund_code: 基金代码
            force_refresh: 是否强制刷新缓存
            
        Returns:
            持仓列表
        """
        # 检查缓存
        cache_key = f"holdings_{fund_code}"
        if not force_refresh and cache_key in self.holdings_cache:
            cache_time, holdings = self.holdings_cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                logger.info(f"使用缓存持仓数据: {fund_code}")
                return holdings
        
        try:
            # 从数据源获取持仓
            holdings = self._fetch_holdings_from_source(fund_code)
            
            # 更新缓存
            self.holdings_cache[cache_key] = (time.time(), holdings)
            
            logger.info(f"成功获取持仓: {fund_code}, 共{len(holdings)}只股票")
            return holdings
            
        except Exception as e:
            logger.error(f"获取持仓失败: {fund_code}, 错误: {e}")
            
            # 尝试使用备用数据源
            holdings = self._get_fallback_holdings(fund_code)
            if holdings:
                logger.warning(f"使用备用持仓数据: {fund_code}")
                return holdings
            
            raise
    
    def get_stock_data(self, stock_code: str, market: MarketType, force_refresh: bool = False) -> Optional[StockData]:
        """
        获取股票实时数据
        
        Args:
            stock_code: 股票代码
            market: 市场类型
            force_refresh: 是否强制刷新缓存
            
        Returns:
            股票数据，失败返回None
        """
        # 检查缓存
        cache_key = f"stock_{stock_code}"
        if not force_refresh and cache_key in self.stock_data_cache:
            cache_time, stock_data = self.stock_data_cache[cache_key]
            if time.time() - cache_time < 60:  # 股票数据缓存1分钟
                return stock_data
        
        try:
            # 从数据源获取股票数据
            stock_data = self._fetch_stock_data_from_source(stock_code, market)
            
            if stock_data and stock_data.is_valid:
                # 更新缓存
                self.stock_data_cache[cache_key] = (time.time(), stock_data)
                return stock_data
            else:
                logger.warning(f"股票数据无效: {stock_code}")
                return None
                
        except Exception as e:
            logger.error(f"获取股票数据失败: {stock_code}, 错误: {e}")
            return None
    
    def estimate_fund(self, fund_code: str, fund_name: str) -> FundEstimationResult:
        """
        估算单只基金涨跌幅
        
        Args:
            fund_code: 基金代码
            fund_name: 基金名称
            
        Returns:
            估算结果
        """
        logger.info(f"开始估算基金: {fund_name}({fund_code})")
        
        try:
            # 1. 获取持仓
            holdings = self.get_fund_holdings(fund_code)
            if not holdings:
                raise ValueError(f"无法获取基金持仓: {fund_code}")
            
            # 2. 获取股票数据
            stock_data_map = {}
            success_count = 0
            
            for holding in holdings[:self.config.get('max_holdings', 10)]:
                stock_data = self.get_stock_data(holding.code, holding.market)
                
                if stock_data:
                    stock_data_map[holding.code] = stock_data
                    success_count += 1
                else:
                    # 使用默认数据
                    stock_data_map[holding.code] = StockData(
                        code=holding.code,
                        name=holding.name,
                        current_price=0,
                        prev_close=1,
                        change=0,
                        change_percent=0
                    )
                
                # 避免请求过快
                time.sleep(self.config.get('request_interval', 0.05))
            
            # 3. 计算估算
            result = self._calculate_estimation(
                fund_code, fund_name, holdings, stock_data_map, success_count
            )
            
            logger.info(f"基金估算完成: {fund_name}, 结果: {result.estimated_change:+.4f}%")
            return result
            
        except Exception as e:
            logger.error(f"基金估算失败: {fund_code}, 错误: {e}")
            raise
    
    def estimate_multiple_funds(self, funds: List[Dict]) -> List[FundEstimationResult]:
        """
        估算多只基金
        
        Args:
            funds: 基金列表，每个元素包含code和name
            
        Returns:
            估算结果列表
        """
        results = []
        
        for fund in funds:
            try:
                result = self.estimate_fund(fund['code'], fund['name'])
                results.append(result)
            except Exception as e:
                logger.error(f"估算基金失败: {fund['code']}, 跳过")
                continue
        
        return results
    
    def _fetch_holdings_from_source(self, fund_code: str) -> List[StockHolding]:
        """
        从数据源获取持仓（需要子类实现）
        
        Args:
            fund_code: 基金代码
            
        Returns:
            持仓列表
        """
        # 这里应该调用具体的数据源实现
        # 例如: return self.data_source.get_fund_holdings(fund_code)
        raise NotImplementedError("子类必须实现此方法")
    
    def _fetch_stock_data_from_source(self, stock_code: str, market: MarketType) -> Optional[StockData]:
        """
        从数据源获取股票数据（需要子类实现）
        
        Args:
            stock_code: 股票代码
            market: 市场类型
            
        Returns:
            股票数据
        """
        # 这里应该调用具体的数据源实现
        # 例如: return self.data_source.get_stock_data(stock_code, market)
        raise NotImplementedError("子类必须实现此方法")
    
    def _get_fallback_holdings(self, fund_code: str) -> List[StockHolding]:
        """
        获取备用持仓数据
        
        Args:
            fund_code: 基金代码
            
        Returns:
            备用持仓列表
        """
        # 这里可以返回模拟数据或从本地文件读取
        # 实际实现应根据具体需求调整
        return []
    
    def _calculate_estimation(self, fund_code: str, fund_name: str, 
                            holdings: List[StockHolding], 
                            stock_data_map: Dict[str, StockData],
                            success_count: int) -> FundEstimationResult:
        """
        计算基金估算
        
        Args:
            fund_code: 基金代码
            fund_name: 基金名称
            holdings: 持仓列表
            stock_data_map: 股票数据映射
            success_count: 成功获取的股票数据数量
            
        Returns:
            估算结果
        """
        # 计算总权重
        total_weight = sum(h.weight for h in holdings)
        
        # 计算加权涨跌
        weighted_change = 0
        contributions = []
        
        for holding in holdings:
            stock_data = stock_data_map.get(holding.code)
            if not stock_data:
                continue
            
            # 计算贡献
            contribution = holding.weight * stock_data.change_percent / 100
            weighted_change += contribution
            
            contributions.append({
                'stock': f"{holding.name}({holding.code})",
                'weight': holding.weight,
                'stock_change': stock_data.change_percent,
                'contribution': contribution,
                'current_price': stock_data.current_price,
                'change': stock_data.change
            })
        
        # 考虑现金仓位
        cash_weight = max(0, 100 - total_weight)
        cash_return_rate = self.config.get('cash_return_rate', 0.0)
        cash_contribution = cash_weight * cash_return_rate / 100
        
        total_estimated_change = weighted_change + cash_contribution
        
        # 数据质量评估
        data_quality = f"{success_count}/{len(holdings)}"
        
        # 创建结果对象
        result = FundEstimationResult(
            fund_code=fund_code,
            fund_name=fund_name,
            estimation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            estimated_change=total_estimated_change,
            stock_weight=total_weight,
            cash_weight=cash_weight,
            holdings_count=len(holdings),
            data_quality=data_quality,
            contributions=sorted(contributions, key=lambda x: abs(x['contribution']), reverse=True)[:5]
        )
        
        return result
    
    def clear_cache(self):
        """清空缓存"""
        self.holdings_cache.clear()
        self.stock_data_cache.clear()
        logger.info("缓存已清空")

class TiantianEastmoneyEstimator(FundEstimator):
    """天天基金网 + 东方财富网估算器"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        # 这里可以初始化具体的数据源客户端
        # 例如: self.tiantian_client = TiantianClient()
        # 例如: self.eastmoney_client = EastmoneyClient()
    
    def _fetch_holdings_from_source(self, fund_code: str) -> List[StockHolding]:
        """从天天基金网获取持仓"""
        # 这里实现具体的天天基金网API调用
        # 实际实现需要处理网络请求、HTML解析等
        
        # 示例: 使用模拟数据
        return self._get_mock_holdings(fund_code)
    
    def _fetch_stock_data_from_source(self, stock_code: str, market: MarketType) -> Optional[StockData]:
        """从东方财富网获取股票数据"""
        # 这里实现具体的东方财富网API调用
        
        # 示例: 使用模拟数据
        return self._get_mock_stock_data(stock_code, market)
    
    def _get_mock_holdings(self, fund_code: str) -> List[StockHolding]:
        """获取模拟持仓数据"""
        # 根据基金代码返回不同的模拟数据
        mock_data = {
            '006228': [  # 中欧医疗
                StockHolding(code='603259', name='药明康德', weight=8.5, market=MarketType.A_SHARE),
                StockHolding(code='300759', name='康龙化成', weight=7.2, market=MarketType.A_SHARE),
                StockHolding(code='300347', name='泰格医药', weight=6.8, market=MarketType.A_SHARE),
                StockHolding(code='002821', name='凯莱英', weight=6.3, market=MarketType.A_SHARE),
                StockHolding(code='300363', name='博腾股份', weight=5.9, market=MarketType.A_SHARE),
            ],
            '005827': [  # 易方达蓝筹
                StockHolding(code='600519', name='贵州茅台', weight=9.8, market=MarketType.A_SHARE),
                StockHolding(code='00700', name='腾讯控股', weight=9.5, market=MarketType.H_SHARE),
                StockHolding(code='600036', name='招商银行', weight=9.2, market=MarketType.A_SHARE),
                StockHolding(code='000858', name='五粮液', weight=8.7, market=MarketType.A_SHARE),
                StockHolding(code='00388', name='香港交易所', weight=8.3, market=MarketType.H_SHARE),
            ]
        }
        
        return mock_data.get(fund_code, [])
    
    def _get_mock_stock_data(self, stock_code: str, market: MarketType) -> StockData:
        """获取模拟股票数据"""
        import random
        
        # 生成随机涨跌幅（-5% 到 +5%）
        change_percent = random.uniform(-5, 5)
        prev_close = random.uniform(10, 500)
        change = prev_close * change_percent / 100
        current_price = prev_close + change
        
        return StockData(
            code=stock_code,
            name=f"股票{stock_code}",
            current_price=current_price,
            prev_close=prev_close,
            change=change,
            change_percent=change_percent,
            update_time=datetime.now().strftime('%H:%M:%S')
        )

# 使用示例
if __name__ == "__main__":
    # 创建估算器
    config = {
        'max_holdings': 10,
        'cash_return_rate': 0.0,
        'request_interval': 0.1,
        'cache_ttl': 300
    }
    
    estimator = TiantianEastmoneyEstimator(config)
    
    # 估算单只基金
    try:
        result = estimator.estimate_fund("006228", "中欧医疗创新股票A")
        print(f"估算结果: {result.estimated_change:+.4f}%")
        print(f"数据质量: {result.data_quality}")
    except Exception as e:
        print(f"估算失败: {e}")
    
    # 估算多只基金
    funds = [
        {'code': '006228', 'name': '中欧医疗创新股票A'},
        {'code': '005827', 'name': '易方达蓝筹精选混合'}
    ]
    
    results = estimator.estimate_multiple_funds(funds)
    for result in results:
        print(f"{result.fund_name}: {result.estimated_change:+.4f}%")