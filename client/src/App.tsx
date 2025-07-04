import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Dashboard from "@/pages/Dashboard";
import Watchlist from "@/pages/Watchlist";
import StockAnalysis from "@/pages/StockAnalysis";
import News from "@/pages/News";
import Portfolio from "@/pages/Portfolio";
import Markets from "@/pages/Markets";
import NotFound from "@/pages/not-found";
import Sidebar from "@/components/Sidebar";

function Router() {
  return (
    <div className="min-h-screen flex bg-dark-primary text-white">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Switch>
          <Route path="/" component={Dashboard} />
          <Route path="/watchlist" component={Watchlist} />
          <Route path="/analysis" component={StockAnalysis} />
          <Route path="/news" component={News} />
          <Route path="/portfolio" component={Portfolio} />
          <Route path="/markets" component={Markets} />
          <Route component={NotFound} />
        </Switch>
      </div>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
