import requests
import sqlite3
import database
import datetime

the_forge_region_id = 10000002
abyssal_type_ids = [
    47408, 47702, 47732, 47736, 47740, 47745, 47749, 47753, 47757, 47769, 47773, 47777, 47781, 47785, 47789, 
    47793, 47800, 47804, 47808, 47812, 47817, 47820, 47824, 47828, 47832, 47836, 47838, 47840, 47842, 47844, 
    47846, 48419, 48423, 48427, 48431, 48435, 48439, 49722, 49726, 49730, 49734, 49738, 52227, 52230, 56303, 
    56304, 56305, 56306, 56307, 56308, 56309, 56310, 56311, 56312, 56313]

def scrape_dogma_attributes():
    r = requests.get("https://esi.evetech.net/latest/dogma/attributes")
    attribute_ids = r.json()

    db_conn = database.get_db_conn()
    c = db_conn.cursor()
    c.row_factory = lambda cur, row: row[0]
    c.execute("SELECT attribute_id FROM dogma_attributes")
    already_scraped = c.fetchall()

    count = 1
    for attribute_id in attribute_ids:
        if attribute_id not in already_scraped:
            print("Scraping attribute id #%d (%d/%d)" % (attribute_id, count, len(attribute_ids)))
            scrape_dogma_attribute(attribute_id)
        else:
            print("Skipping attribute id #%d (%d/%d)" % (attribute_id, count, len(attribute_ids)))
        count += 1

def scrape_dogma_attribute(attribute_id):
    r = requests.get("https://esi.evetech.net/latest/dogma/attributes/%d" % attribute_id)
    d = r.json()

    db_conn = database.get_db_conn()
    c = db_conn.cursor()
    c.execute("INSERT INTO dogma_attributes VALUES (?,?,?,?,?,?,?,?,?,?)", (
        d["attribute_id"],
        d["name"]          if "name" in d else "",
        d["display_name"]  if "display_name" in d else "",
        d["description"]   if "description" in d else "",
        d["high_is_good"]  if "high_is_good" in d else 0,
        d["default_value"] if "default_value" in d else "NULL"
    ))
    db_conn.commit()

def scrape_types(type_ids):
    db_conn = database.get_db_conn()
    c = db_conn.cursor()
    c.row_factory = lambda cur, row: row[0]
    c.execute("SELECT type_id FROM types")
    already_scraped = c.fetchall()

    for type_id in type_ids:
        if type_id not in already_scraped:
            scrape_type(type_id)

def scrape_type(type_id):
    r = requests.get("https://esi.evetech.net/v3/universe/types/%d" % type_id)
    try:
        d = r.json()
    except:
        print("Failed to scrape type id #%d", type_id)
        return False

    db_conn = database.get_db_conn()
    c = db_conn.cursor()
    c.execute("INSERT OR IGNORE INTO types VALUES (?,?)", (d["type_id"], d["name"]))
    db_conn.commit()
    return True

def is_abyssal(type_id):
    if type_id in abyssal_type_ids:
        return True
    else:
        return False

def scrape_public_contracts(region_id):
    r = requests.get("https://esi.evetech.net/v1/contracts/public/%d" % region_id)
    pages = int(r.headers["X-Pages"])
    
    db_conn = database.get_db_conn()
    cur = db_conn.cursor()
    cur.row_factory = lambda cur, row: row[0]
    cur.execute("SELECT contract_id FROM contracts")
    already_scraped = cur.fetchall()

    for page in range(1, pages+1):
        print("Pulling contracts page %d/%d" % (page, pages))

        r = requests.get("https://esi.evetech.net/v1/contracts/public/%d?page=%d" % (region_id, page))
        contracts = r.json()

        for contract in contracts:
            # skip contracts we already scraped
            if int(contract["contract_id"]) in already_scraped:
                continue

            print("Scraping contract #%d (page %d/%d)" % (int(contract["contract_id"]), page, pages))

            # only interested in item exchange contracts
            if contract["type"] != "item_exchange":
                mark_contract_scraped(contract)
                continue
            
            # scrape items
            r = requests.get("https://esi.evetech.net/v1/contracts/public/items/%d/" % int(contract["contract_id"]))
            if r.status_code != 200:
                continue

            try:
                items = r.json()
            except:
                print("Error on contract #%d (page %d/%d)" % (int(contract["contract_id"]), page, pages))
                continue

            # only interested in contracts for singleton item
            if len(items) != 1:
                mark_contract_scraped(contract)
                continue

            item = items[0]

            # only interested in 1x quantity of item
            if int(item["quantity"]) != 1:
                mark_contract_scraped(contract)
                continue

            # only interested in abyssal items
            if not is_abyssal(int(item["type_id"])):
                mark_contract_scraped(contract)
                continue

            print("Abyssal item found, item id #%d" % item["type_id"])
            cur.execute("INSERT INTO abyssal_observations (item_id, type_id, contract_id) VALUES (?,?,?)", (
                item["item_id"],
                item["type_id"],
                contract["contract_id"]
            ))

            mark_contract_scraped(contract)
            db_conn.commit()

def mark_contract_scraped(data):
    db_conn = database.get_db_conn()
    cur = db_conn.cursor()
    cur.execute("INSERT INTO contracts (contract_id, date_issued, date_expired, price) VALUES (?,?,?,?)", (
        data["contract_id"],
        parse_eve_date(data["date_issued"]),
        parse_eve_date(data["date_expired"]),
        data["price"]
    ))
    db_conn.commit()

def parse_eve_date(date):
    dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return (dt - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)