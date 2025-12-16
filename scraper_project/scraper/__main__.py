"""Entry point for the scraper module."""

from scraper.catalog import Catalog
import json
import pandas as pd

def main():
    book_app = Catalog()
    items = book_app.books()
    
    data_list = []
    
    for item in items:
        res = item.to_dict()
        data_list.append(res)
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_list)

    # Write the DataFrame to a CSV file
    df.to_csv('output_pandas.csv', index=False) # index=False prevents writing the DataFrame index as an unnamed column

    print("Data successfully written to output_pandas.csv using pandas")
    
    print(df)
    
    # for item in items:
    #     print(item)
    
    # best_books = book_app.best_books()
    # for book in best_books: 
    #     print(book)

    # print("\n\nCheapest 5 Books:\n")

    # cheapest_books = book_app.cheapest_books()
    # for book in cheapest_books: 
    #     print(book)

# import requests

# def main():
#     URL = 'http://books.toscrape.com'
    
#     # Send a GET request to a URL
#     response = requests.get(URL)
#     print("Scraper is running...")
    
#     print(f"Response Code: {response.status_code}")

#     if response.status_code == 200:
#         # Print the response content
#         print(f"Content Snippet: {response.text[:100]}...")
#         print(response.text)
#     else:
#         print('Error:', response.status_code)

if __name__ == "__main__":
    main()
