import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { isNSESymbol } from "@/lib/utils";
import Header from "@/components/Header";
import StockSearch from "@/components/StockSearch";
import StockChart from "@/components/StockChart";
import KeyMetrics from "@/components/KeyMetrics";
import NewsCard from "@/components/NewsCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Building, Globe, TrendingUp } from "lucide-react";

export default function StockAnalysis() {
  const [selectedStock, setSelectedStock] = useState({
    symbol: "RELIANCE.NS",
    name: "Reliance Industries Ltd",
  });

  const { data: stockData, isLoading: stockLoading } = useQuery({
    queryKey: ['/api/quote', selectedStock.symbol],
    queryFn: () => api.getQuote(selectedStock.symbol, isNSESymbol(selectedStock.symbol) ? 'NSE' : 'FINNHUB'),
    enabled: !!selectedStock.symbol,
    refetchInterval: 30000,
  });

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['/api/profile', selectedStock.symbol],
    queryFn: () => api.getProfile(selectedStock.symbol),
    enabled: !!selectedStock.symbol && !isNSESymbol(selectedStock.symbol),
  });

  const handleStockSelect = (symbol: string, name: string) => {
    setSelectedStock({ symbol, name });
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

  const mockProfile = {
    name: "Reliance Industries Ltd",
    country: "India",
    currency: "INR",
    exchange: "NSE",
    industry: "Oil & Gas",
    marketCap: 18120000000000,
    logo: "",
    weburl: "https://www.ril.com",
  };

  const currentStockData = stockData || mockStockData;
  const currentProfile = profile || mockProfile;

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Stock Analysis" />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          {/* Stock Search */}
          <div className="mb-6">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader>
                <CardTitle className="text-lg font-bold">Select Stock for Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <StockSearch 
                  onSelect={handleStockSelect}
                />
              </CardContent>
            </Card>
          </div>

          {/* Stock Profile */}
          <div className="mb-6">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-dark-primary rounded-lg flex items-center justify-center">
                      <Building className="w-6 h-6 text-accent-blue" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold">{selectedStock.symbol}</h2>
                      <p className="text-gray-400">{currentProfile.name}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <Badge variant="outline" className="flex items-center space-x-1">
                      <Globe className="w-3 h-3" />
                      <span>{currentProfile.exchange}</span>
                    </Badge>
                    <Badge variant="outline">
                      {currentProfile.industry}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              {profileLoading ? (
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Skeleton className="h-20" />
                    <Skeleton className="h-20" />
                    <Skeleton className="h-20" />
                  </div>
                </CardContent>
              ) : (
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Country</p>
                      <p className="text-lg font-semibold">{currentProfile.country}</p>
                    </div>
                    <div className="text-center p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Currency</p>
                      <p className="text-lg font-semibold">{currentProfile.currency}</p>
                    </div>
                    <div className="text-center p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Exchange</p>
                      <p className="text-lg font-semibold">{currentProfile.exchange}</p>
                    </div>
                  </div>
                </CardContent>
              )}
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Chart Section */}
            <div className="lg:col-span-8">
              <StockChart
                symbol={selectedStock.symbol}
                name={selectedStock.name}
                price={currentStockData.price}
                change={currentStockData.change}
                changePercent={currentStockData.changePercent}
              />
            </div>

            {/* Key Metrics */}
            <div className="lg:col-span-4">
              <KeyMetrics symbol={selectedStock.symbol} />
            </div>

            {/* Technical Analysis */}
            <div className="lg:col-span-12">
              <Card className="bg-dark-secondary border-dark-tertiary">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center space-x-2">
                    <TrendingUp className="w-5 h-5" />
                    <span>Technical Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">RSI (14)</p>
                      <p className="text-lg font-semibold">65.4</p>
                      <p className="text-xs text-yellow-400">Neutral</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">MACD</p>
                      <p className="text-lg font-semibold">12.5</p>
                      <p className="text-xs text-green-400">Bullish</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Moving Avg (50)</p>
                      <p className="text-lg font-semibold">2,785.30</p>
                      <p className="text-xs text-green-400">Above</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Bollinger Bands</p>
                      <p className="text-lg font-semibold">Mid Band</p>
                      <p className="text-xs text-yellow-400">Near Center</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* News Section */}
            <div className="lg:col-span-12">
              <NewsCard symbol={selectedStock.symbol} showFilters={false} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
