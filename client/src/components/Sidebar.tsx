import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";
import { 
  ChartPie, 
  Star, 
  Search, 
  Newspaper, 
  Briefcase, 
  Globe, 
  TrendingUp,
  User
} from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/", icon: ChartPie },
  { name: "Watchlist", href: "/watchlist", icon: Star },
  { name: "Stock Analysis", href: "/analysis", icon: Search },
  { name: "News", href: "/news", icon: Newspaper },
  { name: "Portfolio", href: "/portfolio", icon: Briefcase },
  { name: "Markets", href: "/markets", icon: Globe },
];

export default function Sidebar() {
  const [location] = useLocation();

  return (
    <div className="w-64 bg-dark-secondary border-r border-dark-tertiary flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-dark-tertiary">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-accent-blue rounded-lg flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-bold">StockVision Pro</h1>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon;
          const isActive = location === item.href;
          
          return (
            <Link key={item.name} href={item.href}>
              <div
                className={cn(
                  "flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors cursor-pointer",
                  isActive
                    ? "bg-accent-blue text-white"
                    : "text-gray-300 hover:bg-dark-tertiary"
                )}
              >
                <Icon className="w-5 h-5" />
                <span>{item.name}</span>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-dark-tertiary">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
            <User className="w-4 h-4" />
          </div>
          <div>
            <p className="text-sm font-medium">John Trader</p>
            <p className="text-xs text-gray-400">Premium User</p>
          </div>
        </div>
      </div>
    </div>
  );
}
