from root.scrape import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    try:
        resp = scraper.fetch("https://www.google.com")
        print(resp)
        print("Scraper test completed successfully.")

    except Exception as e:
        print("Scraper test failed:", e)