import { users, watchlists, portfolios, type User, type InsertUser, type Watchlist, type InsertWatchlist, type Portfolio, type InsertPortfolio } from "@shared/schema";

export interface IStorage {
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  getUserWatchlist(userId: number): Promise<Watchlist[]>;
  addToWatchlist(userId: number, watchlistItem: InsertWatchlist): Promise<Watchlist>;
  removeFromWatchlist(userId: number, symbol: string): Promise<void>;
  
  getUserPortfolio(userId: number): Promise<Portfolio[]>;
  addToPortfolio(userId: number, portfolioItem: InsertPortfolio): Promise<Portfolio>;
  updatePortfolio(userId: number, symbol: string, quantity: number, avgPrice: number): Promise<void>;
  removeFromPortfolio(userId: number, symbol: string): Promise<void>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private watchlists: Map<number, Watchlist[]>;
  private portfolios: Map<number, Portfolio[]>;
  private currentId: number;
  private currentWatchlistId: number;
  private currentPortfolioId: number;

  constructor() {
    this.users = new Map();
    this.watchlists = new Map();
    this.portfolios = new Map();
    this.currentId = 1;
    this.currentWatchlistId = 1;
    this.currentPortfolioId = 1;
  }

  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentId++;
    const user: User = { 
      ...insertUser, 
      id,
      createdAt: new Date()
    };
    this.users.set(id, user);
    this.watchlists.set(id, []);
    this.portfolios.set(id, []);
    return user;
  }

  async getUserWatchlist(userId: number): Promise<Watchlist[]> {
    return this.watchlists.get(userId) || [];
  }

  async addToWatchlist(userId: number, watchlistItem: InsertWatchlist): Promise<Watchlist> {
    const userWatchlist = this.watchlists.get(userId) || [];
    const newItem: Watchlist = {
      id: this.currentWatchlistId++,
      userId,
      ...watchlistItem,
      addedAt: new Date()
    };
    userWatchlist.push(newItem);
    this.watchlists.set(userId, userWatchlist);
    return newItem;
  }

  async removeFromWatchlist(userId: number, symbol: string): Promise<void> {
    const userWatchlist = this.watchlists.get(userId) || [];
    const filtered = userWatchlist.filter(item => item.symbol !== symbol);
    this.watchlists.set(userId, filtered);
  }

  async getUserPortfolio(userId: number): Promise<Portfolio[]> {
    return this.portfolios.get(userId) || [];
  }

  async addToPortfolio(userId: number, portfolioItem: InsertPortfolio): Promise<Portfolio> {
    const userPortfolio = this.portfolios.get(userId) || [];
    const newItem: Portfolio = {
      id: this.currentPortfolioId++,
      userId,
      ...portfolioItem,
      createdAt: new Date()
    };
    userPortfolio.push(newItem);
    this.portfolios.set(userId, userPortfolio);
    return newItem;
  }

  async updatePortfolio(userId: number, symbol: string, quantity: number, avgPrice: number): Promise<void> {
    const userPortfolio = this.portfolios.get(userId) || [];
    const item = userPortfolio.find(p => p.symbol === symbol);
    if (item) {
      item.quantity = quantity.toString();
      item.avgPrice = avgPrice.toString();
    }
  }

  async removeFromPortfolio(userId: number, symbol: string): Promise<void> {
    const userPortfolio = this.portfolios.get(userId) || [];
    const filtered = userPortfolio.filter(item => item.symbol !== symbol);
    this.portfolios.set(userId, filtered);
  }
}

export const storage = new MemStorage();
