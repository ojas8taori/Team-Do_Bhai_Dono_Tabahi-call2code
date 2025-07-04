export interface StockQuote {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  open: number;
  previousClose: number;
  volume?: number;
}

export interface StockProfile {
  symbol: string;
  name: string;
  country: string;
  currency: string;
  exchange: string;
  industry: string;
  marketCap: number;
  logo?: string;
  weburl?: string;
}

export interface NewsArticle {
  id: string;
  headline: string;
  summary: string;
  source: string;
  url: string;
  image?: string;
  datetime: number;
  sentiment: {
    sentiment: 'positive' | 'negative' | 'neutral';
    score: number;
  };
}

export interface ChartData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface WatchlistItem {
  id: number;
  symbol: string;
  market: string;
  addedAt: string;
}

export interface PortfolioItem {
  id: number;
  symbol: string;
  quantity: number;
  avgPrice: number;
  market: string;
  createdAt: string;
}

export interface MarketIndex {
  name: string;
  value: number;
  change: number;
  changePercent: number;
}

export interface MarketMover {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
}

export type TimeFrame = '1D' | '1W' | '1M' | '3M' | '1Y' | '5Y';
