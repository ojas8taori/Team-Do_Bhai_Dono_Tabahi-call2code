import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, getChangeColor } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Plus, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function WatchlistCard() {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: watchlist, isLoading } = useQuery({
    queryKey: ['/api/watchlist'],
    refetchInterval: 30000,
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

  // Mock data for demonstration
  const mockWatchlist = [
    { symbol: "AAPL", name: "Apple Inc.", price: 191.45, change: 2.34, changePercent: 1.24 },
    { symbol: "TSLA", name: "Tesla Inc.", price: 248.87, change: -1.23, changePercent: -0.49 },
    { symbol: "TCS.NS", name: "Tata Consultancy Services", price: 3645.20, change: 0.87, changePercent: 0.02 },
    { symbol: "INFY.NS", name: "Infosys Limited", price: 1521.75, change: 1.45, changePercent: 0.10 },
  ];

  const displayWatchlist = watchlist && watchlist.length > 0 ? watchlist : mockWatchlist;

  if (isLoading) {
    return (
      <Card className="bg-dark-secondary border-dark-tertiary">
        <CardHeader>
          <CardTitle className="text-lg font-bold">My Watchlist</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Array(4).fill(0).map((_, i) => (
              <div key={i} className="flex items-center justify-between p-3">
                <Skeleton className="h-8 w-20" />
                <Skeleton className="h-6 w-16" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-dark-secondary border-dark-tertiary">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-bold">My Watchlist</CardTitle>
          <Button
            size="sm"
            className="text-accent-blue hover:text-blue-400"
            variant="ghost"
          >
            <Plus className="w-4 h-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {displayWatchlist.map((stock, index) => (
            <div 
              key={stock.symbol || index}
              className="flex items-center justify-between p-3 bg-dark-primary rounded-lg hover:bg-dark-tertiary transition-colors cursor-pointer group"
            >
              <div className="flex-1">
                <p className="font-semibold text-sm">{stock.symbol}</p>
                <p className="text-xs text-gray-400">{stock.name}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold">
                  {formatPrice(stock.price, stock.symbol?.includes('.NS') ? 'INR' : 'USD')}
                </p>
                <p className={`text-xs ${getChangeColor(stock.change)}`}>
                  {stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                </p>
              </div>
              <Button
                size="sm"
                variant="ghost"
                className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
                onClick={() => removeMutation.mutate(stock.symbol)}
                disabled={removeMutation.isPending}
              >
                <Trash2 className="w-4 h-4 text-red-400" />
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
