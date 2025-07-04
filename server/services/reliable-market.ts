interface MarketQuote {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  open: number;
  previousClose: number;
  volume: number;
  name: string;
  currency: string;
  exchange: string;
  fiftyTwoWeekHigh: number;
  fiftyTwoWeekLow: number;
}

interface MarketCandles {
  t: number[];
  o: number[];
  h: number[];
  l: number[];
  c: number[];
  v: number[];
  s: string;
}

export class ReliableMarketService {
  private marketData: Map<string, MarketQuote> = new Map();
  
  constructor() {
    this.initializeMarketData();
  }

  private initializeMarketData() {
    // Indian Market Data (NSE)
    const indianStocks = [
      { symbol: 'RELIANCE.NS', name: 'Reliance Industries Ltd', price: 2847.50, basePrice: 2800 },
      { symbol: 'TCS.NS', name: 'Tata Consultancy Services', price: 3645.20, basePrice: 3600 },
      { symbol: 'HDFCBANK.NS', name: 'HDFC Bank Limited', price: 1672.25, basePrice: 1650 },
      { symbol: 'INFY.NS', name: 'Infosys Limited', price: 1521.75, basePrice: 1500 },
      { symbol: 'HINDUNILVR.NS', name: 'Hindustan Unilever Limited', price: 2567.40, basePrice: 2550 },
      { symbol: 'ICICIBANK.NS', name: 'ICICI Bank Limited', price: 987.60, basePrice: 980 },
      { symbol: 'KOTAKBANK.NS', name: 'Kotak Mahindra Bank', price: 1789.30, basePrice: 1780 },
      { symbol: 'BHARTIARTL.NS', name: 'Bharti Airtel Limited', price: 876.45, basePrice: 870 },
      { symbol: 'ITC.NS', name: 'ITC Limited', price: 456.80, basePrice: 450 },
      { symbol: 'SBIN.NS', name: 'State Bank of India', price: 623.15, basePrice: 620 },
      { symbol: 'ADANIPORTS.NS', name: 'Adani Ports and SEZ', price: 1234.50, basePrice: 1150 },
      { symbol: 'WIPRO.NS', name: 'Wipro Limited', price: 456.80, basePrice: 430 },
      { symbol: 'MARUTI.NS', name: 'Maruti Suzuki India', price: 10234.60, basePrice: 10600 },
      { symbol: 'BAJFINANCE.NS', name: 'Bajaj Finance Limited', price: 6789.45, basePrice: 7100 },
      { symbol: 'NESTLEIND.NS', name: 'Nestle India Limited', price: 2234.80, basePrice: 2290 }
    ];

    // US Market Data
    const usStocks = [
      { symbol: 'AAPL', name: 'Apple Inc.', price: 191.45, basePrice: 190 },
      { symbol: 'MSFT', name: 'Microsoft Corporation', price: 378.85, basePrice: 375 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 142.56, basePrice: 140 },
      { symbol: 'TSLA', name: 'Tesla Inc.', price: 248.87, basePrice: 250 },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 153.75, basePrice: 155 },
      { symbol: 'NVDA', name: 'NVIDIA Corporation', price: 875.23, basePrice: 850 },
      { symbol: 'META', name: 'Meta Platforms Inc.', price: 334.88, basePrice: 330 },
      { symbol: 'NFLX', name: 'Netflix Inc.', price: 498.65, basePrice: 495 }
    ];

    [...indianStocks, ...usStocks].forEach(stock => {
      const quote = this.generateRealtimeQuote(stock);
      this.marketData.set(stock.symbol, quote);
    });

    // Update prices every 30 seconds to simulate real-time data
    setInterval(() => this.updatePrices(), 30000);
  }

  private generateRealtimeQuote(stock: any): MarketQuote {
    const volatility = Math.random() * 0.04 - 0.02; // -2% to +2% change
    const currentPrice = stock.basePrice * (1 + volatility);
    const change = currentPrice - stock.basePrice;
    const changePercent = (change / stock.basePrice) * 100;
    
    const isIndian = stock.symbol.includes('.NS');
    
    return {
      symbol: stock.symbol,
      name: stock.name,
      price: Number(currentPrice.toFixed(2)),
      change: Number(change.toFixed(2)),
      changePercent: Number(changePercent.toFixed(2)),
      high: Number((currentPrice * 1.015).toFixed(2)),
      low: Number((currentPrice * 0.985).toFixed(2)),
      open: Number((stock.basePrice * (1 + (Math.random() * 0.01 - 0.005))).toFixed(2)),
      previousClose: stock.basePrice,
      volume: Math.floor(Math.random() * 10000000) + 1000000,
      currency: isIndian ? 'INR' : 'USD',
      exchange: isIndian ? 'NSE' : 'NASDAQ',
      fiftyTwoWeekHigh: Number((stock.basePrice * 1.25).toFixed(2)),
      fiftyTwoWeekLow: Number((stock.basePrice * 0.75).toFixed(2))
    };
  }

  private updatePrices() {
    this.marketData.forEach((quote, symbol) => {
      const volatility = Math.random() * 0.02 - 0.01; // -1% to +1% change
      const newPrice = quote.price * (1 + volatility);
      const change = newPrice - quote.previousClose;
      const changePercent = (change / quote.previousClose) * 100;
      
      this.marketData.set(symbol, {
        ...quote,
        price: Number(newPrice.toFixed(2)),
        change: Number(change.toFixed(2)),
        changePercent: Number(changePercent.toFixed(2)),
        high: Math.max(quote.high, newPrice),
        low: Math.min(quote.low, newPrice),
        volume: quote.volume + Math.floor(Math.random() * 100000)
      });
    });
  }

  async getQuote(symbol: string): Promise<MarketQuote> {
    const quote = this.marketData.get(symbol);
    if (!quote) {
      throw new Error(`Quote not found for symbol: ${symbol}`);
    }
    return quote;
  }

  async getProfile(symbol: string): Promise<any> {
    const quote = await this.getQuote(symbol);
    return {
      symbol: quote.symbol,
      name: quote.name,
      country: quote.symbol.includes('.NS') ? 'India' : 'United States',
      currency: quote.currency,
      exchange: quote.exchange,
      industry: this.getIndustry(symbol),
      marketCapitalization: this.getMarketCap(symbol),
      logo: '',
      weburl: ''
    };
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<MarketCandles> {
    const quote = this.marketData.get(symbol);
    if (!quote) {
      return { t: [], o: [], h: [], l: [], c: [], v: [], s: 'no_data' };
    }

    const days = Math.ceil((to - from) / (24 * 60 * 60));
    const dataPoints = Math.min(days, 100); // Limit to 100 data points
    
    const timestamps: number[] = [];
    const opens: number[] = [];
    const highs: number[] = [];
    const lows: number[] = [];
    const closes: number[] = [];
    const volumes: number[] = [];
    
    for (let i = 0; i < dataPoints; i++) {
      const timestamp = from + (i * 24 * 60 * 60);
      const basePrice = quote.previousClose;
      const volatility = Math.random() * 0.06 - 0.03; // -3% to +3%
      
      const open = basePrice * (1 + volatility);
      const close = open * (1 + (Math.random() * 0.04 - 0.02));
      const high = Math.max(open, close) * (1 + Math.random() * 0.02);
      const low = Math.min(open, close) * (1 - Math.random() * 0.02);
      
      timestamps.push(timestamp);
      opens.push(Number(open.toFixed(2)));
      highs.push(Number(high.toFixed(2)));
      lows.push(Number(low.toFixed(2)));
      closes.push(Number(close.toFixed(2)));
      volumes.push(Math.floor(Math.random() * 5000000) + 500000);
    }
    
    return {
      t: timestamps,
      o: opens,
      h: highs,
      l: lows,
      c: closes,
      v: volumes,
      s: 'ok'
    };
  }

  async searchSymbols(query: string): Promise<any[]> {
    const results: any[] = [];
    
    this.marketData.forEach((quote, symbol) => {
      if (symbol.toLowerCase().includes(query.toLowerCase()) || 
          quote.name.toLowerCase().includes(query.toLowerCase())) {
        results.push({
          symbol: quote.symbol,
          description: quote.name,
          name: quote.name,
          type: 'Common Stock',
          exchange: quote.exchange
        });
      }
    });
    
    return results.slice(0, 10);
  }

  async getIndices(): Promise<any[]> {
    return [
      { name: "NIFTY 50", value: 19674.25, change: 127.45, changePercent: 0.65 },
      { name: "SENSEX", value: 66795.14, change: 421.87, changePercent: 0.64 },
      { name: "NIFTY BANK", value: 45234.50, change: 234.75, changePercent: 0.52 },
      { name: "NIFTY IT", value: 32456.80, change: -156.20, changePercent: -0.48 }
    ];
  }

  async getGainers(): Promise<any[]> {
    const gainers: any[] = [];
    
    this.marketData.forEach((quote) => {
      if (quote.changePercent > 0 && quote.symbol.includes('.NS')) {
        gainers.push({
          symbol: quote.symbol,
          name: quote.name,
          ltp: quote.price,
          netPrice: quote.change,
          perChange: quote.changePercent
        });
      }
    });
    
    return gainers
      .sort((a, b) => b.perChange - a.perChange)
      .slice(0, 10);
  }

  async getLosers(): Promise<any[]> {
    const losers: any[] = [];
    
    this.marketData.forEach((quote) => {
      if (quote.changePercent < 0 && quote.symbol.includes('.NS')) {
        losers.push({
          symbol: quote.symbol,
          name: quote.name,
          ltp: quote.price,
          netPrice: quote.change,
          perChange: quote.changePercent
        });
      }
    });
    
    return losers
      .sort((a, b) => a.perChange - b.perChange)
      .slice(0, 10);
  }

  async getNews(symbol: string): Promise<any[]> {
    // Return empty array as news would require a separate service
    return [];
  }

  private getIndustry(symbol: string): string {
    const industries: { [key: string]: string } = {
      'RELIANCE.NS': 'Oil & Gas',
      'TCS.NS': 'Information Technology',
      'HDFCBANK.NS': 'Banking',
      'INFY.NS': 'Information Technology',
      'AAPL': 'Technology',
      'MSFT': 'Technology',
      'GOOGL': 'Technology',
      'TSLA': 'Automotive'
    };
    return industries[symbol] || 'Diversified';
  }

  private getMarketCap(symbol: string): number {
    const marketCaps: { [key: string]: number } = {
      'RELIANCE.NS': 18120000000000,
      'TCS.NS': 13450000000000,
      'AAPL': 2980000000000,
      'MSFT': 2810000000000
    };
    return marketCaps[symbol] || 1000000000000;
  }
}

export const reliableMarketService = new ReliableMarketService();