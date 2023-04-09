import os
import pandas as pd
from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Create Flask app instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define the route for the main page
@app.route('/', methods=['GET'])
def upload_file():
    filepath = "static/complete.csv"
    data = {}
    if filepath:
        df = pd.read_csv(filepath)
        # 1. Display a sample of the data
        data["sample"] = (df.sample(5).to_html(index=False, classes='res-table'), ">> df.sample(5)")

        # 2. Display the shape of the data
        data["shape"] = (df.shape, '>> shape = df.shape <br>>>  f"Rows: {shape[0]}, Columns: {shape[1]}"')

        # 3. Display the data types of columns
        data["columns"] = (pd.DataFrame(df.dtypes).reset_index().to_html(classes='res-table toggle-table'),
                           ">> pd.DataFrame(df.dtypes).reset_index()")
        # 4. Display summary statistics
        data["describe"] = (df.describe().to_html(classes='res-table'), ">> df.describe()")

        # 5. Display count of NaN values
        data["nan_count"] = (
            pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(
                classes='res-table toggle-table'),
            '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')

        # 6. Display count of empty values
        data["empty_count"] = (
            pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index().to_html(
                classes='res-table toggle-table'),
            '>> pd.DataFrame(df.isin(["", " "]).sum(), columns=["Empty count"]).reset_index()')

        # 7. Display count of duplicate rows
        data["duplicates_count"] = (f"{df.duplicated().sum()} (rows)", 'f"{df.duplicated().sum()} (rows)"')
        # 8. Drop unnecessary columns
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

        # 8. Display data after dropping unnecessary columns
        data["dropped_columns"] = (df.sample(5).to_html(classes='res-table', index=False),
                                   ">> columns_to_drop = [...] <br>>> df = df.drop(columns=columns_to_drop) <br>>> df.sample(5)")

        # 9. Display count of NaN values after dropping unnecessary columns
        data["nan_count2"] = (
        pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index().to_html(classes='res-table'),
        '>> pd.DataFrame(df.isna().sum(), columns=["NaN count"]).reset_index()')

        # 10. Display rows with at least one NaN value
        data["rows_with_nan"] = (
            df[df.isna().any(axis=1)].reset_index().to_html(classes='res-table toggle-table', index=False),
            '>> df[df.isna().any(axis=1)].reset_index()')

        # 11
        data["multiple_awards"] = (
            df.groupby("name").size().sort_values(ascending=False).reset_index(name="awards_count").query(
                "awards_count > 1").to_html(classes='res-table', index=False),
            '>> df.groupby("name").size().sort_values(ascending=False).reset_index(name="awards_count").query("awards_count > 1")')

        # 12. Countries with more than one award
        data["awards_by_country"] = (
            df.groupby("birth_countryNow")["name"].count()
            .reset_index(name="awards_count")
            .query("awards_count > 1")
            .sort_values(by="awards_count", ascending=False)
            .to_html(classes='res-table toggle-table', index=False),
            '>> df.groupby("birth_countryNow")["name"].count().reset_index(name="awards_count").query("awards_count > 1").sort_values(by="awards_count", ascending=False)')

        # 13. Awards by category
        data["awards_by_category"] = (
            df.groupby("category")["name"].count()
            .reset_index(name="awards_count")
            .sort_values(by="awards_count", ascending=False)
            .to_html(classes='res-table', index=False),
            '>> df.groupby("category")["name"].count().reset_index(name="awards_count").sort_values(by="awards_count", ascending=False)')

    # =================================GRAPHS================================
    # Graph 1

        # Create a new DataFrame with only the necessary columns
        awards_by_country_year = df[['birth_countryNow', 'awardYear']].copy()

        # Group data by year and country, and count the awards
        awards_by_country_year = awards_by_country_year.groupby(['awardYear', 'birth_countryNow']).size().reset_index(
            name='awards_count')

        # Get the top 15 countries by the total number of awards
        top15_countries = awards_by_country_year.groupby('birth_countryNow')['awards_count'].sum().nlargest(
            15).index.tolist()

        # Filter the data for the top 15 countries
        top15_data = awards_by_country_year[awards_by_country_year['birth_countryNow'].isin(top15_countries)]

        fig = px.scatter(top15_data, x='awardYear', y='awards_count', color='birth_countryNow',
                         title='Top 15 Countries by Number of Nobel Prizes (Per Year)',
                         labels={'awards_count': 'Awards Count', 'birth_countryNow': 'Country'})

        # Set the chart template
        pio.templates.default = "plotly_white"

        # Customize x-axis tick marks to display every 5 years
        fig.update_xaxes(tickmode='linear', dtick=5)

        # Save the chart as an HTML file
        pio.write_html(fig, file='static/scatter_chart.html', auto_open=False)

        # Graph 2 =====================
        # Calculate the values for the pie charts
        gender_counts = df['gender'].value_counts()
        category_counts = df['category'].value_counts()

        # Calculate laureate types
        laureate_types = {'Individual': len(df[df['gender'].notnull()]), 'Organization': len(df[df['gender'].isnull()])}
        laureate_types = pd.Series(laureate_types)

        # Create the pie charts
        fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
                            subplot_titles=["Laureate Types", "Gender Distribution", "Category Distribution"])

        fig.add_trace(go.Pie(labels=laureate_types.index, values=laureate_types.values, name="Laureate Types"),
                      1, 1)
        fig.add_trace(go.Pie(labels=gender_counts.index, values=gender_counts.values, name="Gender Distribution"),
                      1, 2)
        fig.add_trace(go.Pie(labels=category_counts.index, values=category_counts.values, name="Category Distribution"),
                      1, 3)

        # Set the layout and title
        fig.update_layout(title="Pie Charts: Laureate Types, Gender Distribution, and Category Distribution")
        pio.templates.default = "plotly_white"

        # Save the chart as an HTML file
        pio.write_html(fig, file='static/pie_charts.html', auto_open=False)

        # Graph 3 =====================
        # Calculate the number of awards by continent and country
        continent_country_counts = df.groupby(['birth_continent', 'birth_countryNow']).size().reset_index(name='count')

        # Create a dictionary to store traces for each country within the respective continent
        continent_traces = {}

        for _, row in continent_country_counts.iterrows():
            continent, country, count = row['birth_continent'], row['birth_countryNow'], row['count']
            if continent not in continent_traces:
                continent_traces[continent] = []
            continent_traces[continent].append(go.Bar(name=country, x=[continent], y=[count]))

        # Create the stacked bar chart
        fig = go.Figure()

        for continent, country_traces in continent_traces.items():
            for trace in country_traces:
                fig.add_trace(trace)

        fig.update_layout(barmode='stack', title="Bar Chart: Number of Awards by Continent and Country")
        pio.templates.default = "plotly_white"

        # Save the chart as an HTML file
        pio.write_html(fig, file='static/continent_country_bar_chart.html', auto_open=False)

        # Render the HTML template and pass the data
    return render_template('upload.html', data=data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
