import pandas as pd

# Replace with your actual Excel file path
file_path = 'dataset.xlsx'  # e.g., 'C:/Users/YourName/property_data.xlsx'

try:
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=0)  # Assumes data is in the first sheet

    # Standardize column names
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Map to expected column names
    col_mapping = {
        'id': ['id', 'Id', 'ID', 'property_id'],
        'area': ['area', 'Area', 'sqft', 'square_feet'],
        'bedrooms': ['bedrooms', 'Bedrooms', 'beds', 'br'],
        'bathrooms': ['bathrooms', 'Bathrooms', 'baths', 'ba'],
        'floors': ['floors', 'Floors', 'levels', 'stories'],
        'yearbuilt': ['yearbuilt', 'YearBuilt', 'year_built', 'year', 'built'],
        'location': ['location', 'Location', 'area_name', 'region'],
        'condition': ['condition', 'Condition', 'state', 'quality'],
        'garage': ['garage', 'Garage', 'parking', 'has_garage'],
        'price': ['price', 'Price', 'cost', 'value']
    }
    new_cols = {}
    for expected, aliases in col_mapping.items():
        for alias in aliases:
            if alias in df.columns:
                new_cols[alias] = expected
                break
    df = df.rename(columns=new_cols)

    # Keep only relevant columns
    expected_cols = ['id', 'area', 'bedrooms', 'bathrooms', 'floors', 'yearbuilt',
                     'location', 'condition', 'garage', 'price']
    df = df[[col for col in expected_cols if col in df.columns]]

    # Convert numeric columns
    numeric_cols = ['id', 'area', 'bedrooms', 'bathrooms', 'floors', 'yearbuilt', 'price']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean categorical columns
    for col in ['location', 'condition', 'garage']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str)

    print(f"Loaded {len(df)} properties from '{file_path}'")

    # Search function
    def search_properties(df):
        print("\nEnter your search criteria (press Enter to skip any field):")

        # Get user inputs
        bedrooms = input("Number of bedrooms (e.g., 3): ").strip()
        bathrooms = input("Number of bathrooms (e.g., 2): ").strip()
        floors = input("Number of floors (e.g., 1): ").strip()
        min_area = input("Minimum area (sqft, e.g., 1000): ").strip()
        max_area = input("Maximum area (sqft, e.g., 5000): ").strip()
        location = input("Location (e.g., Downtown, Suburban, Urban, Rural): ").strip()
        condition = input("Condition (e.g., Excellent, Good, Fair, Poor): ").strip()
        garage = input("Garage (Yes/No): ").strip()
        min_price = input("Minimum price (e.g., 100000): ").strip()
        max_price = input("Maximum price (e.g., 500000): ").strip()

        # Start with full DataFrame
        results = df.copy()

        # Apply filters based on input
        if bedrooms:
            results = results[results['bedrooms'] == int(bedrooms)]
        if bathrooms:
            results = results[results['bathrooms'] == int(bathrooms)]
        if floors:
            results = results[results['floors'] == int(floors)]
        if min_area:
            results = results[results['area'] >= int(min_area)]
        if max_area:
            results = results[results['area'] <= int(max_area)]
        if location:
            results = results[results['location'].str.lower() == location.lower()]
        if condition:
            results = results[results['condition'].str.lower() == condition.lower()]
        if garage:
            garage_val = 'Yes' if garage.lower() in ['yes', 'y'] else 'No'
            results = results[results['garage'] == garage_val]
        if min_price:
            results = results[results['price'] >= int(min_price)]
        if max_price:
            results = results[results['price'] <= int(max_price)]

        # Show results
        if len(results) > 0:
            print(f"\nFound {len(results)} matching properties:")
            print(results.to_string(index=False))
        else:
            print("\nNo properties match your criteria.")

        # Ask if user wants to search again
        again = input("\nSearch again? (yes/no): ").strip().lower()
        if again in ['yes', 'y']:
            search_properties(df)
        else:
            print("Thanks for searching!")

    # Start the search
    search_properties(df)

except FileNotFoundError:
    print(f"Error: '{file_path}' not found. Please check the file path.")
except Exception as e:
    print(f"Error: Something went wrong - {e}")