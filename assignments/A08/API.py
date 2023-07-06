from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import pandas as pd
from typing import Optional

app = FastAPI()

# Load the data.csv file into a pandas DataFrame for easier manipulation
data = pd.read_csv('Data.csv', parse_dates=['Date_reported'])

@app.get("/")
async def docs_redirect():
    """
    Redirects the base URL to the FastAPI auto-generated documentation page.
    """
    return RedirectResponse(url="/docs")

@app.get("/countries/")
async def countries():
    """
    Returns a list of all unique countries present in the dataset.
    """
    return data['Country'].unique().tolist()

@app.get("/regions/")
async def regions():
    """
    Returns a list of all unique WHO regions present in the dataset.
    """
    return data['WHO_region'].unique().tolist()

@app.get("/deaths")
async def total_deaths():
    """
    Returns the total deaths from all countries and regions in the dataset.
    """
    total_deaths = data['Cumulative_deaths'].sum()
    return {"total_deaths": total_deaths}

@app.get("/deaths_by_country/{country}")
async def deaths_by_country(country: str):
    """
    Returns the total deaths for the specified country.
    """
    try:
        filtered_data = data[data['Country'] == country]
        total_deaths = filtered_data['Cumulative_deaths'].sum().item()
        return {"total_deaths": total_deaths}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/deaths_by_region/{region}")
async def deaths_by_region(region: str):
    """
    Returns the total deaths for the specified WHO region.
    """
    filtered_data = data[data['WHO_region'] == region]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

@app.get("/deaths_by_country_year/{country}/{year}")
async def deaths_by_country_year(country: str, year: int):
    """
    Returns the total deaths for the specified country and year.
    """
    filtered_data = data[(data['Country'] == country) & (data['Year'] == year)]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

@app.get("/deaths_by_region_year/{region}/{year}")
async def deaths_by_region_year(region: str, year: int):
    """
    Returns the total deaths for the specified WHO region and year.
    """
    filtered_data = data[(data['WHO_region'] == region) & (data['Year'] == year)]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

@app.get("/max_deaths/")
async def max_deaths(min_date: Optional[str] = None, max_date: Optional[str] = None):
    """
    Returns the country with the maximum number of deaths within the specified date range.
    """
    try:
        if min_date and max_date:
            min_date = pd.to_datetime(min_date, format='%Y-%m-%d')  # Convert min_date to datetime object
            max_date = pd.to_datetime(max_date, format='%Y-%m-%d')  # Convert max_date to datetime object
            date_filtered_data = data[(data['Date_reported'] >= min_date) & (data['Date_reported'] <= max_date)]
        else:
            date_filtered_data = data

        max_death_country = date_filtered_data.loc[date_filtered_data['Cumulative_deaths'].idxmax(), 'Country']

        return {
            "country": max_death_country,
            "success": True,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/min_deaths/")
async def min_deaths(min_date: Optional[str] = None, max_date: Optional[str] = None):
    """
    Returns the country with the minimum number of deaths within the specified date range.
    """
    try:
        if min_date and max_date:
            min_date = pd.to_datetime(min_date, format='%Y-%m-%d')  # Convert min_date to datetime object
            max_date = pd.to_datetime(max_date, format='%Y-%m-%d')  # Convert max_date to datetime object
            date_filtered_data = data[(data['Date_reported'] >= min_date) & (data['Date_reported'] <= max_date)]
        else:
            date_filtered_data = data

        min_death_country = date_filtered_data.loc[date_filtered_data['Cumulative_deaths'].idxmin(), 'Country']

        return {
            "country": min_death_country,
            "success": True,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/avg_deaths/")
async def avg_deaths():
    """
    Returns the average number of deaths across all countries and regions in the dataset.
    """
    try:
        avg_deaths = data['Cumulative_deaths'].mean()

        return {
            "average": avg_deaths,
            "success": True,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
