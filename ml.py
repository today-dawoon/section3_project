import pandas as pd
import sqlite3

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 데이터 호출
conn = sqlite3.connect("movie_info.db")
cur = conn.cursor() 
query = cur.execute(
    """
    SELECT m.Id,
        m.Title,
        g.Genre,
        m.Original_language,
        m.Overview ,
        m.Popularity ,
        m.Vote_average ,
        m.Vote_count ,
        m.Adult,
        m.Release_date,
        m.Backdrop_path ,
        m.Poster_path 
    FROM Movie m 
    LEFT JOIN Genre g ON g.GenreId = m.GenreId 
"""
) 

cols = [column[0] for column in query.description]
result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
conn.close()


# 모델링
model = LinearRegression()

target = 'Popularity'

train, test = train_test_split(result,
                            test_size=0.8,  
                            random_state=2
                            )
                            
features = ['Vote_count', 'Vote_average']

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# 모델 fit
model.fit(X_train, y_train)

# 트레이닝
## 트레이닝 에러: 5.01
y_pred = model.predict(X_train)
mae = mean_absolute_error(y_train, y_pred)

# 테스트
## 테스트 에러: 6.09
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

X_test['pop_pred'] = y_pred
X_test.reset_index(inplace=True)
result.reset_index(inplace=True)

df = X_test.merge(result, on=['index', 'Vote_count', 'Vote_average'], how='left').drop(['index', 'Popularity'], axis=1)
