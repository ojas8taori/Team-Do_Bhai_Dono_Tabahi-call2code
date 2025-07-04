import axios from 'axios';

interface AlphaVantageQuote {
  "01. symbol": string;
  "02. open": string;
  "03. high": string;
  "04. low": string;
  "05. price": string;
  "06. volume": string;
  "07. latest trading day": string;
  "08. previous close": string;
  "09. change": string;
  "10. change percent": string;
}

interface AlphaVantageTimeSeriesData {
  [key: string]: {
    "1. open": string;
    "2. high": string;
    "3. low": string;
    "4. close": string;
    "5. volume": string;
  };
}

interface AlphaVantageTimeSeries {
  "Meta Data": {
    "1. Information": string;
    "2. Symbol": string;
    "3. Last Refreshed": string;
    "4. Output Size": string;
    "5. Time Zone": string;
  };
  "Time Series (Daily)": AlphaVantageTimeSeriesData;
}

interface AlphaVantageSearch {
  "1. symbol": string;
  "2. name": string;
  "3. type": string;
  "4. region": string;
  "5. marketOpen": string;
  "6. marketClose": string;
  "7. timezone": string;
  "8. currency": string;
  "9. matchScore": string;
}

export class AlphaVantageService {
  private apiKey: string;
  private baseUrl = 'https://www.alphavantage.co/query';

  constructor() {
    this.apiKey = process.env.ALPHA_VANTAGE_API_KEY || 'P02ZEMA2P77T8ASE';
  }

  async getQuote(symbol: string): Promise<any> {
    try {
      const response = await axios.get(this.baseUrl, {
        params: {
          function: 'GLOBAL_QUOTE',
          symbol: symbol,
          apikey: this.apiKey,
        },
      });

      const quote = response.data['Global Quote'];
      
      if (!quote || Object.keys(quote).length === 0) {
        throw new Error('No quote data available');
      }

      const price = parseFloat(quote['05. price']);
      const change = parseFloat(quote['09. change']);
      const previousClose = parseFloat(quote['08. previous close']);
      const changePercent = parseFloat(quote['10. change percent'].replace('%', ''));

      return {
        symbol: symbol,
        name: this.getCompanyName(symbol),
        price: price,
        change: change,
        changePercent: changePercent,
        high: parseFloat(quote['03. high']),
        low: parseFloat(quote['04. low']),
        open: parseFloat(quote['02. open']),
        previousClose: previousClose,
        volume: parseInt(quote['06. volume']),
        currency: this.getCurrency(symbol),
        exchange: this.getExchange(symbol),
        fiftyTwoWeekHigh: price * 1.25, // Approximate
        fiftyTwoWeekLow: price * 0.75,  // Approximate
      };
    } catch (error) {
      console.error('Error fetching quote from Alpha Vantage:', error);
      throw error;
    }
  }

  async getProfile(symbol: string): Promise<any> {
    try {
      const response = await axios.get(this.baseUrl, {
        params: {
          function: 'OVERVIEW',
          symbol: symbol,
          apikey: this.apiKey,
        },
      });

      const overview = response.data;
      
      if (!overview || overview.Symbol !== symbol) {
        // Return basic profile if detailed overview not available
        return {
          symbol: symbol,
          name: this.getCompanyName(symbol),
          country: this.getCountry(symbol),
          currency: this.getCurrency(symbol),
          exchange: this.getExchange(symbol),
          industry: overview.Industry || 'N/A',
          marketCapitalization: overview.MarketCapitalization || 0,
          description: overview.Description || 'No description available',
          peRatio: overview.PERatio || 0,
          pegRatio: overview.PEGRatio || 0,
          bookValue: overview.BookValue || 0,
          dividendYield: overview.DividendYield || 0,
          eps: overview.EPS || 0,
          revenuePerShareTTM: overview.RevenuePerShareTTM || 0,
          profitMargin: overview.ProfitMargin || 0,
          operatingMarginTTM: overview.OperatingMarginTTM || 0,
          returnOnAssetsTTM: overview.ReturnOnAssetsTTM || 0,
          returnOnEquityTTM: overview.ReturnOnEquityTTM || 0,
          revenueTTM: overview.RevenueTTM || 0,
          grossProfitTTM: overview.GrossProfitTTM || 0,
          dilutedEPSTTM: overview.DilutedEPSTTM || 0,
          quarterlyEarningsGrowthYOY: overview.QuarterlyEarningsGrowthYOY || 0,
          quarterlyRevenueGrowthYOY: overview.QuarterlyRevenueGrowthYOY || 0,
          analystTargetPrice: overview.AnalystTargetPrice || 0,
          trailingPE: overview.TrailingPE || 0,
          forwardPE: overview.ForwardPE || 0,
          priceToSalesRatioTTM: overview.PriceToSalesRatioTTM || 0,
          priceToBookRatio: overview.PriceToBookRatio || 0,
          evToRevenue: overview.EVToRevenue || 0,
          evToEBITDA: overview.EVToEBITDA || 0,
          beta: overview.Beta || 0,
          week52High: overview['52WeekHigh'] || 0,
          week52Low: overview['52WeekLow'] || 0,
          movingAverage50Day: overview['50DayMovingAverage'] || 0,
          movingAverage200Day: overview['200DayMovingAverage'] || 0,
          sharesOutstanding: overview.SharesOutstanding || 0,
          sharesFloat: overview.SharesFloat || 0,
          sharesShort: overview.SharesShort || 0,
          sharesShortPriorMonth: overview.SharesShortPriorMonth || 0,
          shortRatio: overview.ShortRatio || 0,
          shortPercentOutstanding: overview.ShortPercentOutstanding || 0,
          shortPercentFloat: overview.ShortPercentFloat || 0,
          percentInsiders: overview.PercentInsiders || 0,
          percentInstitutions: overview.PercentInstitutions || 0,
          forwardAnnualDividendRate: overview.ForwardAnnualDividendRate || 0,
          forwardAnnualDividendYield: overview.ForwardAnnualDividendYield || 0,
          payoutRatio: overview.PayoutRatio || 0,
          dividendDate: overview.DividendDate || '',
          exDividendDate: overview.ExDividendDate || '',
          lastSplitFactor: overview.LastSplitFactor || '',
          lastSplitDate: overview.LastSplitDate || '',
        };
      }

      return overview;
    } catch (error) {
      console.error('Error fetching profile from Alpha Vantage:', error);
      throw error;
    }
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<any> {
    try {
      const response = await axios.get(this.baseUrl, {
        params: {
          function: 'TIME_SERIES_DAILY',
          symbol: symbol,
          apikey: this.apiKey,
          outputsize: 'full',
        },
      });

      const timeSeries = response.data['Time Series (Daily)'];
      
      if (!timeSeries) {
        throw new Error('No time series data available');
      }

      const timestamps: number[] = [];
      const opens: number[] = [];
      const highs: number[] = [];
      const lows: number[] = [];
      const closes: number[] = [];
      const volumes: number[] = [];

      // Sort dates and filter by time range
      const sortedDates = Object.keys(timeSeries).sort();
      const fromDate = new Date(from * 1000);
      const toDate = new Date(to * 1000);

      for (const date of sortedDates) {
        const currentDate = new Date(date);
        if (currentDate >= fromDate && currentDate <= toDate) {
          const data = timeSeries[date];
          timestamps.push(Math.floor(currentDate.getTime() / 1000));
          opens.push(parseFloat(data['1. open']));
          highs.push(parseFloat(data['2. high']));
          lows.push(parseFloat(data['3. low']));
          closes.push(parseFloat(data['4. close']));
          volumes.push(parseInt(data['5. volume']));
        }
      }

      return {
        t: timestamps,
        o: opens,
        h: highs,
        l: lows,
        c: closes,
        v: volumes,
        s: 'ok',
      };
    } catch (error) {
      console.error('Error fetching candles from Alpha Vantage:', error);
      throw error;
    }
  }

  async searchSymbols(query: string): Promise<any[]> {
    try {
      const response = await axios.get(this.baseUrl, {
        params: {
          function: 'SYMBOL_SEARCH',
          keywords: query,
          apikey: this.apiKey,
        },
      });

      const matches = response.data['bestMatches'] || [];
      
      return matches.map((match: AlphaVantageSearch) => ({
        symbol: match['1. symbol'],
        name: match['2. name'],
        type: match['3. type'],
        region: match['4. region'],
        marketOpen: match['5. marketOpen'],
        marketClose: match['6. marketClose'],
        timezone: match['7. timezone'],
        currency: match['8. currency'],
        matchScore: parseFloat(match['9. matchScore']),
      }));
    } catch (error) {
      console.error('Error searching symbols in Alpha Vantage:', error);
      throw error;
    }
  }

  async getIndices(): Promise<any[]> {
    // Major indices for both US and Indian markets
    const indices = [
      { symbol: 'SPY', name: 'S&P 500' },
      { symbol: 'QQQ', name: 'NASDAQ-100' },
      { symbol: 'DIA', name: 'Dow Jones' },
      { symbol: 'NSEI', name: 'NIFTY 50' },
      { symbol: 'BSESN', name: 'BSE SENSEX' },
    ];

    const results = [];
    for (const index of indices) {
      try {
        const quote = await this.getQuote(index.symbol);
        results.push({
          name: index.name,
          value: quote.price,
          change: quote.change,
          changePercent: quote.changePercent,
          symbol: index.symbol,
        });
      } catch (error) {
        console.error(`Error fetching index ${index.symbol}:`, error);
        // Continue with other indices
      }
    }

    return results;
  }

  async getGainers(): Promise<any[]> {
    // For demonstration, we'll get quotes for popular Indian stocks
    const popularStocks = [
      'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
      'HDFC.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS',
      'SBIN.NS', 'BAJFINANCE.NS', 'MARUTI.NS', 'ASIANPAINT.NS', 'WIPRO.NS'
    ];

    const quotes = [];
    for (const symbol of popularStocks) {
      try {
        const quote = await this.getQuote(symbol);
        if (quote.changePercent > 0) {
          quotes.push({
            symbol: quote.symbol,
            name: quote.name,
            ltp: quote.price,
            netPrice: quote.change,
            perChange: quote.changePercent,
          });
        }
      } catch (error) {
        console.error(`Error fetching quote for ${symbol}:`, error);
      }
    }

    // Sort by percentage change descending and return top gainers
    return quotes.sort((a, b) => b.perChange - a.perChange).slice(0, 10);
  }

  async getLosers(): Promise<any[]> {
    // For demonstration, we'll get quotes for popular Indian stocks
    const popularStocks = [
      'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
      'HDFC.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'ITC.NS',
      'SBIN.NS', 'BAJFINANCE.NS', 'MARUTI.NS', 'ASIANPAINT.NS', 'WIPRO.NS'
    ];

    const quotes = [];
    for (const symbol of popularStocks) {
      try {
        const quote = await this.getQuote(symbol);
        if (quote.changePercent < 0) {
          quotes.push({
            symbol: quote.symbol,
            name: quote.name,
            ltp: quote.price,
            netPrice: quote.change,
            perChange: quote.changePercent,
          });
        }
      } catch (error) {
        console.error(`Error fetching quote for ${symbol}:`, error);
      }
    }

    // Sort by percentage change ascending and return top losers
    return quotes.sort((a, b) => a.perChange - b.perChange).slice(0, 10);
  }

  async getNews(symbol: string): Promise<any[]> {
    try {
      const response = await axios.get(this.baseUrl, {
        params: {
          function: 'NEWS_SENTIMENT',
          tickers: symbol,
          apikey: this.apiKey,
          limit: 50,
        },
      });

      const feed = response.data.feed || [];
      
      return feed.map((article: any) => ({
        category: 'general',
        datetime: new Date(article.time_published).getTime() / 1000,
        headline: article.title,
        id: article.url.split('/').pop(),
        image: article.banner_image || '',
        related: symbol,
        source: article.source,
        summary: article.summary,
        url: article.url,
        sentiment: {
          sentiment: article.overall_sentiment_label?.toLowerCase() || 'neutral',
          score: article.overall_sentiment_score || 0,
        },
      }));
    } catch (error) {
      console.error('Error fetching news from Alpha Vantage:', error);
      return [];
    }
  }

  private getCompanyName(symbol: string): string {
    const companies: { [key: string]: string } = {
      'RELIANCE.NS': 'Reliance Industries Ltd',
      'TCS.NS': 'Tata Consultancy Services',
      'HDFCBANK.NS': 'HDFC Bank Limited',
      'INFY.NS': 'Infosys Limited',
      'HINDUNILVR.NS': 'Hindustan Unilever Limited',
      'HDFC.NS': 'Housing Development Finance Corporation',
      'ICICIBANK.NS': 'ICICI Bank Limited',
      'KOTAKBANK.NS': 'Kotak Mahindra Bank Limited',
      'BHARTIARTL.NS': 'Bharti Airtel Limited',
      'ITC.NS': 'ITC Limited',
      'SBIN.NS': 'State Bank of India',
      'BAJFINANCE.NS': 'Bajaj Finance Limited',
      'MARUTI.NS': 'Maruti Suzuki India Limited',
      'ASIANPAINT.NS': 'Asian Paints Limited',
      'WIPRO.NS': 'Wipro Limited',
      'AAPL': 'Apple Inc.',
      'MSFT': 'Microsoft Corporation',
      'GOOGL': 'Alphabet Inc.',
      'AMZN': 'Amazon.com Inc.',
      'TSLA': 'Tesla Inc.',
      'SPY': 'SPDR S&P 500 ETF',
      'QQQ': 'Invesco QQQ Trust',
      'DIA': 'SPDR Dow Jones Industrial Average ETF',
    };
    
    return companies[symbol] || symbol;
  }

  private getCurrency(symbol: string): string {
    return symbol.includes('.NS') ? 'INR' : 'USD';
  }

  private getExchange(symbol: string): string {
    if (symbol.includes('.NS')) return 'NSE';
    if (symbol.includes('.BO')) return 'BSE';
    return 'NASDAQ';
  }

  private getCountry(symbol: string): string {
    return symbol.includes('.NS') || symbol.includes('.BO') ? 'India' : 'United States';
  }
}

export const alphaVantageService = new AlphaVantageService();