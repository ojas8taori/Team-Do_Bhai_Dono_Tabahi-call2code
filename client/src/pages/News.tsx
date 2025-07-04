import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getSentimentColor } from "@/lib/utils";
import Header from "@/components/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { ExternalLink, Search, Calendar, TrendingUp, TrendingDown } from "lucide-react";

export default function News() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");

  const { data: news, isLoading } = useQuery({
    queryKey: ['/api/news', searchQuery || 'general'],
    queryFn: () => searchQuery ? api.getNews(searchQuery) : Promise.resolve([]),
    enabled: !!searchQuery,
  });

  const mockNews = [
    {
      id: '1',
      headline: 'Reliance Industries Reports Strong Q3 Results',
      summary: 'The company posted a 12% increase in net profit compared to the previous quarter, beating analyst expectations. Revenue grew by 8% year-over-year.',
      source: 'Economic Times',
      datetime: Date.now() - 2 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'earnings',
      sentiment: { sentiment: 'positive', score: 0.7 }
    },
    {
      id: '2',
      headline: 'NIFTY 50 Reaches New All-Time High',
      summary: 'The benchmark index crossed the 20,000 mark for the first time in history, driven by strong performance in banking and technology sectors.',
      source: 'Bloomberg',
      datetime: Date.now() - 4 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'market',
      sentiment: { sentiment: 'positive', score: 0.8 }
    },
    {
      id: '3',
      headline: 'Tech Stocks Face Pressure Amid Rising Rates',
      summary: 'IT companies see decline as investors shift focus to value stocks. Rising interest rates impact growth stock valuations.',
      source: 'Reuters',
      datetime: Date.now() - 6 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'technology',
      sentiment: { sentiment: 'negative', score: -0.6 }
    },
    {
      id: '4',
      headline: 'Indian Rupee Strengthens Against Dollar',
      summary: 'The rupee gained 0.3% against the dollar today, supported by strong foreign investment inflows and positive economic indicators.',
      source: 'Mint',
      datetime: Date.now() - 8 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'currency',
      sentiment: { sentiment: 'positive', score: 0.5 }
    },
    {
      id: '5',
      headline: 'Oil Prices Surge on Supply Concerns',
      summary: 'Crude oil prices jumped 3% as geopolitical tensions raise concerns about supply disruptions. This impacts energy sector stocks.',
      source: 'CNBC',
      datetime: Date.now() - 10 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'commodities',
      sentiment: { sentiment: 'neutral', score: 0.1 }
    },
    {
      id: '6',
      headline: 'Banking Sector Shows Robust Growth',
      summary: 'Major banks report strong quarterly results with improved asset quality and higher net interest margins driving profitability.',
      source: 'Business Standard',
      datetime: Date.now() - 12 * 60 * 60 * 1000,
      url: '#',
      image: '',
      category: 'banking',
      sentiment: { sentiment: 'positive', score: 0.6 }
    }
  ];

  const displayNews = news && news.length > 0 ? news : mockNews;

  const categories = [
    { id: 'all', name: 'All News', icon: TrendingUp },
    { id: 'market', name: 'Market', icon: TrendingUp },
    { id: 'earnings', name: 'Earnings', icon: TrendingUp },
    { id: 'technology', name: 'Technology', icon: TrendingUp },
    { id: 'banking', name: 'Banking', icon: TrendingUp },
    { id: 'commodities', name: 'Commodities', icon: TrendingDown },
  ];

  const filteredNews = selectedCategory === 'all' 
    ? displayNews 
    : displayNews.filter(article => article.category === selectedCategory);

  const formatTimeAgo = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours < 1) return 'Just now';
    if (hours === 1) return '1 hour ago';
    return `${hours} hours ago`;
  };

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Market News" />
      
      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          {/* Search and Filters */}
          <div className="mb-6 space-y-4">
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardContent className="p-4">
                <div className="flex items-center space-x-4">
                  <div className="relative flex-1">
                    <Input
                      type="text"
                      placeholder="Search news by stock symbol (e.g., RELIANCE, AAPL)"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10 bg-dark-primary border-dark-tertiary text-white placeholder-gray-400"
                    />
                    <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Category Filters */}
            <Card className="bg-dark-secondary border-dark-tertiary">
              <CardContent className="p-4">
                <div className="flex flex-wrap gap-2">
                  {categories.map((category) => (
                    <Button
                      key={category.id}
                      variant={selectedCategory === category.id ? "default" : "secondary"}
                      size="sm"
                      onClick={() => setSelectedCategory(category.id)}
                      className={
                        selectedCategory === category.id
                          ? "bg-accent-blue text-white"
                          : "bg-dark-tertiary text-gray-300 hover:bg-gray-600"
                      }
                    >
                      {category.name}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* News Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {isLoading ? (
              Array(6).fill(0).map((_, i) => (
                <Card key={i} className="bg-dark-secondary border-dark-tertiary">
                  <CardContent className="p-6">
                    <Skeleton className="h-4 w-full mb-3" />
                    <Skeleton className="h-3 w-3/4 mb-4" />
                    <div className="flex items-center justify-between">
                      <Skeleton className="h-3 w-20" />
                      <Skeleton className="h-5 w-16" />
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : filteredNews.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No news found</h3>
                <p className="text-gray-400">Try searching for a different stock symbol</p>
              </div>
            ) : (
              filteredNews.map((article) => (
                <Card key={article.id} className="bg-dark-secondary border-dark-tertiary hover:border-accent-blue/50 transition-colors">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg font-semibold mb-2 line-clamp-2">
                          {article.headline}
                        </CardTitle>
                        <div className="flex items-center space-x-2 text-sm text-gray-400">
                          <Calendar className="w-4 h-4" />
                          <span>{formatTimeAgo(article.datetime)}</span>
                          <span>•</span>
                          <span>{article.source}</span>
                        </div>
                      </div>
                      <Badge 
                        className={`ml-2 ${getSentimentColor(article.sentiment.sentiment)}`}
                        variant="secondary"
                      >
                        {article.sentiment.sentiment}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-300 mb-4 line-clamp-3">
                      {article.summary}
                    </p>
                    <div className="flex items-center justify-between">
                      <Badge variant="outline" className="text-xs">
                        {article.category}
                      </Badge>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-accent-blue hover:text-blue-400"
                        onClick={() => window.open(article.url, '_blank')}
                      >
                        <ExternalLink className="w-4 h-4 mr-1" />
                        Read More
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
