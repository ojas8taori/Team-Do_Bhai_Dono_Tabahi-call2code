import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatPrice, formatMarketCap } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface KeyMetricsProps {
  symbol: string;
}

export default function KeyMetrics({ symbol }: KeyMetricsProps) {
  const { data: profile, isLoading } = useQuery({
    queryKey: ['/api/profile', symbol],
    queryFn: () => api.getProfile(symbol),
    enabled: !!symbol,
  });

  const mockMetrics = {
    marketCap: 18120000000000,
    peRatio: 24.67,
    roe: 13.45,
    dividendYield: 0.47,
    high52w: 2968.00,
    low52w: 2220.30,
  };

  if (isLoading) {
    return (
      <Card className="bg-dark-secondary border-dark-tertiary">
        <CardHeader>
          <CardTitle className="text-lg font-bold">Key Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array(6).fill(0).map((_, i) => (
              <div key={i} className="flex justify-between">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-4 w-16" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  const metrics = profile || mockMetrics;

  return (
    <Card className="bg-dark-secondary border-dark-tertiary">
      <CardHeader>
        <CardTitle className="text-lg font-bold">Key Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex justify-between">
            <span className="text-gray-400">Market Cap</span>
            <span className="font-semibold">
              {formatMarketCap(metrics.marketCap || metrics.marketCapitalization)}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">P/E Ratio</span>
            <span className="font-semibold">{metrics.peRatio || 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">ROE</span>
            <span className="font-semibold">{metrics.roe || 'N/A'}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Dividend Yield</span>
            <span className="font-semibold">{metrics.dividendYield || 'N/A'}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">52W High</span>
            <span className="font-semibold">
              {formatPrice(metrics.high52w || 0, symbol.includes('.NS') ? 'INR' : 'USD')}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">52W Low</span>
            <span className="font-semibold">
              {formatPrice(metrics.low52w || 0, symbol.includes('.NS') ? 'INR' : 'USD')}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
