import os
import pandas as pd
from flask import Flask, render_template
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET'])
def upload_file():
    filepath = "static/complete.csv"
    data = {}
    if filepath:
        df = pd.read_csv(filepath)
        # 1
        data["sample"] = (df.sample(5).to_html(index=False, classes='res-table'), ">> df.sample(5)")
        # 2
        data["shape"] = (df.shape, '>> shape = df.shape <br>>>  f"Rows: {shape[0]}, Columns: {shape[1]}"')
        # 3
        data["columns"] = (pd.DataFrame(df.dtypes).reset_index().to_html(classes='res-table toggle-table'),
                           ">> pd.DataFrame(df.dtypes).reset_index()")
        # 4
        data["describe"] = (df.describe().to_html(classes='res-table'), ">> df.describe()")
        # 5
        data["nan_count"] = (
        pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(classes='res-table toggle-table'),
        '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')
        # 6
        data["empty_count"] = (
            pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index().to_html(classes='res-table toggle-table'),
            '>> pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index()')
        # 7
        data["duplicates_count"] = (f"{df.duplicated().sum()} (rows)", 'f"{df.duplicated().sum()} (rows)"')
        # Здесь будут новые блоки кода для анализа данных из нового файла CSV
        #8
        columns_to_drop = [
            "prizeAmount", "categoryFullName", "sortOrder", "portion", "prizeAmount",
            "dateAwarded", "motivation", "categoryTopMotivation", "award_link", "givenName",
            "familyName", "fullName", "penName", "birth_city", "birth_country", "birth_locationString",
            "death_date", "death_city", "death_cityNow", "death_continent", "death_country",
            "death_countryNow", "death_locationString", "nativeName", "acronym", "org_founded_date",
            "org_founded_city", "org_founded_cityNow", "org_founded_continent", "org_founded_country",
            "org_founded_countryNow", "org_founded_locationString", "residence_1", "residence_2",
            "affiliation_1", "affiliation_2", "affiliation_3", "affiliation_4","laureate_link","orgName"
        ]

        df = df.drop(columns=columns_to_drop)

        # 8. Data after dropping unnecessary columns
        data["dropped_columns"] = (df.sample(5).to_html(classes='res-table', index=False),
                                   ">> columns_to_drop = [...] <br>>> df = df.drop(columns=columns_to_drop) <br>>> df.sample(5)")
        # 9
        data["nan_count2"] = (
        pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(classes='res-table'),
        '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')

        # 10
        data["rows_with_nan"] = (
            df[df.isna().any(axis=1)].reset_index().to_html(classes='res-table toggle-table', index=False),
            '>> df[df.isna().any(axis=1)]')

    return render_template('upload.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
