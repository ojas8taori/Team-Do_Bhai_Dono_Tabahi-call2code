import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { hybridMarketService } from "./services/hybrid-market";
import { sentimentService } from "./services/sentiment";
import { insertWatchlistSchema, insertPortfolioSchema } from "@shared/schema";

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Market Data Routes
  app.get("/api/quote/:symbol", async (req, res) => {
    try {
      const { symbol } = req.params;
      const quote = await hybridMarketService.getQuote(symbol);
      res.json(quote);
    } catch (error) {
      console.error('Error fetching quote:', error);
      res.status(500).json({ error: 'Failed to fetch quote data' });
    }
  });

  app.get("/api/profile/:symbol", async (req, res) => {
    try {
      const { symbol } = req.params;
      const profile = await hybridMarketService.getProfile(symbol);
      res.json(profile);
    } catch (error) {
      console.error('Error fetching profile:', error);
      res.status(500).json({ error: 'Failed to fetch profile data' });
    }
  });

  app.get("/api/news/:symbol", async (req, res) => {
    try {
      const { symbol } = req.params;
      const news = await hybridMarketService.getNews(symbol);
      
      // Add sentiment analysis to news (Alpha Vantage already provides sentiment)
      const newsWithSentiment = news.map((article: any) => ({
        ...article,
        sentiment: article.sentiment || sentimentService.analyzeSentiment(article.headline + ' ' + article.summary)
      }));
      
      res.json(newsWithSentiment);
    } catch (error) {
      console.error('Error fetching news:', error);
      res.status(500).json({ error: 'Failed to fetch news data' });
    }
  });

  app.get("/api/candles/:symbol", async (req, res) => {
    try {
      const { symbol } = req.params;
      const { resolution, from, to } = req.query;
      
      const candles = await hybridMarketService.getCandles(
        symbol, 
        resolution as string, 
        parseInt(from as string), 
        parseInt(to as string)
      );
      
      res.json(candles);
    } catch (error) {
      console.error('Error fetching candles:', error);
      res.status(500).json({ error: 'Failed to fetch candle data' });
    }
  });

  app.get("/api/indices", async (req, res) => {
    try {
      const indices = await hybridMarketService.getIndices();
      res.json(indices);
    } catch (error) {
      console.error('Error fetching indices:', error);
      res.status(500).json({ error: 'Failed to fetch indices data' });
    }
  });

  app.get("/api/gainers", async (req, res) => {
    try {
      const gainers = await hybridMarketService.getGainers();
      res.json(gainers);
    } catch (error) {
      console.error('Error fetching gainers:', error);
      res.status(500).json({ error: 'Failed to fetch gainers data' });
    }
  });

  app.get("/api/losers", async (req, res) => {
    try {
      const losers = await hybridMarketService.getLosers();
      res.json(losers);
    } catch (error) {
      console.error('Error fetching losers:', error);
      res.status(500).json({ error: 'Failed to fetch losers data' });
    }
  });

  app.get("/api/search/:query", async (req, res) => {
    try {
      const { query } = req.params;
      const results = await hybridMarketService.searchSymbols(query);
      res.json(results);
    } catch (error) {
      console.error('Error searching symbols:', error);
      res.status(500).json({ error: 'Failed to search symbols' });
    }
  });

  // Watchlist Routes
  app.get("/api/watchlist", async (req, res) => {
    try {
      // For demo purposes, using user ID 1
      const userId = 1;
      const watchlist = await storage.getUserWatchlist(userId);
      res.json(watchlist);
    } catch (error) {
      console.error('Error fetching watchlist:', error);
      res.status(500).json({ error: 'Failed to fetch watchlist' });
    }
  });

  app.post("/api/watchlist", async (req, res) => {
    try {
      const userId = 1;
      const validatedData = insertWatchlistSchema.parse(req.body);
      const watchlistItem = await storage.addToWatchlist(userId, validatedData);
      res.json(watchlistItem);
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      res.status(500).json({ error: 'Failed to add to watchlist' });
    }
  });

  app.delete("/api/watchlist/:symbol", async (req, res) => {
    try {
      const userId = 1;
      const { symbol } = req.params;
      await storage.removeFromWatchlist(userId, symbol);
      res.json({ success: true });
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      res.status(500).json({ error: 'Failed to remove from watchlist' });
    }
  });

  // Portfolio Routes
  app.get("/api/portfolio", async (req, res) => {
    try {
      const userId = 1;
      const portfolio = await storage.getUserPortfolio(userId);
      res.json(portfolio);
    } catch (error) {
      console.error('Error fetching portfolio:', error);
      res.status(500).json({ error: 'Failed to fetch portfolio' });
    }
  });

  app.post("/api/portfolio", async (req, res) => {
    try {
      const userId = 1;
      const validatedData = insertPortfolioSchema.parse(req.body);
      const portfolioItem = await storage.addToPortfolio(userId, validatedData);
      res.json(portfolioItem);
    } catch (error) {
      console.error('Error adding to portfolio:', error);
      res.status(500).json({ error: 'Failed to add to portfolio' });
    }
  });

  app.delete("/api/portfolio/:symbol", async (req, res) => {
    try {
      const userId = 1;
      const { symbol } = req.params;
      await storage.removeFromPortfolio(userId, symbol);
      res.json({ success: true });
    } catch (error) {
      console.error('Error removing from portfolio:', error);
      res.status(500).json({ error: 'Failed to remove from portfolio' });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
