import access
import database
import scrape
import sys

print("Welcome to Abyssalearn")

# init db
print("Connecting to database and performing init")
database.create_tables()

# scrape basic data for db
print("Updating basic data from EVE servers")
scrape.scrape_types(scrape.abyssal_type_ids)
scrape.scrape_dogma_attributes()

print()

if len(sys.argv) > 1:
    if sys.argv[1] == "scrape":
        print("Scraping the latest contract and abyssal data from the EVE servers (this may take a while)")
        scrape.scrape_public_contracts(scrape.the_forge_region_id)
        scrape.scrape_incomplete_abyssal_items()
    elif sys.argv[1] == "summary":
        print("Summary of abyssal mod counts currently in database: (type IDs are in brackets)\n")
        print(access.generate_summary())
    elif sys.argv[1] == "random":
        print("Dumping data for random module matching provided type id...\n")
        print(access.random_item(int(sys.argv[2])))