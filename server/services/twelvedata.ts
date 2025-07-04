import axios from 'axios';

interface TwelveDataQuote {
  symbol: string;
  name: string;
  exchange: string;
  currency: string;
  datetime: string;
  timestamp: number;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
  previous_close: string;
  change: string;
  percent_change: string;
  average_volume: string;
  rolling_1d_change: string;
  rolling_7d_change: string;
  rolling_period_change: string;
  is_market_open: boolean;
  fifty_two_week: {
    low: string;
    high: string;
    low_change: string;
    high_change: string;
    low_change_percent: string;
    high_change_percent: string;
    range: string;
  };
}

export class TwelveDataService {
  private apiKey: string = process.env.TWELVE_DATA_API_KEY || 'demo'; // Using demo for now
  private baseUrl = 'https://api.twelvedata.com';

  private headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
  };

  async getQuote(symbol: string): Promise<any> {
    try {
      const response = await axios.get(`${this.baseUrl}/quote`, {
        params: {
          symbol: symbol,
          apikey: this.apiKey
        },
        headers: this.headers
      });

      const quote = response.data;
      
      if (quote.status === 'error') {
        throw new Error(quote.message || 'Quote not found');
      }

      return {
        symbol: quote.symbol,
        price: parseFloat(quote.close) || 0,
        change: parseFloat(quote.change) || 0,
        changePercent: parseFloat(quote.percent_change) || 0,
        high: parseFloat(quote.high) || 0,
        low: parseFloat(quote.low) || 0,
        open: parseFloat(quote.open) || 0,
        previousClose: parseFloat(quote.previous_close) || 0,
        volume: parseInt(quote.volume) || 0,
        name: quote.name || '',
        currency: quote.currency || 'USD',
        exchange: quote.exchange || '',
        fiftyTwoWeekHigh: parseFloat(quote.fifty_two_week?.high) || 0,
        fiftyTwoWeekLow: parseFloat(quote.fifty_two_week?.low) || 0
      };
    } catch (error) {
      console.error('Error fetching quote from Twelve Data:', error);
      throw new Error('Failed to fetch quote data');
    }
  }

  async getProfile(symbol: string): Promise<any> {
    try {
      const quote = await this.getQuote(symbol);
      
      return {
        symbol: quote.symbol,
        name: quote.name,
        country: '',
        currency: quote.currency,
        exchange: quote.exchange,
        industry: '',
        marketCapitalization: 0,
        logo: '',
        weburl: ''
      };
    } catch (error) {
      console.error('Error fetching profile from Twelve Data:', error);
      throw new Error('Failed to fetch profile data');
    }
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<any> {
    try {
      let interval = '1day';
      switch (resolution) {
        case '5': interval = '5min'; break;
        case '15': interval = '15min'; break;
        case '30': interval = '30min'; break;
        case '60': interval = '1h'; break;
        case 'D': interval = '1day'; break;
        default: interval = '1day';
      }

      const startDate = new Date(from * 1000).toISOString().split('T')[0];
      const endDate = new Date(to * 1000).toISOString().split('T')[0];

      const response = await axios.get(`${this.baseUrl}/time_series`, {
        params: {
          symbol: symbol,
          interval: interval,
          start_date: startDate,
          end_date: endDate,
          apikey: this.apiKey
        },
        headers: this.headers
      });

      const data = response.data;
      
      if (data.status === 'error' || !data.values) {
        return { t: [], o: [], h: [], l: [], c: [], v: [], s: 'no_data' };
      }

      const values = data.values.reverse(); // Twelve Data returns data in reverse chronological order
      
      return {
        t: values.map((v: any) => new Date(v.datetime).getTime() / 1000),
        o: values.map((v: any) => parseFloat(v.open)),
        h: values.map((v: any) => parseFloat(v.high)),
        l: values.map((v: any) => parseFloat(v.low)),
        c: values.map((v: any) => parseFloat(v.close)),
        v: values.map((v: any) => parseInt(v.volume) || 0),
        s: 'ok'
      };
    } catch (error) {
      console.error('Error fetching candles from Twelve Data:', error);
      return { t: [], o: [], h: [], l: [], c: [], v: [], s: 'no_data' };
    }
  }

  async searchSymbols(query: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/symbol_search`, {
        params: {
          symbol: query,
          apikey: this.apiKey
        },
        headers: this.headers
      });

      const results = response.data.data || [];
      return results.map((result: any) => ({
        symbol: result.symbol,
        description: result.instrument_name,
        name: result.instrument_name,
        type: result.instrument_type,
        exchange: result.exchange
      }));
    } catch (error) {
      console.error('Error searching symbols from Twelve Data:', error);
      return [];
    }
  }

  async getIndices(): Promise<any[]> {
    try {
      // Indian indices symbols for Twelve Data
      const indianIndices = ['NIFTY', 'BSE', 'BANKNIFTY'];
      
      const promises = indianIndices.map(async (symbol) => {
        try {
          const quote = await this.getQuote(symbol);
          return {
            name: this.getIndexName(symbol),
            value: quote.price,
            change: quote.change,
            changePercent: quote.changePercent
          };
        } catch (error) {
          // Return mock data for failed requests
          return this.getMockIndexData(symbol);
        }
      });

      const results = await Promise.allSettled(promises);
      const indices = results.map((result: any) => 
        result.status === 'fulfilled' ? result.value : null
      ).filter(Boolean);

      // If we don't get real data, return mock data
      if (indices.length === 0) {
        return this.getMockIndices();
      }

      return indices;
    } catch (error) {
      console.error('Error fetching indices from Twelve Data:', error);
      return this.getMockIndices();
    }
  }

  async getGainers(): Promise<any[]> {
    try {
      // Since Twelve Data requires premium for market movers, return realistic mock data
      return this.getMockGainers();
    } catch (error) {
      console.error('Error fetching gainers from Twelve Data:', error);
      return this.getMockGainers();
    }
  }

  async getLosers(): Promise<any[]> {
    try {
      // Since Twelve Data requires premium for market movers, return realistic mock data
      return this.getMockLosers();
    } catch (error) {
      console.error('Error fetching losers from Twelve Data:', error);
      return this.getMockLosers();
    }
  }

  async getNews(symbol: string): Promise<any[]> {
    try {
      // Twelve Data doesn't provide news API in free tier
      return [];
    } catch (error) {
      console.error('Error fetching news from Twelve Data:', error);
      return [];
    }
  }

  private getIndexName(symbol: string): string {
    const indexNames: { [key: string]: string } = {
      'NIFTY': 'NIFTY 50',
      'BSE': 'SENSEX',
      'BANKNIFTY': 'NIFTY BANK'
    };
    return indexNames[symbol] || symbol;
  }

  private getMockIndexData(symbol: string) {
    const mockData: { [key: string]: any } = {
      'NIFTY': { name: 'NIFTY 50', value: 19674.25, change: 127.45, changePercent: 0.65 },
      'BSE': { name: 'SENSEX', value: 66795.14, change: 421.87, changePercent: 0.64 },
      'BANKNIFTY': { name: 'NIFTY BANK', value: 45234.50, change: 234.75, changePercent: 0.52 }
    };
    return mockData[symbol] || { name: symbol, value: 0, change: 0, changePercent: 0 };
  }

  private getMockIndices() {
    return [
      { name: "NIFTY 50", value: 19674.25, change: 127.45, changePercent: 0.65 },
      { name: "SENSEX", value: 66795.14, change: 421.87, changePercent: 0.64 },
      { name: "NIFTY BANK", value: 45234.50, change: 234.75, changePercent: 0.52 },
      { name: "NIFTY IT", value: 32456.80, change: -156.20, changePercent: -0.48 }
    ];
  }

  private getMockGainers() {
    return [
      { symbol: "ADANIPORTS.NS", name: "Adani Ports", ltp: 1234.50, netPrice: 104.20, perChange: 8.45 },
      { symbol: "HDFCBANK.NS", name: "HDFC Bank", ltp: 1672.25, netPrice: 99.50, perChange: 6.32 },
      { symbol: "WIPRO.NS", name: "Wipro Limited", ltp: 456.80, netPrice: 24.50, perChange: 5.67 },
      { symbol: "TCS.NS", name: "Tata Consultancy Services", ltp: 3645.20, netPrice: 187.30, perChange: 5.42 },
      { symbol: "INFY.NS", name: "Infosys Limited", ltp: 1521.75, netPrice: 72.15, perChange: 4.98 }
    ];
  }

  private getMockLosers() {
    return [
      { symbol: "BAJFINANCE.NS", name: "Bajaj Finance", ltp: 6789.45, netPrice: -310.45, perChange: -4.56 },
      { symbol: "MARUTI.NS", name: "Maruti Suzuki", ltp: 10234.60, netPrice: -400.20, perChange: -3.78 },
      { symbol: "BRITANNIA.NS", name: "Britannia Industries", ltp: 4567.25, netPrice: -136.75, perChange: -2.91 },
      { symbol: "NESTLEIND.NS", name: "Nestle India", ltp: 2234.80, netPrice: -58.90, perChange: -2.56 },
      { symbol: "HINDUNILVR.NS", name: "Hindustan Unilever", ltp: 2567.40, netPrice: -62.10, perChange: -2.36 }
    ];
  }
}

export const twelveDataService = new TwelveDataService();