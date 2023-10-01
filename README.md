# Toko Alvabet Data Scraping and Price Comparator

This Python script is designed to scrape data from Toko Alvabet's website and perform price comparison for the obtained products. It includes features for viewing and analyzing product data, as well as comparing prices with other sellers.

## Features

### Data Scraping

- Scrapes product data from Toko Alvabet's website.
- Extracts information such as product title, price, author, genre, stock, weight, edition, and more.
- Saves the scraped data to a CSV file for further analysis.

### Price Comparator

- Compares the prices of products with other sellers for the same product.
- Calculates the breakeven price and potential profit for each product.
- Allows you to view search results and details for each product.

## Usage

1. Run the script using the following command:

   ```bash
   python script.py
   ```

2. GUI Interface:
   - Use the graphical user interface to enter and view data.
   - Enter the starting row number and click "Start" to begin the scraping process.
   - Navigate through the data using "Next" and "Back" buttons.
   - Copy URLs and product details for further use.
   - Compare product prices and view potential profits.

3. Data Files:
   - The script uses a CSV file named 'tokoalvabet.csv' to store scraped data. Ensure this file is present in the same directory.
   - Modify the `COLUMNS` and other parameters as needed to customize the data columns and behavior.

## Dependencies

- The script relies on several Python libraries, including `pandas`, `requests`, `BeautifulSoup`, and PyQt6. Install these dependencies using pip if you haven't already:

   ```bash
   pip install pandas requests beautifulsoup4 PyQt6
   ```

## Author

- Author: [Your Name]

Feel free to customize the script, GUI, and README as needed for your specific use case or requirements.
```

Replace `[Your Name]` in the author section with your name or details. Additionally, make sure to update the dependencies section if there are any other dependencies required for your script.
