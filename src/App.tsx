import React, { useState } from 'react'
import './App.css'

function App() {
  const [fundCode, setFundCode] = useState('005827')
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const fetchFundData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/index.py?code=${fundCode}`)
      
      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
      }
      
      const result = await response.json()
      setData(result)
    } catch (err: any) {
      setError(err.message || '获取数据失败')
      console.error('API调用错误:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📊 基金持仓数据查询系统</h1>
        <p>React前端 + Python API混合应用</p>
      </header>

      <main className="main">
        <div className="card">
          <h2>查询基金持仓</h2>
          
          <div className="input-group">
            <label htmlFor="fundCode">基金代码:</label>
            <input
              id="fundCode"
              type="text"
              value={fundCode}
              onChange={(e) => setFundCode(e.target.value)}
              placeholder="例如: 005827"
            />
            <button 
              onClick={fetchFundData}
              disabled={loading}
              className="query-button"
            >
              {loading ? '查询中...' : '查询持仓数据'}
            </button>
          </div>

          {error && (
            <div className="error">
              ❌ 错误: {error}
            </div>
          )}

          {data && !error && (
            <div className="result">
              <div className="success">
                ✅ 查询成功！
              </div>
              
              <div className="info">
                <p><strong>基金代码:</strong> {data.fund}</p>
                <p><strong>基金名称:</strong> {data.name}</p>
                <p><strong>持仓数量:</strong> {data.count} 只股票</p>
                <p><strong>更新时间:</strong> {data.timestamp}</p>
              </div>

              {data.holdings && data.holdings.length > 0 && (
                <div className="holdings">
                  <h3>持仓详情 (前5条):</h3>
                  <table>
                    <thead>
                      <tr>
                        <th>股票代码</th>
                        <th>股票名称</th>
                        <th>持仓比例</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.holdings.slice(0, 5).map((item: any, index: number) => (
                        <tr key={index}>
                          <td>{item.symbol || 'N/A'}</td>
                          <td>{item.name || 'N/A'}</td>
                          <td>{item.proportion || 'N/A'}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          <div className="info-card">
            <h3>📋 系统说明</h3>
            <p>这是一个 <strong>React前端 + Python API</strong> 混合应用：</p>
            <ul>
              <li><strong>前端</strong>: React + Vite (静态构建)</li>
              <li><strong>后端</strong>: Python API (AKShare数据)</li>
              <li><strong>部署</strong>: Vercel混合部署</li>
            </ul>
            <p>✅ 此配置解决了Vercel Python Entrypoint报错问题！</p>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Vercel混合部署解决方案 | React + Python API</p>
      </footer>
    </div>
  )
}

export default App