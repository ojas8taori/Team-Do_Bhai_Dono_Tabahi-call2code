import { apiRequest } from './queryClient';

export const api = {
  // Market Data
  getQuote: async (symbol: string, market?: string) => {
    const params = market ? `?market=${market}` : '';
    const response = await apiRequest('GET', `/api/quote/${symbol}${params}`);
    return response.json();
  },

  getProfile: async (symbol: string) => {
    const response = await apiRequest('GET', `/api/profile/${symbol}`);
    return response.json();
  },

  getNews: async (symbol: string) => {
    const response = await apiRequest('GET', `/api/news/${symbol}`);
    return response.json();
  },

  getCandles: async (symbol: string, resolution: string, from: number, to: number) => {
    const response = await apiRequest('GET', `/api/candles/${symbol}?resolution=${resolution}&from=${from}&to=${to}`);
    return response.json();
  },

  getIndices: async () => {
    const response = await apiRequest('GET', '/api/indices');
    return response.json();
  },

  getGainers: async () => {
    const response = await apiRequest('GET', '/api/gainers');
    return response.json();
  },

  getLosers: async () => {
    const response = await apiRequest('GET', '/api/losers');
    return response.json();
  },

  searchSymbols: async (query: string, market?: string) => {
    const params = market ? `?market=${market}` : '';
    const response = await apiRequest('GET', `/api/search/${query}${params}`);
    return response.json();
  },

  // Watchlist
  getWatchlist: async () => {
    const response = await apiRequest('GET', '/api/watchlist');
    return response.json();
  },

  addToWatchlist: async (symbol: string, market: string) => {
    const response = await apiRequest('POST', '/api/watchlist', { symbol, market });
    return response.json();
  },

  removeFromWatchlist: async (symbol: string) => {
    const response = await apiRequest('DELETE', `/api/watchlist/${symbol}`);
    return response.json();
  },

  // Portfolio
  getPortfolio: async () => {
    const response = await apiRequest('GET', '/api/portfolio');
    return response.json();
  },

  addToPortfolio: async (symbol: string, quantity: number, avgPrice: number, market: string) => {
    const response = await apiRequest('POST', '/api/portfolio', { symbol, quantity, avgPrice, market });
    return response.json();
  },

  removeFromPortfolio: async (symbol: string) => {
    const response = await apiRequest('DELETE', `/api/portfolio/${symbol}`);
    return response.json();
  },
};
