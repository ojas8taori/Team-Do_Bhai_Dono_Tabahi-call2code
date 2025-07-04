import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number, currency: string = 'USD'): string {
  if (currency === 'INR') {
    return `₹${price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }
  return `$${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function formatChange(change: number, changePercent: number): string {
  const sign = change >= 0 ? '+' : '';
  return `${sign}${change.toFixed(2)} (${sign}${changePercent.toFixed(2)}%)`;
}

export function formatVolume(volume: number): string {
  if (volume >= 1000000000) {
    return `${(volume / 1000000000).toFixed(1)}B`;
  } else if (volume >= 1000000) {
    return `${(volume / 1000000).toFixed(1)}M`;
  } else if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`;
  }
  return volume.toString();
}

export function formatMarketCap(marketCap: number): string {
  if (marketCap >= 1000000000000) {
    return `${(marketCap / 1000000000000).toFixed(2)}T`;
  } else if (marketCap >= 1000000000) {
    return `${(marketCap / 1000000000).toFixed(2)}B`;
  } else if (marketCap >= 1000000) {
    return `${(marketCap / 1000000).toFixed(2)}M`;
  }
  return marketCap.toString();
}

export function getChangeColor(change: number): string {
  if (change > 0) return 'text-green-500';
  if (change < 0) return 'text-red-500';
  return 'text-gray-400';
}

export function getSentimentColor(sentiment: string): string {
  switch (sentiment) {
    case 'positive':
      return 'text-green-500 bg-green-500/20';
    case 'negative':
      return 'text-red-500 bg-red-500/20';
    default:
      return 'text-gray-400 bg-gray-400/20';
  }
}

export function getTimeframeTimestamp(timeframe: string): { from: number; to: number } {
  const now = Math.floor(Date.now() / 1000);
  let from: number;

  switch (timeframe) {
    case '1D':
      from = now - 24 * 60 * 60;
      break;
    case '1W':
      from = now - 7 * 24 * 60 * 60;
      break;
    case '1M':
      from = now - 30 * 24 * 60 * 60;
      break;
    case '3M':
      from = now - 90 * 24 * 60 * 60;
      break;
    case '1Y':
      from = now - 365 * 24 * 60 * 60;
      break;
    case '5Y':
      from = now - 5 * 365 * 24 * 60 * 60;
      break;
    default:
      from = now - 24 * 60 * 60;
  }

  return { from, to: now };
}

export function isNSESymbol(symbol: string): boolean {
  return symbol.endsWith('.NS') || symbol.endsWith('.BO');
}
