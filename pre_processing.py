_author_ = 'arichland'
import pydict
import pymysql
from datetime import datetime
import calculate_distance as cd

def import_dataset():
    sql = pydict.localhost.get
    user = sql('user')
    pw = sql('password')
    host = sql('host')
    db = sql('database')
    count = 0
    dt = datetime
    data = {}
    headers = []

    con = pymysql.connect(user=user, password=pw, host=host, database=db)
    with con.cursor() as cur:
        try:
            query = """
                SELECT 
                tbl_wms_orders.timestamp, 
                tbl_wms_orders.sku, tbl_wms_orders.quantity, 
                tbl_wms_coordinates.location AS poo, 
                tbl_wms_coordinates.x_coordinate AS poo_x, 
                tbl_wms_coordinates.y_coordinate AS poo_y, 
                tbl_wms_coordinates_1.location AS pod, 
                tbl_wms_coordinates_1.x_coordinate AS pod_x, 
                tbl_wms_coordinates_1.y_coordinate AS pod_y
                FROM tbl_wms_coordinates AS tbl_wms_coordinates_1 
                INNER JOIN (tbl_wms_coordinates INNER JOIN tbl_wms_orders ON tbl_wms_coordinates.id = tbl_wms_orders.fk_poo) ON tbl_wms_coordinates_1.id = tbl_wms_orders.fk_pod
                ORDER BY tbl_wms_orders.timestamp ASC;"""
            cur.execute(query)
            col = cur.description
            rows = cur.fetchall()

            for i in range(len(col)):
                headers.append(col[i][0])

            # SQL query to dict
            for row in rows:
                count += 1
                temp_dict = {count: {
                    headers[0]: dt.isoformat(row[0]),
                    headers[1]: row[1],
                    headers[2]: row[2],
                    headers[3]: row[3],
                    headers[4]: row[4],
                    headers[5]: row[5],
                    headers[6]: row[6],
                    headers[7]: row[7],
                    headers[8]: row[8],
                    "poo_coord": (row[4], row[5]),
                    "pod_coord": (row[7], row[8])
                }}
                data.update(temp_dict)
        finally:
            con.commit()
    cur.close()
    con.close()
    return data

def import_dataset_original():
    sql = pydict.localhost.get
    user = sql('user')
    pw = sql('password')
    host = sql('host')
    db = sql('database')
    count = 0
    dt = datetime
    data = {}
    headers = []

    con = pymysql.connect(user=user, password=pw, host=host, database=db)
    with con.cursor() as cur:
        try:
            qry_create_table = """
             SELECT 
             tbl_wms_orders.timestamp, 
             tbl_wms_master_data.reference_id, 
             tbl_wms_master_data.reference_name, 
             tbl_wms_orders.quantity, 
             tbl_wms_master_data.storage_location, 
             tbl_wms_orders.destination
             FROM (tbl_wms_master_data INNER JOIN tbl_wms_coordinates ON tbl_wms_master_data.storage_location = tbl_wms_coordinates.storage_location) 
             INNER JOIN tbl_wms_orders ON tbl_wms_master_data.reference_id = tbl_wms_orders.reference_id
             ORDER BY tbl_wms_orders.timestamp ASC;"""
            cur.execute(qry_create_table)
            col = cur.description
            rows = cur.fetchall()

            for i in range(len(col)):
                headers.append(col[i][0])

            for row in rows: # SQL query to dict
                count += 1

                # Get item x,y coordinates
                item_loc = row[4]
                item_lgt = len(row[4])
                item_dash = item_loc.find("-")
                item_x_coord = item_loc[0:item_dash]
                item_y_coord = item_loc[item_dash + 1: item_lgt]
                item_coorid = [item_x_coord, item_y_coord]

                # Get destination x,y coordinates
                dest_loc = row[5]
                dest_lgt = len(row[5])
                dest_dash = dest_loc.find("-")
                dest_x = dest_loc[0:dest_dash]
                dest_y = dest_loc[dest_dash + 1: dest_lgt]
                dest_coord = [dest_x, dest_y]

                # Save data to dictionary
                temp_dict = {count: {
                    headers[0]: dt.isoformat(row[0]),
                    headers[1]: row[1],
                    headers[2]: row[2],
                    headers[3]: row[3],
                    headers[4]: row[4],
                    headers[5]: row[5],
                    "item_coord": item_coorid,
                    "dest_coord": dest_coord
                }}
                data.update(temp_dict)

        finally:
            con.commit()
    cur.close()
    con.close()
    return data



import_dataset()

d = import_dataset()

y_low = 0
y_high = 130
origin = (0, 0)
picks = []

for i in range(len(d)):
    poo = d[i+1]['poo']
    pod = d[i+1]['pod']
    picks.append(d[i+1]['poo_coord'])
    loc1 = d[i+1]['poo_coord']
    end = d[i+1]['pod_coord']
    print(poo, loc1)





#cd.next_location(origin, picks, y_low, y_high)
print("\nRoute")
cd.create_picking_route(origin, picks, y_low, y_high)
#cd.create_picking_route(start_loc, list_locs, y_low, y_high)
