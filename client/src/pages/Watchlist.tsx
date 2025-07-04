import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, getChangeColor } from "@/lib/utils";
import Header from "@/components/Header";
import StockSearch from "@/components/StockSearch";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Trash2, Plus, TrendingUp, TrendingDown } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Watchlist() {
  const [showSearch, setShowSearch] = useState(false);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: watchlist, isLoading } = useQuery({
    queryKey: ['/api/watchlist'],
    refetchInterval: 30000,
  });

  const addMutation = useMutation({
    mutationFn: ({ symbol, market }: { symbol: string; market: string }) => 
      api.addToWatchlist(symbol, market),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/watchlist'] });
      toast({
        title: "Success",
        description: "Stock added to watchlist",
      });
      setShowSearch(false);
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to add stock to watchlist",
        variant: "destructive",
      });
    },
  });

  const removeMutation = useMutation({
    mutationFn: (symbol: string) => api.removeFromWatchlist(symbol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/watchlist'] });
      toast({
        title: "Success",
        description: "Stock removed from watchlist",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to remove stock from watchlist",
        variant: "destructive",
      });
    },
  });

  const handleAddToWatchlist = (symbol: string, market: string) => {
    addMutation.mutate({ symbol, market });
  };

  const handleRemoveFromWatchlist = (symbol: string) => {
    removeMutation.mutate(symbol);
  };

  // Mock data for demonstration
  const mockWatchlist = [
    { 
      symbol: "AAPL", 
      market: "FINNHUB",
      name: "Apple Inc.", 
      price: 191.45, 
      change: 2.34, 
      changePercent: 1.24,
      addedAt: new Date().toISOString()
    },
    { 
      symbol: "TSLA", 
      market: "FINNHUB",
      name: "Tesla Inc.", 
      price: 248.87, 
      change: -1.23, 
      changePercent: -0.49,
      addedAt: new Date().toISOString()
    },
    { 
      symbol: "TCS.NS", 
      market: "NSE",
      name: "Tata Consultancy Services", 
      price: 3645.20, 
      change: 0.87, 
      changePercent: 0.02,
      addedAt: new Date().toISOString()
    },
    { 
      symbol: "INFY.NS", 
      market: "NSE",
      name: "Infosys Limited", 
      price: 1521.75, 
      change: 1.45, 
      changePercent: 0.10,
      addedAt: new Date().toISOString()
    },
  ];

  const displayWatchlist = watchlist && watchlist.length > 0 ? watchlist : mockWatchlist;

  return (
    <div className="flex-1 flex flex-col">
      <Header title="My Watchlist" />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          {/* Add Stock Section */}
          <div className="mb-6">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-bold">Add Stocks to Watchlist</CardTitle>
                  <Button
                    onClick={() => setShowSearch(!showSearch)}
                    className="bg-accent-blue text-white hover:bg-blue-600"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Stock
                  </Button>
                </div>
              </CardHeader>
              {showSearch && (
                <CardContent>
                  <StockSearch
                    onSelect={(symbol, name) => {
                      const market = symbol.includes('.NS') ? 'NSE' : 'FINNHUB';
                      handleAddToWatchlist(symbol, market);
                    }}
                    onAddToWatchlist={handleAddToWatchlist}
                  />
                </CardContent>
              )}
            </Card>
          </div>

          {/* Watchlist Table */}
          <Card className="bg-dark-secondary border-dark-tertiary">
            <CardHeader>
              <CardTitle className="text-lg font-bold">
                Your Watchlist ({displayWatchlist.length} stocks)
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-4">
                  {Array(5).fill(0).map((_, i) => (
                    <div key={i} className="flex items-center justify-between p-4 bg-dark-primary rounded-lg">
                      <div className="flex items-center space-x-4">
                        <Skeleton className="h-8 w-16" />
                        <Skeleton className="h-6 w-32" />
                      </div>
                      <Skeleton className="h-6 w-20" />
                    </div>
                  ))}
                </div>
              ) : displayWatchlist.length === 0 ? (
                <div className="text-center py-12">
                  <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No stocks in your watchlist</h3>
                  <p className="text-gray-400 mb-4">Add stocks to track their performance</p>
                  <Button
                    onClick={() => setShowSearch(true)}
                    className="bg-accent-blue text-white hover:bg-blue-600"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Your First Stock
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {displayWatchlist.map((stock) => (
                    <div
                      key={stock.symbol}
                      className="flex items-center justify-between p-4 bg-dark-primary rounded-lg hover:bg-dark-tertiary transition-colors group"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2">
                          <span className="font-bold text-lg">{stock.symbol}</span>
                          <Badge variant="outline" className="text-xs">
                            {stock.market}
                          </Badge>
                        </div>
                        <div>
                          <p className="text-sm text-gray-400">{stock.name}</p>
                          <p className="text-xs text-gray-500">
                            Added {new Date(stock.addedAt).toLocaleDateString()}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-6">
                        <div className="text-right">
                          <p className="text-lg font-semibold">
                            {formatPrice(stock.price, stock.symbol.includes('.NS') ? 'INR' : 'USD')}
                          </p>
                          <div className="flex items-center space-x-1">
                            {stock.change > 0 ? (
                              <TrendingUp className="w-4 h-4 text-green-500" />
                            ) : (
                              <TrendingDown className="w-4 h-4 text-red-500" />
                            )}
                            <span className={`text-sm ${getChangeColor(stock.change)}`}>
                              {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)} ({stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%)
                            </span>
                          </div>
                        </div>

                        <Button
                          size="sm"
                          variant="ghost"
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => handleRemoveFromWatchlist(stock.symbol)}
                          disabled={removeMutation.isPending}
                        >
                          <Trash2 className="w-4 h-4 text-red-400" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
