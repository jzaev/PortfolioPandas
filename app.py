import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET'])
def upload_file():
    filepath = "organizations-10000.csv"
    data = {}
    if filepath:
        df = pd.read_csv(filepath)
        # 1
        data["sample"] = (df.sample(5).to_html(index=False, classes='res-table'), ">> df.sample(5)")
        # 2
        data["shape"] = (df.shape, '>> shape = df.shape <br>>>  f"Rows: {shape[0]}, Columns: {shape[1]}"')
        # 3
        data["columns"] = (pd.DataFrame(df.dtypes).reset_index().to_html(classes='res-table'),
                           ">> pd.DataFrame(df.dtypes).reset_index()")
        # 4
        data["describe"] = (df.describe().to_html(classes='res-table'), ">> df.describe()")
        # 5
        data["nan_count"] = (pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(classes='res-table'),
                             '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')
        # 6
        data["empty_count"] = (
        pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index().to_html(classes='res-table'),
        '>> pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index()')
        # 7
        data["duplicates_count"] = (f"{df.duplicated().sum()} (rows)", 'f"{df.duplicated().sum()} (rows)"')

    return render_template('upload.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
