from mrjob.job import MRJob
import pandas as pd
import matplotlib.pyplot as plt
import re

# Regular expression to get clean words (removing punctuation)
WORD_RE = re.compile(r"[\w']+")

class InvertedIndexAndFrequency(MRJob):
    
    def mapper_init(self):
        # Initialize a line counter for this split/file mapper instance
        self.line_number = 0

    def mapper(self, _, line):
        self.line_number += 1
        # break down line into individual clean words 
        for word in WORD_RE.findall(line):
            word_lower = word.lower()
            # Yield word as key, and a dictionary containing line occurrence and a count of 1
            yield (word_lower, {"line": self.line_number, "count": 1})
              
    def reducer(self, word, values):
        total_count = 0
        lines_found = set() #datatype store an unordered collection of unique items
        
        # add counts and unique line numbers for each word
        for val in values:
            total_count += val["count"]
            lines_found.add(val["line"])
            
        # Yield the word mapping to its frequency and sorted list of lines
        yield (word, {"count": total_count, "lines": sorted(list(lines_found))})

if __name__ == '__main__':
    # Simulating data execution using 'inputtext1.txt'
    mr_job = InvertedIndexAndFrequency(args=['inputtext1.txt'])
    results = []
    
    with mr_job.make_runner() as runner:
        runner.run()
        for key, value in mr_job.parse_output(runner.cat_output()):
            results.append({
                'word': key, 
                'count': value['count'], 
                'lines': value['lines']
            })
            
    #print the sample inverted index dictionary items
    print("Inverted Index Sample (First 5):")
    print(results[:5])
    
    #build Pandas DataFrame
    wordCount_df = pd.DataFrame(results)
    
    print("\nPandas DataFrame Head (Inverted Index Mapping):")
    print(wordCount_df[['word', 'lines', 'count']].head())
    
    # display chart of frequently occuring words
    top_words = wordCount_df.sort_values(by="count", ascending=False).head(10)
    print("\nTop 10 Most Frequent Words:")
    print(top_words[['word', 'count']])
    
    #plot
    top_words.plot(x="word", y="count", kind="bar", color="skyblue")
    plt.title("Top 10 Most Frequent Words")
    plt.ylabel("Occurrences")
    plt.savefig("word_count_chart.png")
    print("\nPlot saved successfully as 'word_count_chart.png'")
