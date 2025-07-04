interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
}

export class SentimentService {
  analyzeSentiment(text: string): SentimentResult {
    // Simple sentiment analysis based on positive/negative keywords
    const positiveWords = [
      'good', 'great', 'excellent', 'positive', 'bullish', 'strong', 'growth',
      'profit', 'gain', 'increase', 'high', 'up', 'rise', 'surge', 'boom',
      'success', 'achieve', 'beat', 'exceed', 'outperform', 'robust'
    ];

    const negativeWords = [
      'bad', 'terrible', 'negative', 'bearish', 'weak', 'decline', 'loss',
      'fall', 'drop', 'down', 'crash', 'plunge', 'fail', 'miss', 'underperform',
      'concern', 'worry', 'risk', 'threat', 'challenge', 'struggle'
    ];

    const words = text.toLowerCase().split(/\s+/);
    let positiveCount = 0;
    let negativeCount = 0;

    words.forEach(word => {
      if (positiveWords.includes(word)) {
        positiveCount++;
      } else if (negativeWords.includes(word)) {
        negativeCount++;
      }
    });

    const totalSentimentWords = positiveCount + negativeCount;
    if (totalSentimentWords === 0) {
      return { sentiment: 'neutral', score: 0 };
    }

    const score = (positiveCount - negativeCount) / totalSentimentWords;
    
    if (score > 0.1) {
      return { sentiment: 'positive', score };
    } else if (score < -0.1) {
      return { sentiment: 'negative', score };
    } else {
      return { sentiment: 'neutral', score };
    }
  }
}

export const sentimentService = new SentimentService();
