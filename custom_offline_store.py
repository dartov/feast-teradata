from feast import FeatureStore
import pandas as pd
from sklearn import datasets
from feature_repo.repo import flower, df_feature_view
from datetime import datetime


fs = FeatureStore("feature_repo/")
fs.apply([flower, df_feature_view])


data = datasets.load_iris()
target_df = pd.DataFrame(data=data.target, columns=["class"])
timestamps = pd.date_range(
    end=pd.Timestamp.now(),
    periods=len(target_df),
    freq='D').to_frame(name="event_timestamp", index=False)

# target_df = pd.concat(objs=[target_df, timestamps], axis=1)
# flower_ids = pd.DataFrame(data=list(range(len(target_df))), columns=["flower_id"])
# target_df = pd.concat(objs=[target_df, flower_ids], axis=1)
# print(target_df.dtypes)
# rs = fs.get_historical_features(
#     entity_df="Select event_timestamp,flower_id from iris_data",
#     features=[
#         "df_feature_view:sepal length (cm)",
#         "df_feature_view:sepal width (cm)",
#         "df_feature_view:petal length (cm)",
#         "df_feature_view:petal width (cm)"
#     ]
#     )
# rs = rs.to_df()
# print(rs)

fs.materialize_incremental(end_date=datetime.now())


feature_vector = fs.get_online_features(
    features=[
        "df_feature_view:sepal length (cm)",
        "df_feature_view:sepal width (cm)",
        "df_feature_view:petal length (cm)",
        "df_feature_view:petal width (cm)"
    ], entity_rows=[{"flower_id": 5}]
    ).to_dict()

print(feature_vector)

fs.teardown()


