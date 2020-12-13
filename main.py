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

if len(sys.argv) > 1:
    if sys.argv[1] == "scrape":
        print("Scraping the latest contract data from the EVE servers (this may take a while)")
        scrape.scrape_public_contracts(scrape.the_forge_region_id)