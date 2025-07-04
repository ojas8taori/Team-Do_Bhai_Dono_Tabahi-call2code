import axios from 'axios';

interface YahooQuote {
  symbol: string;
  regularMarketPrice: number;
  regularMarketChange: number;
  regularMarketChangePercent: number;
  regularMarketPreviousClose: number;
  regularMarketOpen: number;
  regularMarketDayHigh: number;
  regularMarketDayLow: number;
  regularMarketVolume: number;
  marketCap: number;
  trailingPE: number;
  fiftyTwoWeekHigh: number;
  fiftyTwoWeekLow: number;
  longName: string;
  currency: string;
  exchange: string;
}

interface YahooSearchResult {
  symbol: string;
  shortname: string;
  longname: string;
  exchDisp: string;
  typeDisp: string;
}

interface YahooChart {
  timestamp: number[];
  indicators: {
    quote: [{
      open: number[];
      high: number[];
      low: number[];
      close: number[];
      volume: number[];
    }];
  };
}

export class YahooFinanceService {
  private baseUrl = 'https://query1.finance.yahoo.com/v8/finance/chart';
  private quotesUrl = 'https://query1.finance.yahoo.com/v7/finance/quote';
  private searchUrl = 'https://query1.finance.yahoo.com/v1/finance/search';
  private screamUrl = 'https://query1.finance.yahoo.com/v1/finance/screener';

  private headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
  };

  async getQuote(symbol: string): Promise<any> {
    try {
      const response = await axios.get(`${this.quotesUrl}?symbols=${symbol}`, {
        headers: this.headers
      });
      
      const quote = response.data.quoteResponse.result[0];
      if (!quote) {
        throw new Error('Quote not found');
      }

      return {
        symbol: quote.symbol,
        price: quote.regularMarketPrice || 0,
        change: quote.regularMarketChange || 0,
        changePercent: quote.regularMarketChangePercent || 0,
        high: quote.regularMarketDayHigh || 0,
        low: quote.regularMarketDayLow || 0,
        open: quote.regularMarketOpen || 0,
        previousClose: quote.regularMarketPreviousClose || 0,
        volume: quote.regularMarketVolume || 0,
        marketCap: quote.marketCap || 0,
        trailingPE: quote.trailingPE || 0,
        fiftyTwoWeekHigh: quote.fiftyTwoWeekHigh || 0,
        fiftyTwoWeekLow: quote.fiftyTwoWeekLow || 0,
        name: quote.longName || quote.shortName || '',
        currency: quote.currency || 'USD',
        exchange: quote.fullExchangeName || quote.exchange || ''
      };
    } catch (error) {
      console.error('Error fetching quote from Yahoo Finance:', error);
      throw new Error('Failed to fetch quote data');
    }
  }

  async getProfile(symbol: string): Promise<any> {
    try {
      const response = await axios.get(`${this.quotesUrl}?symbols=${symbol}`, {
        headers: this.headers
      });
      
      const quote = response.data.quoteResponse.result[0];
      if (!quote) {
        throw new Error('Profile not found');
      }

      return {
        symbol: quote.symbol,
        name: quote.longName || quote.shortName || '',
        country: quote.country || '',
        currency: quote.currency || 'USD',
        exchange: quote.fullExchangeName || quote.exchange || '',
        industry: quote.sector || '',
        marketCapitalization: quote.marketCap || 0,
        logo: '',
        weburl: ''
      };
    } catch (error) {
      console.error('Error fetching profile from Yahoo Finance:', error);
      throw new Error('Failed to fetch profile data');
    }
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<any> {
    try {
      let interval = '1d';
      switch (resolution) {
        case '5': interval = '5m'; break;
        case '15': interval = '15m'; break;
        case '30': interval = '30m'; break;
        case '60': interval = '1h'; break;
        case 'D': interval = '1d'; break;
        default: interval = '1d';
      }

      const response = await axios.get(`${this.baseUrl}/${symbol}`, {
        params: {
          period1: from,
          period2: to,
          interval: interval,
          includePrePost: false,
          events: 'div,splits'
        },
        headers: this.headers
      });

      const chart = response.data.chart.result[0];
      if (!chart || !chart.timestamp) {
        return { t: [], o: [], h: [], l: [], c: [], v: [], s: 'no_data' };
      }

      const quote = chart.indicators.quote[0];
      
      return {
        t: chart.timestamp,
        o: quote.open,
        h: quote.high,
        l: quote.low,
        c: quote.close,
        v: quote.volume,
        s: 'ok'
      };
    } catch (error) {
      console.error('Error fetching candles from Yahoo Finance:', error);
      return { t: [], o: [], h: [], l: [], c: [], v: [], s: 'no_data' };
    }
  }

  async searchSymbols(query: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.searchUrl}`, {
        params: { q: query },
        headers: this.headers
      });

      const results = response.data.quotes || [];
      return results.map((result: any) => ({
        symbol: result.symbol,
        description: result.longname || result.shortname,
        name: result.longname || result.shortname,
        type: result.typeDisp,
        exchange: result.exchDisp
      }));
    } catch (error) {
      console.error('Error searching symbols from Yahoo Finance:', error);
      return [];
    }
  }

  async getIndices(): Promise<any[]> {
    try {
      // Indian indices symbols
      const indianIndices = ['^NSEI', '^BSESN', '^NSEBANK', '^CNXIT', '^NSEPHARMA', '^CNXFMCG'];
      
      const promises = indianIndices.map(symbol => this.getQuote(symbol));
      const results = await Promise.allSettled(promises);
      
      const indices = results
        .filter(result => result.status === 'fulfilled')
        .map((result: any) => result.value)
        .map(quote => ({
          name: this.getIndexName(quote.symbol),
          value: quote.price,
          change: quote.change,
          changePercent: quote.changePercent
        }));

      return indices;
    } catch (error) {
      console.error('Error fetching indices from Yahoo Finance:', error);
      return [];
    }
  }

  async getGainers(): Promise<any[]> {
    try {
      // Get top Indian stocks and filter for gainers
      const nifty50Symbols = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS',
        'ASIANPAINT.NS', 'LT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
        'TITAN.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS', 'M&M.NS'
      ];

      const promises = nifty50Symbols.map(symbol => this.getQuote(symbol));
      const results = await Promise.allSettled(promises);
      
      const stocks = results
        .filter(result => result.status === 'fulfilled')
        .map((result: any) => result.value)
        .filter(stock => stock.changePercent > 0)
        .sort((a, b) => b.changePercent - a.changePercent)
        .slice(0, 10)
        .map(stock => ({
          symbol: stock.symbol,
          name: stock.name,
          ltp: stock.price,
          netPrice: stock.change,
          perChange: stock.changePercent
        }));

      return stocks;
    } catch (error) {
      console.error('Error fetching gainers from Yahoo Finance:', error);
      return [];
    }
  }

  async getLosers(): Promise<any[]> {
    try {
      // Get top Indian stocks and filter for losers
      const nifty50Symbols = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
        'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS',
        'ASIANPAINT.NS', 'LT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
        'TITAN.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS', 'M&M.NS'
      ];

      const promises = nifty50Symbols.map(symbol => this.getQuote(symbol));
      const results = await Promise.allSettled(promises);
      
      const stocks = results
        .filter(result => result.status === 'fulfilled')
        .map((result: any) => result.value)
        .filter(stock => stock.changePercent < 0)
        .sort((a, b) => a.changePercent - b.changePercent)
        .slice(0, 10)
        .map(stock => ({
          symbol: stock.symbol,
          name: stock.name,
          ltp: stock.price,
          netPrice: stock.change,
          perChange: stock.changePercent
        }));

      return stocks;
    } catch (error) {
      console.error('Error fetching losers from Yahoo Finance:', error);
      return [];
    }
  }

  async getNews(symbol: string): Promise<any[]> {
    try {
      // Yahoo Finance doesn't provide news API in the same way
      // You could integrate with other news APIs or use web scraping
      // For now, return empty array and rely on mock data
      return [];
    } catch (error) {
      console.error('Error fetching news from Yahoo Finance:', error);
      return [];
    }
  }

  private getIndexName(symbol: string): string {
    const indexNames: { [key: string]: string } = {
      '^NSEI': 'NIFTY 50',
      '^BSESN': 'SENSEX',
      '^NSEBANK': 'NIFTY BANK',
      '^CNXIT': 'NIFTY IT',
      '^NSEPHARMA': 'NIFTY PHARMA',
      '^CNXFMCG': 'NIFTY FMCG'
    };
    return indexNames[symbol] || symbol;
  }
}

export const yahooFinanceService = new YahooFinanceService();