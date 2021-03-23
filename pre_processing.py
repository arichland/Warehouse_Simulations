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

for i in range(len(d)):
    start_loc = (1, 12)
    y_low = 1
    y_high = 12
    loc1 = d[i+1]['item_coord']
    loc2 = d[i+1]['dest_coord']

    #dist = cd.distance_picking(loc1, loc2, 1, 12)



list_locs = [[1, 12], [19, 12], [2, 2], [10, 12]]
start_loc = (1, 1)
y_low = 1
y_high = 12

#cd.next_location(start_loc, list_locs, y_low, y_high)
cd.create_picking_route(start_loc, list_locs, y_low, y_high)
