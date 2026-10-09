from mrjob.job import MRJob
import pandas as pd
import matplotlib.pyplot as plt


class WordCount(MRJob):
    #define a pandas dataframe
    #wordCount=pd.DataFrame(columns=['word', 'count'])
    #row_list=[]

    #create a mapper function 
    def mapper(self, _, line): #self: the class itself, _ an unused variable, 
        #in this instance the key, and the line is the line being read from the text 
        for word in line.strip().split(' '):
            if len(word) > 0:
                yield (word, 1)

    #create the reducer class 
    def reducer(self, word, count):
        #row_list.append[{'word':word, 'count':sum(count)}]
        yield (word, sum(count))

    #print the dataframe
    '''def wordCountHead():
        wordCount=pd.DataFrame(row_list)
        print(wordCount.head())'''

if __name__ == '__main__':
    mr_job=WordCount(args=['inputtext1.txt'])
    results = []
    # Run the job and read the raw output stream sequentially
    with mr_job.make_runner() as runner:
        runner.run()
        for key, value in mr_job.parse_output(runner.cat_output()):
            results.append({'word': key, 'count': value})

    # 4. Initialize and print the DataFrame after the job completes
    wordCount_df = pd.DataFrame(results)
    print("\n--- Pandas DataFrame Head ---")
    print(wordCount_df.head())
    top_words = wordCount_df.sort_values(by="count", ascending=False).head(10)
    top_words.plot(x="word", y="count", kind="bar")
    plt.savefig("word_count_chart.png", bbox_inches="tight")
    print("Plot saved successfully as 'word_count_chart.png'")
