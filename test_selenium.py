from root.scrape import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    try:
        scraper.fetch("https://www.example.com")
        print("Scraper test completed successfully.")
    except Exception as e:
        print("Scraper test failed:", e)