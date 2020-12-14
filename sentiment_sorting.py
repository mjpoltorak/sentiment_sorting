import pandas as pd
from textblob import TextBlob
from collections import Counter
import timeit


def load_data(csv_lst):
    # The loop below reads the csv files into pandas dataframes, removes the headers, and then appends them
    master = pd.DataFrame()
    for csv in csv_lst:
        to_add = pd.read_csv(csv, header=None, skiprows=1)
        master = master.append(to_add)

    # This re-adds normalized column names, writes it to a csv, and then calls the next function
    master.rename(columns={0: "Name", 1: "Purpose"}, inplace=True)
    master.to_csv('master_companies.csv', index=False)
    sentiment_analysis()


def original_code():
    df = pd.read_csv('master_companies.csv')
    high_score = -1000
    best_company = None
    low_score = 1000
    worst_company = None
    for company in df.iterrows():
        company = company[1]
        blob = TextBlob(company['Purpose'])
        if blob.sentiment.polarity > high_score:
            high_score = blob.sentiment.polarity
            best_company = company
        if blob.sentiment.polarity < low_score:
            low_score = blob.sentiment.polarity
            worst_company = company


def revision_code():
    df = pd.read_csv('master_companies.csv')
    df['sentiment'] = df['Purpose'].apply(lambda t: TextBlob(t).sentiment.polarity)
    df.sort_values('sentiment', inplace=True)


def sentiment_analysis():
    df = pd.read_csv('master_companies.csv')
    print("Comparison of methods")
    print("Revision Code: ", timeit.timeit("revision_code()", setup="from __main__ import revision_code",  number=100))
    print("Original Code: ", timeit.timeit("original_code()", setup="from __main__ import original_code", number=100))
    # As I have demonstrated the revision code is indeed more efficient. While 1 run of each is both under 1 second
    # it can be seen that over 100 iterations pandas sorting is faster
    df['sentiment'] = df['Purpose'].apply(lambda t: TextBlob(t).sentiment.polarity)
    df.sort_values('sentiment', inplace=True)
    # After reading the newly created csv the for loop below tracks the best and worst company based on sentiment
    # Sentiment is tracked using textblobs polarity measure
    #
    print("Best Company: " + df.iloc[-1]['Name'] + "\n\tScore: " + str(df.iloc[-1]['sentiment']))
    print("Worst Company: " + df.iloc[0]['Name'] + "\n\tScore: " + str(df.iloc[0]['sentiment']))
    print()
    most_common()


def most_common():
    df = pd.read_csv('master_companies.csv')
    all_words = []
    # This loop breaks each company's purpose into words and appends it to a master list where occurrences will be
    # counted later
    for company in df.iterrows():
        company = company[1]
        blob = TextBlob(company['Purpose'])
        all_words += list(blob.words)

    # Counter is a builtin function of python 3. I found the function and the most common function in the docs here:
    # https://docs.python.org/2/library/collections.html
    count = Counter(all_words)
    most_comm = count.most_common()
    print("10 most common words (number of occurrences): ")
    for i in range(0, 10):
        print("\t" + str(i+1) + ". " + most_comm[i][0] + " ({})".format(str(most_comm[i][1])))
    print()


if __name__ == '__main__':
    csv_list = ['liam_extracted_companies.csv', 'alex_requests_output.csv', 'ryan_web_scraper.csv', 'lucas_output.csv']
    load_data(csv_list)
