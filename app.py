<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Analysis Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid #e1e4e8;
            margin-bottom: 30px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .logo h1 {
            font-size: 24px;
            color: #1a73e8;
        }
        
        .logo-icon {
            color: #1a73e8;
            font-size: 28px;
        }
        
        nav ul {
            display: flex;
            list-style: none;
            gap: 25px;
        }
        
        nav a {
            text-decoration: none;
            color: #5f6368;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        nav a:hover, nav a.active {
            color: #1a73e8;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 30px;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 25px;
            margin-bottom: 25px;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eaecef;
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 600;
            color: #1a232e;
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .stock-price {
            font-size: 32px;
            font-weight: 700;
            color: #1a232e;
        }
        
        .stock-change {
            font-size: 16px;
            font-weight: 600;
            color: #0f9d58;
            background: #e6f4ea;
            padding: 5px 10px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .stock-change.negative {
            color: #d93025;
            background: #fce8e6;
        }
        
        .stock-meta {
            color: #5f6368;
            font-size: 14px;
            margin-bottom: 25px;
        }
        
        .time-filters {
            display: flex;
            background: #f1f3f4;
            border-radius: 6px;
            padding: 4px;
            margin-bottom: 25px;
        }
        
        .time-filter {
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .time-filter.active {
            background: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            font-weight: 500;
        }
        
        .chart-placeholder {
            height: 250px;
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #6c757d;
            margin-bottom: 20px;
        }
        
        .key-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #f1f3f4;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            color: #5f6368;
            font-size: 14px;
        }
        
        .metric-value {
            font-weight: 600;
            color: #1a232e;
        }
        
        .research-sections {
            margin-top: 30px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #1a232e;
            padding-bottom: 10px;
            border-bottom: 1px solid #eaecef;
        }
        
        .section-content {
            color: #5f6368;
            line-height: 1.7;
        }
        
        .section-content p {
            margin-bottom: 15px;
        }
        
        .btn {
            display: inline-block;
            background: #1a73e8;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: background 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover {
            background: #0d62c9;
        }
        
        .btn-outline {
            background: transparent;
            border: 1px solid #1a73e8;
            color: #1a73e8;
        }
        
        .btn-outline:hover {
            background: #f0f7ff;
        }
        
        .actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        footer {
            text-align: center;
            padding: 30px 0;
            margin-top: 40px;
            border-top: 1px solid #e1e4e8;
            color: #5f6368;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .key-metrics {
                grid-template-columns: 1fr;
            }
            
            nav ul {
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <i class="fas fa-chart-line logo-icon"></i>
                <h1>MarketAnalytics Pro</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="#" class="active">Dashboard</a></li>
                    <li><a href="#">Research</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">News</a></li>
                    <li><a href="#">Settings</a></li>
                </ul>
            </nav>
        </header>
        
        <div class="dashboard">
            <div class="main-content">
                <div class="card">
                    <div class="stock-header">
                        <div>
                            <h2>NIFTY 50 Index</h2>
                            <div class="stock-meta">9 Oct, 3:30 pm IST • Disclaimer</div>
                        </div>
                        <div>
                            <div class="stock-price">3,060.20</div>
                            <div class="stock-change">
                                <i class="fas fa-arrow-up"></i>
                                +33.00 (1.09%)
                            </div>
                        </div>
                    </div>
                    
                    <div class="time-filters">
                        <div class="time-filter active">1D</div>
                        <div class="time-filter">5D</div>
                        <div class="time-filter">1M</div>
                        <div class="time-filter">6M</div>
                        <div class="time-filter">YTD</div>
                        <div class="time-filter">1Y</div>
                        <div class="time-filter">5Y</div>
                        <div class="time-filter">Max</div>
                    </div>
                    
                    <div class="chart-placeholder">
                        <div style="text-align: center;">
                            <i class="fas fa-chart-area" style="font-size: 48px; margin-bottom: 10px; opacity: 0.5;"></i>
                            <p>Interactive Chart Area</p>
                            <p style="font-size: 12px; margin-top: 5px;">3,070 | 3,060 | 3,050 | 3,040 | 3,030 | 3,020</p>
                            <p style="font-size: 12px; margin-top: 10px;">11:00 am | 1:00 pm | 3:00 pm</p>
                        </div>
                    </div>
                    
                    <div class="key-metrics">
                        <div class="metric">
                            <span class="metric-label">Previous Close</span>
                            <span class="metric-value">3,027.20</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Open</span>
                            <span class="metric-value">3,034.00</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">High</span>
                            <span class="metric-value">3,066.00</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Low</span>
                            <span class="metric-value">3,020.00</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Mkt Cap</span>
                            <span class="metric-value">11.08 LCr</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">P/E Ratio</span>
                            <span class="metric-value">22.47</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">52-wk High</span>
                            <span class="metric-value">4,494.90</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Dividend Yield</span>
                            <span class="metric-value">1.99%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Qtrly Div Amt</span>
                            <span class="metric-value">15.22</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">52-wk Low</span>
                            <span class="metric-value">2,866.60</span>
                        </div>
                    </div>
                </div>
                
                <div class="research-sections">
                    <div class="section">
                        <h3 class="section-title">Technical Analysis</h3>
                        <div class="section-content">
                            <p>The NIFTY 50 index shows a bullish trend with a strong support level at 3,020. The index has broken through the resistance at 3,050 and is now testing the 3,070 level.</p>
                            <p>RSI indicator is at 62, suggesting there is still room for upward movement before reaching overbought territory. The moving averages (50-day and 200-day) are in a bullish alignment.</p>
                            <div class="actions">
                                <a href="#" class="btn">View Full Report</a>
                                <a href="#" class="btn btn-outline">Download PDF</a>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h3 class="section-title">Fundamental Analysis</h3>
                        <div class="section-content">
                            <p>The current P/E ratio of 22.47 is slightly above the 5-year historical average of 21.3, indicating a modest premium valuation. Market capitalization stands at 11.08 Lakh Crore.</p>
                            <p>Dividend yield of 1.99% is competitive compared to fixed income alternatives in the current interest rate environment. Quarterly dividend amount of 15.22 represents a stable payout ratio.</p>
                            <div class="actions">
                                <a href="#" class="btn">View Full Report</a>
                                <a href="#" class="btn btn-outline">Download PDF</a>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h3 class="section-title">Risk Assessment</h3>
                        <div class="section-content">
                            <p>The index is currently trading 32% below its 52-week high, indicating significant recovery potential but also highlighting the volatility experienced over the past year.</p>
                            <p>Key risk factors include global macroeconomic conditions, currency fluctuations, and geopolitical tensions that could impact market sentiment.</p>
                            <div class="actions">
                                <a href="#" class="btn">View Full Report</a>
                                <a href="#" class="btn btn-outline">Download PDF</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Watchlist</h3>
                        <a href="#">Manage</a>
                    </div>
                    <div class="watchlist">
                        <div class="metric">
                            <span class="metric-label">RELIANCE</span>
                            <span class="metric-value">2,450.50 <span style="color: #0f9d58; font-size: 12px;">+1.2%</span></span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">TCS</span>
                            <span class="metric-value">3,215.75 <span style="color: #0f9d58; font-size: 12px;">+0.8%</span></span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">HDFC BANK</span>
                            <span class="metric-value">1,550.25 <span style="color: #d93025; font-size: 12px;">-0.5%</span></span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">INFOSYS</span>
                            <span class="metric-value">1,675.40 <span style="color: #0f9d58; font-size: 12px;">+1.7%</span></span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">News & Updates</h3>
                        <a href="#">View All</a>
                    </div>
                    <div class="news">
                        <div class="metric">
                            <span class="metric-label">RBI Policy Decision</span>
                            <span class="metric-value" style="font-size: 12px;">2h ago</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Q2 Earnings Reports</span>
                            <span class="metric-value" style="font-size: 12px;">5h ago</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Global Market Trends</span>
                            <span class="metric-value" style="font-size: 12px;">1d ago</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Sector Rotation Analysis</span>
                            <span class="metric-value" style="font-size: 12px;">2d ago</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Quick Actions</h3>
                    </div>
                    <div class="actions" style="flex-direction: column;">
                        <a href="#" class="btn" style="text-align: center; margin-bottom: 10px;">Create Alert</a>
                        <a href="#" class="btn btn-outline" style="text-align: center; margin-bottom: 10px;">Export Data</a>
                        <a href="#" class="btn btn-outline" style="text-align: center;">Compare Stocks</a>
                    </div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Disclaimer: This data is for informational purposes only and should not be considered as financial advice.</p>
            <p>MarketAnalytics Pro &copy; 2025. All rights reserved.</p>
        </footer>
    </div>

    <script>
        // Simple interactivity for time filters
        document.querySelectorAll('.time-filter').forEach(filter => {
            filter.addEventListener('click', function() {
                document.querySelectorAll('.time-filter').forEach(f => f.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Simulate loading state for chart
        const chart = document.querySelector('.chart-placeholder');
        chart.addEventListener('click', function() {
            this.innerHTML = '<div style="text-align: center;"><div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid #1a73e8; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 0 auto 15px;"></div><p>Loading advanced chart...</p></div>';
            
            setTimeout(() => {
                chart.innerHTML = '<div style="text-align: center;"><i class="fas fa-chart-line" style="font-size: 48px; margin-bottom: 10px; color: #1a73e8;"></i><p>Advanced Chart Loaded</p><p style="font-size: 12px; margin-top: 10px;">Interactive features enabled</p></div>';
            }, 1500);
        });
    </script>
</body>
</html>