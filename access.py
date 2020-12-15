import database
import json
import scrape
import sqlite3

# these are attributes that will never matter for prices
blacklisted_attribute_ids = [
    277, # required skill level
    182, # primary skill required
    633, # meta level
    1692, # meta group id
    162, # radius
    422, # tech level
    1212 # required thermodynamics level
]

def generate_summary():
    summary = ""

    db_conn = database.get_db_conn()
    cur = db_conn.cursor()

    q = f"SELECT * FROM types WHERE type_id in ({','.join(['?']*len(scrape.abyssal_type_ids))}) ORDER BY name"
    cur.execute(q, scrape.abyssal_type_ids)
    types = cur.fetchall()

    for t in types:
        cur.execute("SELECT COUNT(*) FROM abyssal_observations WHERE type_id = ?", (t[0],))
        count = cur.fetchall()
        summary += "%s - %s (#%d)\n" % (str(count[0][0]).rjust(6), t[1], t[0])

    return summary

def random_item(type_id):
    db_conn = database.get_db_conn()
    cur = db_conn.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute('''
        SELECT ao.*, c.price, t.name FROM abyssal_observations ao
        LEFT JOIN contracts c ON c.contract_id=ao.contract_id
        LEFT JOIN types t ON t.type_id=ao.type_id
        WHERE ao.type_id=?
        ORDER BY RANDOM()
        LIMIT 1''', (type_id,))

    item = cur.fetchone()
    
    summary = ""
    summary += "Type: " + item["name"] + "\n"
    summary += f"List Price: {item['price']:,} ISK\n"
    summary += "Attributes:\n"

    item_attribs = json.loads(item["dogma_attributes"])
    attribute_ids = []

    for attrib in item_attribs:
        attribute_ids.append(attrib["attribute_id"])

    q = f"SELECT * FROM dogma_attributes WHERE attribute_id in ({','.join(['?']*len(attribute_ids))}) ORDER BY name"
    cur.execute(q, attribute_ids)
    attribs = cur.fetchall()
    attrib_ids_to_display_names = {}
    for attrib in attribs:
        if attrib["display_name"] != "":
            attrib_ids_to_display_names[attrib["attribute_id"]] = attrib["display_name"]
        else:
            attrib_ids_to_display_names[attrib["attribute_id"]] = attrib["name"]

    for attrib in item_attribs:
        if attrib["attribute_id"] not in blacklisted_attribute_ids:
            summary += (attrib_ids_to_display_names[attrib["attribute_id"]].ljust(30)) + ("(#" + str(attrib["attribute_id"]) + "):").ljust(10) + "%f\n" % (attrib["value"])

    return summary

def item_matrix(type_id):
    db_conn = database.get_db_conn()
    cur = db_conn.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute('''
        SELECT c.price, ao.dogma_attributes FROM abyssal_observations ao
        LEFT JOIN contracts c ON c.contract_id=ao.contract_id
        WHERE ao.type_id=?''', (type_id,))

    matrix = []

    while True:
        item = cur.fetchone()

        if item == None:
            break

        attribs = json.loads(item["dogma_attributes"])

        attribs_dict = {}
        for attrib in attribs:
            if attrib["attribute_id"] not in blacklisted_attribute_ids:
                attribs_dict[attrib["attribute_id"]] = attrib["value"]

        attribs_values = list(attribs_dict.values())

        vector = [item["price"]] + attribs_values
        matrix.append(vector)

    return matrix
        