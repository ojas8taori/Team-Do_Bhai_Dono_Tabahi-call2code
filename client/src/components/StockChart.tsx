import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getTimeframeTimestamp } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useState } from "react";
import type { TimeFrame } from "@/types";

interface StockChartProps {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
}

const timeframes: TimeFrame[] = ['1D', '1W', '1M', '3M', '1Y', '5Y'];

export default function StockChart({ symbol, name, price, change, changePercent }: StockChartProps) {
  const [selectedTimeframe, setSelectedTimeframe] = useState<TimeFrame>('1D');
  
  const { from, to } = getTimeframeTimestamp(selectedTimeframe);
  const resolution = selectedTimeframe === '1D' ? '5' : selectedTimeframe === '1W' ? '30' : 'D';

  const { data: chartData, isLoading } = useQuery({
    queryKey: ['/api/candles', symbol, resolution, from, to],
    queryFn: () => api.getCandles(symbol, resolution, from, to),
    enabled: !!symbol,
  });

  const formatChartData = (data: any) => {
    if (!data || !data.t || data.t.length === 0) return [];
    
    return data.t.map((timestamp: number, index: number) => ({
      time: new Date(timestamp * 1000).toLocaleDateString(),
      price: data.c[index],
      high: data.h[index],
      low: data.l[index],
      open: data.o[index],
    }));
  };

  const formattedData = formatChartData(chartData);

  return (
    <Card className="bg-dark-secondary border-dark-tertiary">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-xl font-bold">{symbol}</CardTitle>
            <p className="text-gray-400">{name}</p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold">{price.toFixed(2)}</p>
            <p className={`${change >= 0 ? 'text-success' : 'text-danger'}`}>
              {change >= 0 ? '+' : ''}{change.toFixed(2)} ({changePercent >= 0 ? '+' : ''}{changePercent.toFixed(2)}%)
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {/* Timeframe Selector */}
        <div className="flex items-center space-x-2 mb-4">
          {timeframes.map((timeframe) => (
            <Button
              key={timeframe}
              variant={selectedTimeframe === timeframe ? "default" : "secondary"}
              size="sm"
              onClick={() => setSelectedTimeframe(timeframe)}
              className={
                selectedTimeframe === timeframe
                  ? "bg-accent-blue text-white"
                  : "bg-dark-tertiary text-gray-300 hover:bg-gray-600"
              }
            >
              {timeframe}
            </Button>
          ))}
        </div>

        {/* Chart */}
        <div className="h-96">
          {isLoading ? (
            <div className="h-full flex items-center justify-center">
              <Skeleton className="w-full h-full" />
            </div>
          ) : formattedData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={formattedData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis 
                  dataKey="time" 
                  stroke="#94a3b8"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#94a3b8"
                  fontSize={12}
                  domain={['dataMin - 5', 'dataMax + 5']}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: '#f8fafc'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 4, fill: '#3b82f6' }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <p>No chart data available</p>
                <p className="text-sm">Please try a different symbol or timeframe</p>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
