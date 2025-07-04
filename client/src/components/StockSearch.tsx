import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Search, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

interface StockSearchProps {
  onSelect: (symbol: string, name: string) => void;
  onAddToWatchlist?: (symbol: string, market: string) => void;
}

export default function StockSearch({ onSelect, onAddToWatchlist }: StockSearchProps) {
  const [query, setQuery] = useState("");
  const [showResults, setShowResults] = useState(false);

  const { data: results, isLoading } = useQuery({
    queryKey: ['/api/search', query],
    queryFn: () => api.searchSymbols(query),
    enabled: query.length > 2,
  });

  useEffect(() => {
    setShowResults(query.length > 2);
  }, [query]);

  const handleSelect = (symbol: string, name: string) => {
    onSelect(symbol, name);
    setQuery("");
    setShowResults(false);
  };

  const handleAddToWatchlist = (symbol: string, market: string) => {
    if (onAddToWatchlist) {
      onAddToWatchlist(symbol, market);
    }
  };

  return (
    <div className="relative">
      <div className="relative">
        <Input
          type="text"
          placeholder="Search stocks (e.g., AAPL, TSLA, RELIANCE.NS)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-10 bg-dark-primary border-dark-tertiary text-white placeholder-gray-400 focus:border-accent-blue"
        />
        <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
      </div>

      {showResults && (
        <Card className="absolute top-full left-0 right-0 mt-1 bg-dark-secondary border-dark-tertiary max-h-96 overflow-y-auto z-50">
          <CardContent className="p-2">
            {isLoading ? (
              <div className="p-4 text-center text-gray-400">
                Searching...
              </div>
            ) : results && results.length > 0 ? (
              <div className="space-y-1">
                {results.slice(0, 10).map((stock: any, index: number) => (
                  <div
                    key={stock.symbol || index}
                    className="flex items-center justify-between p-3 hover:bg-dark-tertiary rounded-lg cursor-pointer group"
                    onClick={() => handleSelect(stock.symbol, stock.description || stock.name)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-sm">{stock.symbol}</span>
                        <span className="text-xs text-gray-400">
                          {stock.type || stock.exchange}
                        </span>
                      </div>
                      <p className="text-xs text-gray-400 truncate">
                        {stock.description || stock.name}
                      </p>
                    </div>
                    
                    {onAddToWatchlist && (
                      <Button
                        size="sm"
                        variant="ghost"
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleAddToWatchlist(
                            stock.symbol, 
                            stock.symbol.includes('.NS') ? 'NSE' : 'FINNHUB'
                          );
                        }}
                      >
                        <Plus className="w-4 h-4 text-accent-blue" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-4 text-center text-gray-400">
                No results found
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
