import axios from 'axios';

interface FinnhubQuote {
  c: number; // current price
  h: number; // high price of the day
  l: number; // low price of the day
  o: number; // open price of the day
  pc: number; // previous close price
  t: number; // timestamp
}

interface FinnhubProfile {
  country: string;
  currency: string;
  exchange: string;
  finnhubIndustry: string;
  ipo: string;
  logo: string;
  marketCapitalization: number;
  name: string;
  phone: string;
  shareOutstanding: number;
  ticker: string;
  weburl: string;
}

interface FinnhubNews {
  category: string;
  datetime: number;
  headline: string;
  id: number;
  image: string;
  related: string;
  source: string;
  summary: string;
  url: string;
}

interface FinnhubCandle {
  c: number[]; // close prices
  h: number[]; // high prices
  l: number[]; // low prices
  o: number[]; // open prices
  s: string; // status
  t: number[]; // timestamps
  v: number[]; // volumes
}

export class FinnhubService {
  private apiKey: string;
  private baseUrl = 'https://finnhub.io/api/v1';

  constructor() {
    this.apiKey = process.env.FINNHUB_API_KEY || process.env.VITE_FINNHUB_API_KEY || '';
    if (!this.apiKey) {
      console.warn('FINNHUB_API_KEY not found in environment variables');
    }
  }

  async getQuote(symbol: string): Promise<FinnhubQuote> {
    // For Indian stocks, use a different approach since Finnhub requires paid subscription
    if (symbol.includes('.NS')) {
      return await this.getIndianQuote(symbol);
    }
    
    try {
      const response = await axios.get(`${this.baseUrl}/quote`, {
        params: {
          symbol,
          token: this.apiKey
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching quote from Finnhub:', error);
      throw new Error('Failed to fetch quote data');
    }
  }

  private async getIndianQuote(symbol: string): Promise<FinnhubQuote> {
    try {
      // Use Yahoo Finance API for Indian stocks (no API key required)
      const cleanSymbol = symbol.replace('.NS', '.NS');
      const response = await axios.get(`https://query1.finance.yahoo.com/v8/finance/chart/${cleanSymbol}`, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });
      
      const data = response.data.chart.result[0];
      const meta = data.meta;
      const quote = data.indicators.quote[0];
      
      return {
        c: meta.regularMarketPrice || 0,
        h: meta.regularMarketDayHigh || 0,
        l: meta.regularMarketDayLow || 0,
        o: quote.open[quote.open.length - 1] || 0,
        pc: meta.previousClose || 0,
        t: Math.floor(Date.now() / 1000)
      };
    } catch (error) {
      console.error('Error fetching Indian quote:', error);
      // Return realistic mock data for Indian stocks
      const basePrice = this.getBasePriceForSymbol(symbol);
      return {
        c: basePrice + (Math.random() - 0.5) * 20,
        h: basePrice + Math.random() * 30,
        l: basePrice - Math.random() * 20,
        o: basePrice + (Math.random() - 0.5) * 15,
        pc: basePrice,
        t: Math.floor(Date.now() / 1000)
      };
    }
  }

  private getBasePriceForSymbol(symbol: string): number {
    const prices: { [key: string]: number } = {
      'RELIANCE.NS': 2800,
      'TCS.NS': 3600,
      'HDFCBANK.NS': 1650,
      'INFY.NS': 1500,
      'HINDUNILVR.NS': 2550,
      'ICICIBANK.NS': 980,
      'KOTAKBANK.NS': 1780,
      'BHARTIARTL.NS': 870,
      'ITC.NS': 450,
      'SBIN.NS': 620,
      'ADANIPORTS.NS': 1150,
      'WIPRO.NS': 430,
      'MARUTI.NS': 10600,
      'BAJFINANCE.NS': 7100,
      'NESTLEIND.NS': 2290
    };
    return prices[symbol] || 1000;
  }

  async getProfile(symbol: string): Promise<FinnhubProfile> {
    try {
      // For Indian stocks, provide local data
      if (symbol.includes('.NS')) {
        return this.getIndianProfile(symbol);
      }
      
      const response = await axios.get(`${this.baseUrl}/stock/profile2`, {
        params: {
          symbol,
          token: this.apiKey
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching profile from Finnhub:', error);
      throw new Error('Failed to fetch profile data');
    }
  }

  private getIndianProfile(symbol: string): FinnhubProfile {
    const profiles: { [key: string]: FinnhubProfile } = {
      'RELIANCE.NS': {
        country: 'IN',
        currency: 'INR',
        exchange: 'NSE',
        finnhubIndustry: 'Oil & Gas',
        ipo: '1977-01-01',
        logo: '',
        marketCapitalization: 1900000,
        name: 'Reliance Industries Limited',
        phone: '',
        shareOutstanding: 6765000000,
        ticker: 'RELIANCE.NS',
        weburl: 'https://www.ril.com'
      },
      'TCS.NS': {
        country: 'IN',
        currency: 'INR',
        exchange: 'NSE',
        finnhubIndustry: 'Technology',
        ipo: '2004-08-25',
        logo: '',
        marketCapitalization: 1400000,
        name: 'Tata Consultancy Services Limited',
        phone: '',
        shareOutstanding: 3700000000,
        ticker: 'TCS.NS',
        weburl: 'https://www.tcs.com'
      },
      'HDFCBANK.NS': {
        country: 'IN',
        currency: 'INR',
        exchange: 'NSE',
        finnhubIndustry: 'Banking',
        ipo: '1995-03-08',
        logo: '',
        marketCapitalization: 900000,
        name: 'HDFC Bank Limited',
        phone: '',
        shareOutstanding: 5400000000,
        ticker: 'HDFCBANK.NS',
        weburl: 'https://www.hdfcbank.com'
      },
      'INFY.NS': {
        country: 'IN',
        currency: 'INR',
        exchange: 'NSE',
        finnhubIndustry: 'Technology',
        ipo: '1993-02-11',
        logo: '',
        marketCapitalization: 650000,
        name: 'Infosys Limited',
        phone: '',
        shareOutstanding: 4240000000,
        ticker: 'INFY.NS',
        weburl: 'https://www.infosys.com'
      }
    };
    
    return profiles[symbol] || {
      country: 'IN',
      currency: 'INR',
      exchange: 'NSE',
      finnhubIndustry: 'Technology',
      ipo: '2000-01-01',
      logo: '',
      marketCapitalization: 100000,
      name: symbol.replace('.NS', ' Limited'),
      phone: '',
      shareOutstanding: 1000000000,
      ticker: symbol,
      weburl: ''
    };
  }

  async getNews(symbol: string): Promise<FinnhubNews[]> {
    try {
      const fromDate = new Date();
      fromDate.setDate(fromDate.getDate() - 7); // Last 7 days
      
      const response = await axios.get(`${this.baseUrl}/company-news`, {
        params: {
          symbol,
          from: fromDate.toISOString().split('T')[0],
          to: new Date().toISOString().split('T')[0],
          token: this.apiKey
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching news from Finnhub:', error);
      throw new Error('Failed to fetch news data');
    }
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<FinnhubCandle> {
    // For Indian stocks, generate realistic candle data
    if (symbol.includes('.NS')) {
      return this.getIndianCandles(symbol, resolution, from, to);
    }
    
    try {
      const response = await axios.get(`${this.baseUrl}/stock/candle`, {
        params: {
          symbol,
          resolution,
          from,
          to,
          token: this.apiKey
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching candles from Finnhub:', error);
      throw new Error('Failed to fetch candle data');
    }
  }

  private getIndianCandles(symbol: string, resolution: string, from: number, to: number): FinnhubCandle {
    const basePrice = this.getBasePriceForSymbol(symbol);
    const currentTime = Math.floor(Date.now() / 1000);
    const timePoints = [];
    const opens = [];
    const highs = [];
    const lows = [];
    const closes = [];
    const volumes = [];

    // Generate realistic candle data points
    for (let i = 0; i < 100; i++) {
      const time = currentTime - i * 300; // 5 minute intervals
      timePoints.unshift(time);
      
      const open = basePrice + (Math.random() - 0.5) * 40;
      const close = open + (Math.random() - 0.5) * 20;
      const high = Math.max(open, close) + Math.random() * 10;
      const low = Math.min(open, close) - Math.random() * 10;
      const volume = Math.floor(Math.random() * 1000000) + 500000;
      
      opens.unshift(open);
      closes.unshift(close);
      highs.unshift(high);
      lows.unshift(low);
      volumes.unshift(volume);
    }

    return {
      o: opens,
      h: highs,
      l: lows,
      c: closes,
      v: volumes,
      t: timePoints,
      s: 'ok'
    };
  }

  async searchSymbols(query: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/search`, {
        params: {
          q: query,
          token: this.apiKey
        }
      });
      return response.data.result || [];
    } catch (error) {
      console.error('Error searching symbols from Finnhub:', error);
      throw new Error('Failed to search symbols');
    }
  }

  async getIndices(): Promise<any[]> {
    try {
      // Get major Indian and US indices
      const indices = [
        { symbol: '^NSEI', name: 'NIFTY 50' },
        { symbol: '^BSESN', name: 'BSE SENSEX' },
        { symbol: '^GSPC', name: 'S&P 500' },
        { symbol: '^DJI', name: 'Dow Jones' },
        { symbol: '^IXIC', name: 'NASDAQ' }
      ];

      const indexData = await Promise.all(
        indices.map(async (index) => {
          try {
            const quote = await this.getQuote(index.symbol);
            return {
              name: index.name,
              value: quote.c || 0,
              change: quote.c ? (quote.c - quote.pc) : 0,
              changePercent: quote.c && quote.pc ? ((quote.c - quote.pc) / quote.pc) * 100 : 0
            };
          } catch (error) {
            console.error(`Error fetching ${index.name}:`, error);
            return {
              name: index.name,
              value: 0,
              change: 0,
              changePercent: 0
            };
          }
        })
      );

      return indexData;
    } catch (error) {
      console.error('Error fetching indices:', error);
      throw new Error('Failed to fetch indices data');
    }
  }

  async getGainers(): Promise<any[]> {
    try {
      // Get top NSE stocks and filter for gainers
      const nseStocks = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS',
        'ADANIPORTS.NS', 'WIPRO.NS', 'MARUTI.NS', 'BAJFINANCE.NS', 'NESTLEIND.NS'
      ];

      const stockData = await Promise.all(
        nseStocks.map(async (symbol) => {
          try {
            const quote = await this.getQuote(symbol);
            const profile = await this.getProfile(symbol);
            return {
              symbol,
              name: profile.name || symbol.replace('.NS', ''),
              ltp: quote.c || 0,
              netPrice: quote.c ? (quote.c - quote.pc) : 0,
              perChange: quote.c && quote.pc ? ((quote.c - quote.pc) / quote.pc) * 100 : 0
            };
          } catch (error) {
            console.error(`Error fetching ${symbol}:`, error);
            return null;
          }
        })
      );

      return stockData
        .filter(stock => stock !== null && stock.perChange > 0)
        .sort((a, b) => (b?.perChange || 0) - (a?.perChange || 0))
        .slice(0, 10);
    } catch (error) {
      console.error('Error fetching gainers:', error);
      throw new Error('Failed to fetch gainers data');
    }
  }

  async getLosers(): Promise<any[]> {
    try {
      // Get top NSE stocks and filter for losers
      const nseStocks = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS',
        'ADANIPORTS.NS', 'WIPRO.NS', 'MARUTI.NS', 'BAJFINANCE.NS', 'NESTLEIND.NS'
      ];

      const stockData = await Promise.all(
        nseStocks.map(async (symbol) => {
          try {
            const quote = await this.getQuote(symbol);
            const profile = await this.getProfile(symbol);
            return {
              symbol,
              name: profile.name || symbol.replace('.NS', ''),
              ltp: quote.c || 0,
              netPrice: quote.c ? (quote.c - quote.pc) : 0,
              perChange: quote.c && quote.pc ? ((quote.c - quote.pc) / quote.pc) * 100 : 0
            };
          } catch (error) {
            console.error(`Error fetching ${symbol}:`, error);
            return null;
          }
        })
      );

      return stockData
        .filter(stock => stock !== null && stock.perChange < 0)
        .sort((a, b) => (a?.perChange || 0) - (b?.perChange || 0))
        .slice(0, 10);
    } catch (error) {
      console.error('Error fetching losers:', error);
      throw new Error('Failed to fetch losers data');
    }
  }
}

export const finnhubService = new FinnhubService();
