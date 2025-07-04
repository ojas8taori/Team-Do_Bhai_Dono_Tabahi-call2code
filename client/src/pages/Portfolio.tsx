import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, getChangeColor, formatVolume } from "@/lib/utils";
import Header from "@/components/Header";
import StockSearch from "@/components/StockSearch";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Trash2, Plus, TrendingUp, TrendingDown, PieChart, DollarSign } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Portfolio() {
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [selectedStock, setSelectedStock] = useState({ symbol: "", name: "" });
  const [quantity, setQuantity] = useState("");
  const [avgPrice, setAvgPrice] = useState("");
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: portfolio, isLoading } = useQuery({
    queryKey: ['/api/portfolio'],
    refetchInterval: 30000,
  });

  const addMutation = useMutation({
    mutationFn: ({ symbol, quantity, avgPrice, market }: { symbol: string; quantity: number; avgPrice: number; market: string }) => 
      api.addToPortfolio(symbol, quantity, avgPrice, market),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/portfolio'] });
      toast({
        title: "Success",
        description: "Stock added to portfolio",
      });
      setShowAddDialog(false);
      setSelectedStock({ symbol: "", name: "" });
      setQuantity("");
      setAvgPrice("");
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to add stock to portfolio",
        variant: "destructive",
      });
    },
  });

  const removeMutation = useMutation({
    mutationFn: (symbol: string) => api.removeFromPortfolio(symbol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/portfolio'] });
      toast({
        title: "Success",
        description: "Stock removed from portfolio",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to remove stock from portfolio",
        variant: "destructive",
      });
    },
  });

  const handleAddStock = () => {
    if (!selectedStock.symbol || !quantity || !avgPrice) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }

    const market = selectedStock.symbol.includes('.NS') ? 'NSE' : 'FINNHUB';
    addMutation.mutate({
      symbol: selectedStock.symbol,
      quantity: parseFloat(quantity),
      avgPrice: parseFloat(avgPrice),
      market
    });
  };

  const handleStockSelect = (symbol: string, name: string) => {
    setSelectedStock({ symbol, name });
  };

  const handleRemoveStock = (symbol: string) => {
    removeMutation.mutate(symbol);
  };

  // Mock data for demonstration purposes
  const mockPortfolio = [
    {
      symbol: "AAPL",
      quantity: "50",
      avgPrice: "150.00",
      market: "FINNHUB",
      currentPrice: 191.45,
      change: 2.34,
      changePercent: 1.24,
      createdAt: new Date().toISOString()
    },
    {
      symbol: "TSLA",
      quantity: "25",
      avgPrice: "200.00",
      market: "FINNHUB",
      currentPrice: 248.87,
      change: -1.23,
      changePercent: -0.49,
      createdAt: new Date().toISOString()
    },
    {
      symbol: "RELIANCE.NS",
      quantity: "100",
      avgPrice: "2500.00",
      market: "NSE",
      currentPrice: 2847.50,
      change: 45.25,
      changePercent: 1.62,
      createdAt: new Date().toISOString()
    },
  ];

  const displayPortfolio = portfolio && portfolio.length > 0 ? portfolio : mockPortfolio;

  // Calculate portfolio metrics
  const portfolioMetrics = displayPortfolio.reduce((acc, stock) => {
    const qty = parseFloat(stock.quantity);
    const avgPrice = parseFloat(stock.avgPrice);
    const currentPrice = stock.currentPrice;
    const invested = qty * avgPrice;
    const currentValue = qty * currentPrice;
    const gainLoss = currentValue - invested;

    acc.totalInvested += invested;
    acc.totalCurrentValue += currentValue;
    acc.totalGainLoss += gainLoss;

    return acc;
  }, { totalInvested: 0, totalCurrentValue: 0, totalGainLoss: 0 });

  const portfolioChangePercent = portfolioMetrics.totalInvested > 0 
    ? ((portfolioMetrics.totalGainLoss / portfolioMetrics.totalInvested) * 100) 
    : 0;

  return (
    <div className="flex-1 flex flex-col">
      <Header title="My Portfolio" />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          {/* Portfolio Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Invested</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {formatPrice(portfolioMetrics.totalInvested, 'USD')}
                </div>
                <p className="text-xs text-muted-foreground">
                  Your initial investment
                </p>
              </CardContent>
            </Card>

            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Current Value</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {formatPrice(portfolioMetrics.totalCurrentValue, 'USD')}
                </div>
                <p className="text-xs text-muted-foreground">
                  Current market value
                </p>
              </CardContent>
            </Card>

            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Gain/Loss</CardTitle>
                <PieChart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className={`text-2xl font-bold ${getChangeColor(portfolioMetrics.totalGainLoss)}`}>
                  {portfolioMetrics.totalGainLoss >= 0 ? '+' : ''}{formatPrice(portfolioMetrics.totalGainLoss, 'USD')}
                </div>
                <p className={`text-xs ${getChangeColor(portfolioMetrics.totalGainLoss)}`}>
                  {portfolioChangePercent >= 0 ? '+' : ''}{portfolioChangePercent.toFixed(2)}%
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Add Stock Dialog */}
          <div className="mb-6">
            <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
              <DialogTrigger asChild>
                <Button className="bg-accent-blue text-white hover:bg-blue-600">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Stock to Portfolio
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-dark-secondary border-dark-tertiary">
                <DialogHeader>
                  <DialogTitle>Add Stock to Portfolio</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="stock-search">Search Stock</Label>
                    <StockSearch
                      onSelect={handleStockSelect}
                    />
                    {selectedStock.symbol && (
                      <p className="text-sm text-gray-400 mt-2">
                        Selected: {selectedStock.symbol} - {selectedStock.name}
                      </p>
                    )}
                  </div>
                  
                  <div>
                    <Label htmlFor="quantity">Quantity</Label>
                    <Input
                      id="quantity"
                      type="number"
                      value={quantity}
                      onChange={(e) => setQuantity(e.target.value)}
                      className="bg-dark-primary border-dark-tertiary"
                      placeholder="Enter quantity"
                    />
                  </div>

                  <div>
                    <Label htmlFor="avg-price">Average Price</Label>
                    <Input
                      id="avg-price"
                      type="number"
                      step="0.01"
                      value={avgPrice}
                      onChange={(e) => setAvgPrice(e.target.value)}
                      className="bg-dark-primary border-dark-tertiary"
                      placeholder="Enter average price"
                    />
                  </div>

                  <Button
                    onClick={handleAddStock}
                    disabled={addMutation.isPending}
                    className="w-full bg-accent-blue text-white hover:bg-blue-600"
                  >
                    {addMutation.isPending ? "Adding..." : "Add to Portfolio"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Portfolio Holdings */}
          <Card className="bg-dark-secondary border-dark-tertiary">
            <CardHeader>
              <CardTitle className="text-lg font-bold">
                Portfolio Holdings ({displayPortfolio.length} stocks)
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-4">
                  {Array(3).fill(0).map((_, i) => (
                    <div key={i} className="flex items-center justify-between p-4 bg-dark-primary rounded-lg">
                      <div className="flex items-center space-x-4">
                        <Skeleton className="h-8 w-16" />
                        <Skeleton className="h-6 w-32" />
                      </div>
                      <Skeleton className="h-6 w-20" />
                    </div>
                  ))}
                </div>
              ) : displayPortfolio.length === 0 ? (
                <div className="text-center py-12">
                  <PieChart className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No stocks in your portfolio</h3>
                  <p className="text-gray-400 mb-4">Add stocks to track your investment performance</p>
                  <Button
                    onClick={() => setShowAddDialog(true)}
                    className="bg-accent-blue text-white hover:bg-blue-600"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Your First Stock
                  </Button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="text-left text-sm text-gray-400 border-b border-dark-tertiary">
                        <th className="pb-3">Symbol</th>
                        <th className="pb-3">Quantity</th>
                        <th className="pb-3">Avg Price</th>
                        <th className="pb-3">Current Price</th>
                        <th className="pb-3">Market Value</th>
                        <th className="pb-3">Gain/Loss</th>
                        <th className="pb-3">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {displayPortfolio.map((stock) => {
                        const qty = parseFloat(stock.quantity);
                        const avgPrice = parseFloat(stock.avgPrice);
                        const currentPrice = stock.currentPrice;
                        const marketValue = qty * currentPrice;
                        const invested = qty * avgPrice;
                        const gainLoss = marketValue - invested;
                        const gainLossPercent = ((gainLoss / invested) * 100);

                        return (
                          <tr key={stock.symbol} className="border-b border-dark-tertiary/50 hover:bg-dark-tertiary/20">
                            <td className="py-4">
                              <div className="flex items-center space-x-2">
                                <span className="font-semibold">{stock.symbol}</span>
                                <Badge variant="outline" className="text-xs">
                                  {stock.market}
                                </Badge>
                              </div>
                            </td>
                            <td className="py-4">{formatVolume(qty)}</td>
                            <td className="py-4">
                              {formatPrice(avgPrice, stock.symbol.includes('.NS') ? 'INR' : 'USD')}
                            </td>
                            <td className="py-4">
                              <div>
                                <div className="font-semibold">
                                  {formatPrice(currentPrice, stock.symbol.includes('.NS') ? 'INR' : 'USD')}
                                </div>
                                <div className={`text-sm ${getChangeColor(stock.change)}`}>
                                  {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)} ({stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%)
                                </div>
                              </div>
                            </td>
                            <td className="py-4 font-semibold">
                              {formatPrice(marketValue, stock.symbol.includes('.NS') ? 'INR' : 'USD')}
                            </td>
                            <td className="py-4">
                              <div className={`${getChangeColor(gainLoss)}`}>
                                <div className="font-semibold">
                                  {gainLoss >= 0 ? '+' : ''}{formatPrice(gainLoss, stock.symbol.includes('.NS') ? 'INR' : 'USD')}
                                </div>
                                <div className="text-sm">
                                  {gainLossPercent >= 0 ? '+' : ''}{gainLossPercent.toFixed(2)}%
                                </div>
                              </div>
                            </td>
                            <td className="py-4">
                              <Button
                                size="sm"
                                variant="ghost"
                                onClick={() => handleRemoveStock(stock.symbol)}
                                disabled={removeMutation.isPending}
                              >
                                <Trash2 className="w-4 h-4 text-red-400" />
                              </Button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
