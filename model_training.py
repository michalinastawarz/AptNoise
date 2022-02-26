import pickle
import sqlite3
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeRegressor


def model_training(test):
    con = sqlite3.connect('site.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM record")
    articles = cur.fetchall()

    input_cols = [
        'id',
        'author',
        'title',
        'url',
        'published_at',
        'content',
        'source_name',
        'predicted_score_when_presented',
        'assigned_score'
    ]
    articles_df = pd.DataFrame(articles, columns=input_cols)
    articles_df.set_index('id', inplace=True)

    encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=999)
    cat_cols = ['author', 'source_name']
    encoder.fit(articles_df[cat_cols])

    training_data = articles_df.copy()
    training_data.dropna(how='any', inplace=True)

    training_data[cat_cols] = encoder.transform(training_data[cat_cols])
    x_train = training_data[['author', 'source_name']]
    y_train = training_data['assigned_score']

    model = DecisionTreeRegressor()
    model.fit(x_train, y_train)

    if test:
        suffix = '_test'
    else:
        suffix = ''

    pickle.dump(encoder, open(f'source_encoder{suffix}.pkl', 'wb'))
    pickle.dump(model, open(f'ml_model{suffix}.pkl', 'wb'))

    return None


if __name__ == '__main__':
    model_training(test=False)
