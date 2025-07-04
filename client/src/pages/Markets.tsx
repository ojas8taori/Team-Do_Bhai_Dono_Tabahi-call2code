import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, getChangeColor } from "@/lib/utils";
import Header from "@/components/Header";
import MarketOverview from "@/components/MarketOverview";
import MarketMovers from "@/components/MarketMovers";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Globe, TrendingUp, TrendingDown, Activity, DollarSign } from "lucide-react";

export default function Markets() {
  const { data: indices, isLoading: indicesLoading } = useQuery({
    queryKey: ['/api/indices'],
    refetchInterval: 30000,
  });

  const { data: gainers, isLoading: gainersLoading } = useQuery({
    queryKey: ['/api/gainers'],
    refetchInterval: 60000,
  });

  const { data: losers, isLoading: losersLoading } = useQuery({
    queryKey: ['/api/losers'],
    refetchInterval: 60000,
  });

  // Mock data for comprehensive market view
  const mockIndices = [
    { name: "NIFTY 50", value: 19674.25, change: 127.45, changePercent: 0.65, volume: 2450000000 },
    { name: "SENSEX", value: 66795.14, change: 421.87, changePercent: 0.64, volume: 1850000000 },
    { name: "NIFTY BANK", value: 45234.50, change: 234.75, changePercent: 0.52, volume: 890000000 },
    { name: "NIFTY IT", value: 32456.80, change: -156.20, changePercent: -0.48, volume: 567000000 },
    { name: "NIFTY PHARMA", value: 15678.90, change: 89.45, changePercent: 0.57, volume: 234000000 },
    { name: "NIFTY FMCG", value: 52345.60, change: -89.30, changePercent: -0.17, volume: 345000000 },
  ];

  const mockGlobalIndices = [
    { name: "S&P 500", value: 4765.20, change: -12.45, changePercent: -0.26, country: "US" },
    { name: "NASDAQ", value: 15047.70, change: 65.12, changePercent: 0.43, country: "US" },
    { name: "DOW JONES", value: 37689.54, change: -45.68, changePercent: -0.12, country: "US" },
    { name: "FTSE 100", value: 7456.23, change: 23.45, changePercent: 0.32, country: "UK" },
    { name: "DAX", value: 16234.56, change: 87.90, changePercent: 0.54, country: "Germany" },
    { name: "NIKKEI", value: 32145.78, change: 156.34, changePercent: 0.49, country: "Japan" },
  ];

  const mockSectorPerformance = [
    { sector: "Technology", change: 2.34, stocks: 150 },
    { sector: "Banking", change: 1.87, stocks: 45 },
    { sector: "Healthcare", change: 1.23, stocks: 67 },
    { sector: "Energy", change: -0.89, stocks: 34 },
    { sector: "Consumer Goods", change: 0.45, stocks: 78 },
    { sector: "Telecommunications", change: -0.23, stocks: 23 },
  ];

  const displayIndices = indices && indices.length > 0 ? indices : mockIndices;
  const displayGainers = gainers && gainers.length > 0 ? gainers : [];
  const displayLosers = losers && losers.length > 0 ? losers : [];

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Markets Overview" />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Market Overview */}
          <MarketOverview />

          {/* Market Tabs */}
          <Tabs defaultValue="indian" className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-dark-secondary">
              <TabsTrigger value="indian" className="data-[state=active]:bg-accent-blue">
                Indian Markets
              </TabsTrigger>
              <TabsTrigger value="global" className="data-[state=active]:bg-accent-blue">
                Global Markets
              </TabsTrigger>
              <TabsTrigger value="sectors" className="data-[state=active]:bg-accent-blue">
                Sectors
              </TabsTrigger>
              <TabsTrigger value="movers" className="data-[state=active]:bg-accent-blue">
                Market Movers
              </TabsTrigger>
            </TabsList>

            <TabsContent value="indian" className="space-y-6">
              <Card className="bg-dark-secondary border-dark-tertiary">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center space-x-2">
                    <Globe className="w-5 h-5" />
                    <span>Indian Market Indices</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {indicesLoading ? (
                      Array(6).fill(0).map((_, i) => (
                        <div key={i} className="p-4 bg-dark-primary rounded-lg">
                          <Skeleton className="h-4 w-20 mb-2" />
                          <Skeleton className="h-8 w-32 mb-2" />
                          <Skeleton className="h-4 w-16" />
                        </div>
                      ))
                    ) : (
                      displayIndices.map((index, i) => (
                        <div key={i} className="p-4 bg-dark-primary rounded-lg hover:bg-dark-tertiary transition-colors">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-semibold text-sm">{index.name}</h3>
                            <Badge variant="outline" className="text-xs">NSE</Badge>
                          </div>
                          <div className="space-y-1">
                            <p className="text-xl font-bold">
                              {formatPrice(index.value, 'INR')}
                            </p>
                            <div className="flex items-center space-x-2">
                              <span className={`text-sm font-semibold ${getChangeColor(index.change)}`}>
                                {index.change >= 0 ? '+' : ''}{index.change.toFixed(2)}
                              </span>
                              <span className={`text-sm ${getChangeColor(index.change)}`}>
                                ({index.changePercent >= 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)
                              </span>
                            </div>
                            {index.volume && (
                              <p className="text-xs text-gray-400">
                                Volume: {(index.volume / 1000000).toFixed(1)}M
                              </p>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="global" className="space-y-6">
              <Card className="bg-dark-secondary border-dark-tertiary">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center space-x-2">
                    <Globe className="w-5 h-5" />
                    <span>Global Market Indices</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {mockGlobalIndices.map((index, i) => (
                      <div key={i} className="p-4 bg-dark-primary rounded-lg hover:bg-dark-tertiary transition-colors">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-sm">{index.name}</h3>
                          <Badge variant="outline" className="text-xs">{index.country}</Badge>
                        </div>
                        <div className="space-y-1">
                          <p className="text-xl font-bold">
                            {formatPrice(index.value, 'USD')}
                          </p>
                          <div className="flex items-center space-x-2">
                            <span className={`text-sm font-semibold ${getChangeColor(index.change)}`}>
                              {index.change >= 0 ? '+' : ''}{index.change.toFixed(2)}
                            </span>
                            <span className={`text-sm ${getChangeColor(index.change)}`}>
                              ({index.changePercent >= 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="sectors" className="space-y-6">
              <Card className="bg-dark-secondary border-dark-tertiary">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center space-x-2">
                    <Activity className="w-5 h-5" />
                    <span>Sector Performance</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {mockSectorPerformance
                      .sort((a, b) => b.change - a.change)
                      .map((sector, i) => (
                        <div key={i} className="flex items-center justify-between p-4 bg-dark-primary rounded-lg">
                          <div className="flex items-center space-x-4">
                            <div className={`w-4 h-4 rounded-full ${sector.change >= 0 ? 'bg-green-500' : 'bg-red-500'}`}></div>
                            <div>
                              <h3 className="font-semibold">{sector.sector}</h3>
                              <p className="text-sm text-gray-400">{sector.stocks} stocks</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="flex items-center space-x-2">
                              {sector.change >= 0 ? (
                                <TrendingUp className="w-4 h-4 text-green-500" />
                              ) : (
                                <TrendingDown className="w-4 h-4 text-red-500" />
                              )}
                              <span className={`font-semibold ${getChangeColor(sector.change)}`}>
                                {sector.change >= 0 ? '+' : ''}{sector.change.toFixed(2)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="movers" className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <MarketMovers type="gainers" />
                <MarketMovers type="losers" />
              </div>

              {/* Market Statistics */}
              <Card className="bg-dark-secondary border-dark-tertiary">
                <CardHeader>
                  <CardTitle className="text-lg font-bold flex items-center space-x-2">
                    <DollarSign className="w-5 h-5" />
                    <span>Market Statistics</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Advancing Stocks</p>
                      <p className="text-2xl font-bold text-green-500">1,234</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Declining Stocks</p>
                      <p className="text-2xl font-bold text-red-500">876</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Unchanged</p>
                      <p className="text-2xl font-bold text-gray-400">345</p>
                    </div>
                    <div className="p-4 bg-dark-primary rounded-lg">
                      <p className="text-sm text-gray-400">Total Volume</p>
                      <p className="text-2xl font-bold">2.45B</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
}
