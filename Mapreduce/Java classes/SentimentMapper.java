package Sentiment_Analysis;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class SentimentMapper extends Mapper<Object, Text, Text, IntWritable> {

    private Text sentimentKey = new Text();
    private boolean isHeader = true;  // Skip the first row (header)

    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();

        // Skip the header row
        if (isHeader) {
            isHeader = false;
            return;
        }

        // Split the CSV line by commas (or use your delimiter if different)
        String[] fields = line.split(",", -1);

        // Ensure there are enough columns for ID and reviewText
        if (fields.length > 1) {
            String id = fields[0].trim();  // ID column
            String reviewText = fields[1].toLowerCase().trim();  // reviewText column

            // Set the ID as the key for output
            sentimentKey.set(id);

            // Calculate sentiment score
            int score = calculateSentimentScore(reviewText);
            context.write(sentimentKey, new IntWritable(score));  // Emit sentiment score
        }
    }

    // Helper function to calculate sentiment score
    private int calculateSentimentScore(String reviewText) {
        int score = 0;

        // Simple keyword-based scoring logic
        if (isPositiveReview(reviewText)) {
            score++;
        }
        if (isNegativeReview(reviewText)) {
            score--;
        }

        return score;
    }

    // Helper function to detect positive sentiment
    private boolean isPositiveReview(String reviewText) {
        // Define simple positive words
        String[] positiveWords = {"good", "great", "excellent", "happy", "love", "best", "fantastic", "amazing"};
        
        for (String word : positiveWords) {
            if (reviewText.contains(word)) {
                return true;  // Positive sentiment found
            }
        }
        return false;
    }

    // Helper function to detect negative sentiment
    private boolean isNegativeReview(String reviewText) {
        // Define simple negative words
        String[] negativeWords = {"bad", "poor", "terrible", "hate", "worst", "awful", "disappointing", "not good"};

        for (String word : negativeWords) {
            if (reviewText.contains(word)) {
                return true;  // Negative sentiment found
            }
        }
        return false;
    }
}
