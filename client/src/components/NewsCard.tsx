import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getSentimentColor } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { ExternalLink } from "lucide-react";

interface NewsCardProps {
  symbol?: string;
  showFilters?: boolean;
}

export default function NewsCard({ symbol, showFilters = true }: NewsCardProps) {
  const { data: news, isLoading } = useQuery({
    queryKey: ['/api/news', symbol || 'general'],
    queryFn: () => symbol ? api.getNews(symbol) : Promise.resolve([]),
    enabled: !!symbol,
  });

  const mockNews = [
    {
      id: '1',
      headline: 'Reliance Industries Reports Strong Q3 Results',
      summary: 'The company posted a 12% increase in net profit compared to the previous quarter...',
      source: 'Economic Times',
      datetime: Date.now() - 2 * 60 * 60 * 1000,
      url: '#',
      sentiment: { sentiment: 'positive', score: 0.7 }
    },
    {
      id: '2',
      headline: 'NIFTY 50 Reaches New All-Time High',
      summary: 'The benchmark index crossed the 20,000 mark for the first time in history...',
      source: 'Bloomberg',
      datetime: Date.now() - 4 * 60 * 60 * 1000,
      url: '#',
      sentiment: { sentiment: 'positive', score: 0.8 }
    },
    {
      id: '3',
      headline: 'Tech Stocks Face Pressure Amid Rising Rates',
      summary: 'IT companies see decline as investors shift focus to value stocks...',
      source: 'Reuters',
      datetime: Date.now() - 6 * 60 * 60 * 1000,
      url: '#',
      sentiment: { sentiment: 'negative', score: -0.6 }
    },
  ];

  const displayNews = news && news.length > 0 ? news.slice(0, 3) : mockNews;

  const formatTimeAgo = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Just now';
    if (hours === 1) return '1 hour ago';
    return `${hours} hours ago`;
  };

  if (isLoading) {
    return (
      <Card className="bg-dark-secondary border-dark-tertiary">
        <CardHeader>
          <CardTitle className="text-lg font-bold">Market News</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array(3).fill(0).map((_, i) => (
              <div key={i} className="bg-dark-primary rounded-lg p-4">
                <Skeleton className="h-4 w-full mb-2" />
                <Skeleton className="h-3 w-3/4 mb-2" />
                <Skeleton className="h-3 w-1/2" />
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
          <CardTitle className="text-lg font-bold">Market News</CardTitle>
          {showFilters && (
            <div className="flex items-center space-x-2">
              <Button size="sm" className="bg-accent-blue text-white">All</Button>
              <Button size="sm" variant="secondary" className="bg-dark-tertiary text-gray-300">
                {symbol || 'Tech'}
              </Button>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayNews.map((article) => (
            <div 
              key={article.id}
              className="bg-dark-primary rounded-lg p-4 hover:bg-dark-tertiary transition-colors cursor-pointer group"
            >
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-accent-blue rounded-full mt-2 flex-shrink-0"></div>
                <div className="flex-1">
                  <h4 className="font-semibold text-sm mb-2 group-hover:text-accent-blue transition-colors">
                    {article.headline}
                  </h4>
                  <p className="text-xs text-gray-400 mb-3 line-clamp-2">
                    {article.summary}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      {formatTimeAgo(article.datetime)}
                    </span>
                    <div className="flex items-center space-x-2">
                      <Badge 
                        className={`text-xs px-2 py-1 ${getSentimentColor(article.sentiment.sentiment)}`}
                        variant="secondary"
                      >
                        {article.sentiment.sentiment}
                      </Badge>
                      <ExternalLink className="w-3 h-3 text-gray-400" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
