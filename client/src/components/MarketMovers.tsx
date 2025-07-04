import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, getChangeColor } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface MarketMoversProps {
  type: 'gainers' | 'losers';
}

export default function MarketMovers({ type }: MarketMoversProps) {
  const { data: movers, isLoading } = useQuery({
    queryKey: [`/api/${type}`],
    refetchInterval: 60000, // Refresh every minute
  });

  const mockGainers = [
    { symbol: "ADANIPORTS.NS", name: "Adani Ports", price: 1234.50, changePercent: 8.45 },
    { symbol: "HDFCBANK.NS", name: "HDFC Bank", price: 1672.25, changePercent: 6.32 },
    { symbol: "WIPRO.NS", name: "Wipro Limited", price: 456.80, changePercent: 5.67 },
  ];

  const mockLosers = [
    { symbol: "BAJFINANCE.NS", name: "Bajaj Finance", price: 6789.45, changePercent: -4.56 },
    { symbol: "MARUTI.NS", name: "Maruti Suzuki", price: 10234.60, changePercent: -3.78 },
    { symbol: "BRITANNIA.NS", name: "Britannia Industries", price: 4567.25, changePercent: -2.91 },
  ];

  const mockData = type === 'gainers' ? mockGainers : mockLosers;
  const displayData = movers && movers.length > 0 ? movers.slice(0, 3) : mockData;

  if (isLoading) {
    return (
      <Card className="bg-dark-secondary border-dark-tertiary">
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            Top {type === 'gainers' ? 'Gainers' : 'Losers'} (NSE)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Array(3).fill(0).map((_, i) => (
              <div key={i} className="flex items-center justify-between p-3">
                <Skeleton className="h-8 w-32" />
                <Skeleton className="h-6 w-20" />
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
        <CardTitle className="text-lg font-bold">
          Top {type === 'gainers' ? 'Gainers' : 'Losers'} (NSE)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {displayData.map((stock, index) => (
            <div 
              key={stock.symbol || index}
              className="flex items-center justify-between p-3 bg-dark-primary rounded-lg"
            >
              <div>
                <p className="font-semibold text-sm">{stock.symbol}</p>
                <p className="text-xs text-gray-400">{stock.name}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold">
                  {formatPrice(stock.ltp || stock.price || 0, 'INR')}
                </p>
                <p className={`text-xs font-semibold ${getChangeColor(stock.perChange || stock.changePercent || 0)}`}>
                  {(stock.perChange || stock.changePercent || 0) >= 0 ? '+' : ''}{(stock.perChange || stock.changePercent || 0).toFixed(2)}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
