# import requests
# import numpy as np
# import xarray as xr
# def get_chlorophyll_concentration(lat, lon):
#     netcdf_file = 'data/PACE_OCI.20240902.L3m.DAY.CHL.V2_0.chlor_a.0p1deg.NRT.nc'
#     dataset = xr.open_dataset(netcdf_file)
#     print(dataset)
#     chlor_a = dataset['chlor_a']
#     chlor_at_point = chlor_a.sel(lat=lat, lon=lon, method='nearest')
#     chlor_value = chlor_at_point.values
#     print(f"Chlorophyll-a concentration at ({lat}, {lon}): {chlor_value} mg/m³")
# get_chlorophyll_concentration(20.4,88.4)
from flask import Flask, request, jsonify
import xarray as xr

app = Flask(__name__)

@app.route('/chlorophyll', methods=['GET'])
def chlorophyll_concentration():
    try:
        # Retrieve latitude and longitude from query parameters
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        
        # Define the NetCDF file path
        netcdf_file = 'data/PACE_OCI.20240902.L3m.DAY.CHL.V2_0.chlor_a.0p1deg.NRT.nc'
        
        # Open the dataset
        dataset = xr.open_dataset(netcdf_file)
        
        # Access the chlorophyll-a data
        try:
            chlor_a = dataset['chlor_a']
        except KeyError:
            return jsonify({"error": "The dataset does not contain 'chlor_a'. Please check the variable names."}), 400

        # Select the nearest chlorophyll-a value at the specified lat and lon
        try:
            chlor_at_point = chlor_a.sel(lat=lat, lon=lon, method='nearest')
            chlor_value = chlor_at_point.values
            return jsonify({
                "chlorophyll_concentration": chlor_value.tolist()
            })
        except Exception as e:
            return jsonify({"error": f"An error occurred during selection: {str(e)}"}), 400

    except ValueError:
        return jsonify({"error": "Invalid latitude or longitude provided."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
