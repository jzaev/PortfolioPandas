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
    filepath = "static/organizations-10000.csv"
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
        data["nan_count"] = (
        pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(classes='res-table'),
        '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')
        # 6
        data["empty_count"] = (
            pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index().to_html(classes='res-table'),
            '>> pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index()')
        # 7
        data["duplicates_count"] = (f"{df.duplicated().sum()} (rows)", 'f"{df.duplicated().sum()} (rows)"')
        # 8
        country_column = "Country"
        data["unique_countries"] = (
        df[country_column].value_counts().reset_index().to_html(classes='res-table', table_id='table8'),
        f">> df['{country_column}'].value_counts().reset_index()")
        # 9
        data["grouped_by_country"] = (
        df.groupby("Country")["Number of employees"].sum().sort_values(ascending=False).reset_index().to_html(
            classes='res-table', table_id='table9'),
        f">> df.groupby('Country')['employees_column'].sum().sort_values(ascending=False).reset_index()")
        # 10
        data["unique_industries"] = (
        df["Industry"].value_counts().reset_index().to_html(classes='res-table', table_id='table10'),
        f">> df['Industry'].value_counts().reset_index()")

        # ===========GRAPH===================

        fig1 = px.bar(df["Country"].value_counts().head(10),
                      x=df["Country"].value_counts().head(10).index,
                      y=df["Country"].value_counts().head(10).values,
                      labels={"x": "Country", "y": "Number of organizations"},
                      title="Top 10 countries by number of organizations")
        fig1.write_image("static/images/top_countries_plotly.png")

        top_industries = df["Industry"].value_counts().head(10)
        fig2 = px.bar(top_industries,
                      x=top_industries.values,
                      y=top_industries.index,
                      orientation='h',
                      labels={"x": "Number of organizations", "y": "Industry"},
                      title="Top 10 industries by number of organizations")
        fig2.write_image("static/images/top_industries_plotly.png")

        industry_counts = df['Industry'].value_counts().nlargest(15)

        fig3 = go.Figure(go.Bar(
            x=industry_counts.values,
            y=industry_counts.index,
            orientation='h'
        ))

        fig3.update_layout(
            title="Top 15 Industries",
            xaxis_title="Number of Companies",
            yaxis_title="Industry",
        )

        fig3.write_image("static/images/top15_industries_plotly.png")

    return render_template('upload.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
