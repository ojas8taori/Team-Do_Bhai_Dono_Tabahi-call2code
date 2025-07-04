import { Search, Clock } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useState, useEffect } from "react";

interface HeaderProps {
  title: string;
  onSearch?: (query: string) => void;
}

export default function Header({ title, onSearch }: HeaderProps) {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    if (onSearch) {
      onSearch(query);
    }
  };

  return (
    <header className="bg-dark-secondary border-b border-dark-tertiary p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <h2 className="text-2xl font-bold">{title}</h2>
          <div className="flex items-center space-x-2 text-sm text-gray-400">
            <Clock className="w-4 h-4" />
            <span>{currentTime.toLocaleTimeString('en-US', { 
              hour: '2-digit', 
              minute: '2-digit', 
              second: '2-digit',
              hour12: true 
            })}</span>
            <span className="w-2 h-2 bg-success rounded-full animate-pulse"></span>
            <span>Live</span>
          </div>
        </div>
        
        {onSearch && (
          <div className="relative">
            <Input
              type="text"
              placeholder="Search stocks (e.g., AAPL, TSLA, RELIANCE.NS)"
              value={searchQuery}
              onChange={handleSearchChange}
              className="w-96 pl-10 bg-dark-primary border-dark-tertiary text-white placeholder-gray-400 focus:border-accent-blue"
            />
            <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
          </div>
        )}
      </div>
    </header>
  );
}
