import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, formatChange, getChangeColor } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

const mockIndices = [
  { name: "NIFTY 50", value: 19674.25, change: 127.45, changePercent: 0.65 },
  { name: "SENSEX", value: 66795.14, change: 421.87, changePercent: 0.64 },
  { name: "S&P 500", value: 4765.20, change: -12.45, changePercent: -0.26 },
  { name: "NASDAQ", value: 15047.70, change: 65.12, changePercent: 0.43 },
];

export default function MarketOverview() {
  const { data: indices, isLoading, error } = useQuery({
    queryKey: ['/api/indices'],
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {Array(4).fill(0).map((_, i) => (
          <Card key={i} className="bg-dark-secondary border-dark-tertiary">
            <CardContent className="p-6">
              <Skeleton className="h-4 w-20 mb-2" />
              <Skeleton className="h-8 w-32 mb-2" />
              <Skeleton className="h-4 w-16" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    console.error('Error fetching indices:', error);
    // Use mock data as fallback
  }

  const displayIndices = indices && indices.length > 0 ? indices.slice(0, 4) : mockIndices;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {displayIndices.map((index, i) => (
        <Card key={i} className="bg-dark-secondary border-dark-tertiary">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">{index.name}</p>
                <p className="text-2xl font-bold">
                  {formatPrice(index.value, index.name.includes('NIFTY') || index.name.includes('SENSEX') ? 'INR' : 'USD')}
                </p>
              </div>
              <div className="text-right">
                <p className={`text-sm font-semibold ${getChangeColor(index.change)}`}>
                  {index.change >= 0 ? '+' : ''}{index.change.toFixed(2)}
                </p>
                <p className={`text-sm ${getChangeColor(index.change)}`}>
                  {index.changePercent >= 0 ? '+' : ''}{index.changePercent.toFixed(2)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
