import pandas as pd
from textblob import TextBlob
from collections import Counter


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


def sentiment_analysis():
    df = pd.read_csv('master_companies.csv')
    high_score = -1000
    best_company = None
    low_score = 1000
    worst_company = None
    # After reading the newly created csv the for loop below tracks the best and worst company based on sentiment
    # Sentiment is tracked using textblobs polarity measure
    for company in df.iterrows():
        company = company[1]
        blob = TextBlob(company['Purpose'])
        if blob.sentiment.polarity > high_score:
            high_score = blob.sentiment.polarity
            best_company = company
        if blob.sentiment.polarity < low_score:
            low_score = blob.sentiment.polarity
            worst_company = company
    print("Best Company: " + best_company['Name'] + "\n\tScore: " + str(high_score))
    print("Worst Company: " + worst_company['Name'] + "\n\tScore: " + str(low_score))
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
