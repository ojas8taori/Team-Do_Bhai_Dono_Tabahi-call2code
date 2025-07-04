import axios from 'axios';

interface NSEQuote {
  symbol: string;
  companyName: string;
  lastPrice: number;
  change: number;
  pChange: number;
  previousClose: number;
  open: number;
  close: number;
  dayHigh: number;
  dayLow: number;
  totalTradedVolume: number;
  totalTradedValue: number;
  lastUpdateTime: string;
}

interface NSEGainerLoser {
  symbol: string;
  ltp: number;
  netPrice: number;
  perChange: number;
  lastCorpAnnouncementDate: string;
  lastCorpAnnouncement: string;
}

export class NSEService {
  private baseUrl = 'https://www.nseindia.com/api';
  private headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
  };

  async getQuote(symbol: string): Promise<NSEQuote> {
    try {
      const response = await axios.get(`${this.baseUrl}/quote-equity`, {
        params: { symbol: symbol.replace('.NS', '') },
        headers: this.headers
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching quote from NSE:', error);
      throw new Error('Failed to fetch NSE quote data');
    }
  }

  async getIndices(): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/allIndices`, {
        headers: this.headers
      });
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching indices from NSE:', error);
      throw new Error('Failed to fetch NSE indices data');
    }
  }

  async getGainers(): Promise<NSEGainerLoser[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/live-analysis-gainers`, {
        params: { index: 'gainers' },
        headers: this.headers
      });
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching gainers from NSE:', error);
      throw new Error('Failed to fetch NSE gainers data');
    }
  }

  async getLosers(): Promise<NSEGainerLoser[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/live-analysis-losers`, {
        params: { index: 'losers' },
        headers: this.headers
      });
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching losers from NSE:', error);
      throw new Error('Failed to fetch NSE losers data');
    }
  }

  async searchSymbols(query: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/search/autocomplete`, {
        params: { q: query },
        headers: this.headers
      });
      return response.data.symbols || [];
    } catch (error) {
      console.error('Error searching symbols from NSE:', error);
      throw new Error('Failed to search NSE symbols');
    }
  }
}

export const nseService = new NSEService();
