import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { isNSESymbol, formatPrice } from "@/lib/utils";
import Header from "@/components/Header";
import MarketOverview from "@/components/MarketOverview";
import StockChart from "@/components/StockChart";
import WatchlistCard from "@/components/WatchlistCard";
import KeyMetrics from "@/components/KeyMetrics";
import MarketMovers from "@/components/MarketMovers";
import NewsCard from "@/components/NewsCard";
import StockSearch from "@/components/StockSearch";
import { Card, CardContent } from "@/components/ui/card";

export default function Dashboard() {
  const [selectedStock, setSelectedStock] = useState({
    symbol: "RELIANCE.NS",
    name: "Reliance Industries Ltd",
  });

  const { data: stockData } = useQuery({
    queryKey: ['/api/quote', selectedStock.symbol],
    queryFn: () => api.getQuote(selectedStock.symbol, isNSESymbol(selectedStock.symbol) ? 'NSE' : 'FINNHUB'),
    enabled: !!selectedStock.symbol,
    refetchInterval: 30000,
  });

  const handleStockSelect = (symbol: string, name: string) => {
    setSelectedStock({ symbol, name });
  };

  const handleSearch = (query: string) => {
    // Search functionality is handled by StockSearch component
    console.log("Search query:", query);
  };

  // Mock data for demonstration
  const mockStockData = {
    price: 2847.50,
    change: 45.25,
    changePercent: 1.62,
    high: 2865.00,
    low: 2820.00,
    open: 2835.00,
    previousClose: 2802.25,
  };

  const currentStockData = stockData || mockStockData;

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Market Dashboard" onSearch={handleSearch} />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Market Overview Cards */}
          <div className="lg:col-span-12">
            <MarketOverview />
          </div>

          {/* Stock Search */}
          <div className="lg:col-span-12 mb-6">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardContent className="p-4">
                <StockSearch 
                  onSelect={handleStockSelect}
                  onAddToWatchlist={(symbol, market) => {
                    console.log("Add to watchlist:", symbol, market);
                  }}
                />
              </CardContent>
            </Card>
          </div>

          {/* Main Chart Section */}
          <div className="lg:col-span-8">
            <StockChart
              symbol={selectedStock.symbol}
              name={selectedStock.name}
              price={currentStockData.price}
              change={currentStockData.change}
              changePercent={currentStockData.changePercent}
            />
          </div>

          {/* Side Panel - Watchlist & Key Metrics */}
          <div className="lg:col-span-4 space-y-6">
            <WatchlistCard />
            <KeyMetrics symbol={selectedStock.symbol} />
          </div>

          {/* Market Movers Section */}
          <div className="lg:col-span-6">
            <MarketMovers type="gainers" />
          </div>

          <div className="lg:col-span-6">
            <MarketMovers type="losers" />
          </div>

          {/* News Section */}
          <div className="lg:col-span-12">
            <NewsCard symbol={selectedStock.symbol} />
          </div>
        </div>
      </main>
    </div>
  );
}
