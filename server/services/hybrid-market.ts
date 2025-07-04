import { alphaVantageService } from './alphavantage';
import { reliableMarketService } from './reliable-market';

export class HybridMarketService {
  private isIndianStock(symbol: string): boolean {
    return symbol.includes('.NS') || symbol.includes('.BO');
  }

  async getQuote(symbol: string): Promise<any> {
    if (this.isIndianStock(symbol)) {
      // Use reliable market service for Indian stocks
      return await reliableMarketService.getQuote(symbol);
    } else {
      // Use Alpha Vantage for US stocks
      return await alphaVantageService.getQuote(symbol);
    }
  }

  async getProfile(symbol: string): Promise<any> {
    if (this.isIndianStock(symbol)) {
      return await reliableMarketService.getProfile(symbol);
    } else {
      return await alphaVantageService.getProfile(symbol);
    }
  }

  async getCandles(symbol: string, resolution: string, from: number, to: number): Promise<any> {
    if (this.isIndianStock(symbol)) {
      return await reliableMarketService.getCandles(symbol, resolution, from, to);
    } else {
      return await alphaVantageService.getCandles(symbol, resolution, from, to);
    }
  }

  async searchSymbols(query: string): Promise<any[]> {
    // Search both US and Indian markets
    const [usResults, indianResults] = await Promise.allSettled([
      alphaVantageService.searchSymbols(query),
      reliableMarketService.searchSymbols(query)
    ]);

    const results = [];
    
    if (usResults.status === 'fulfilled') {
      results.push(...usResults.value);
    }
    
    if (indianResults.status === 'fulfilled') {
      results.push(...indianResults.value);
    }

    return results;
  }

  async getIndices(): Promise<any[]> {
    // Get indices from both services
    const [usIndices, indianIndices] = await Promise.allSettled([
      alphaVantageService.getIndices(),
      reliableMarketService.getIndices()
    ]);

    const results = [];
    
    if (usIndices.status === 'fulfilled') {
      results.push(...usIndices.value);
    }
    
    if (indianIndices.status === 'fulfilled') {
      results.push(...indianIndices.value);
    }

    return results;
  }

  async getGainers(): Promise<any[]> {
    // Focus on Indian market gainers since that's what the user specifically requested
    try {
      return await reliableMarketService.getGainers();
    } catch (error) {
      console.error('Error fetching Indian gainers:', error);
      return [];
    }
  }

  async getLosers(): Promise<any[]> {
    // Focus on Indian market losers since that's what the user specifically requested
    try {
      return await reliableMarketService.getLosers();
    } catch (error) {
      console.error('Error fetching Indian losers:', error);
      return [];
    }
  }

  async getNews(symbol: string): Promise<any[]> {
    if (this.isIndianStock(symbol)) {
      return await reliableMarketService.getNews(symbol);
    } else {
      return await alphaVantageService.getNews(symbol);
    }
  }
}

export const hybridMarketService = new HybridMarketService();