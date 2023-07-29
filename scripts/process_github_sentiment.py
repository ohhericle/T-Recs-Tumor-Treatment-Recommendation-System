import pandas as pd
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def read_data(datapath: Path):

    def sanitize(text: str):

        junk = "',?!&."
        junk += '"'
        text = text[1:]
        text = ''.join([i for i in text if i not in junk])

        return text

    def get_sentiment(text: str):

        sid_obj = SentimentIntensityAnalyzer()

        sentiment_dict = sid_obj.polarity_scores(text)
        negative = sentiment_dict['neg']
        positive = sentiment_dict['pos']
        neutral = sentiment_dict['neu']
        compound = sentiment_dict['compound']

        if sentiment_dict['compound'] >= 0.05:

            overall_sentiment = 'Positive'

        elif sentiment_dict['compound'] < 0.05:

            overall_sentiment = 'Negative'

        else:

            overall_sentiment = 'Neutral'

        return positive, negative, neutral, compound, overall_sentiment

    data = pd.read_csv(datapath)
    data = data[data['specialty'].str.contains('onc')]
    data['review'] = data['review'].apply(lambda x: sanitize(x))
    data.to_csv('../data/clean_data/gh_contains_onc.csv', index=False)
    reviews = data['review']

    scores = []
    reviews = reviews.to_list()

    for i in reviews:

        score = get_sentiment(i)
        scores.append(score)
        print(score)

    final_scores = pd.DataFrame()
    final_scores['positive'] = [i[0] for i in scores]
    final_scores['negative'] = [i[1] for i in scores]
    final_scores['neutral'] = [i[2] for i in scores]
    final_scores['compound'] = [i[3] for i in scores]
    final_scores['overall'] = [i[4] for i in scores]

    return final_scores


if __name__ == '__main__':

    scores = read_data(Path('../data/raw_data/all_GitHub.csv'))
    scores.to_csv('../data/final/final_combined_github_data.csv', index=False)
