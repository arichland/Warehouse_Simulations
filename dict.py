_author_ = 'arichland'

localhost = {
    'user': '',
    'password': '',
    'host': '',
    'database': '',
    'charset': ''
}

sql_queries = {"master_data": """INSERT INTO tbl_wms_master_data(reference_id, reference_name, storage_location) VALUES(%s, %s, %s);""",
               "coordinates": """INSERT INTO tbl_wms_coordinates(storage_location, x_coordinate, y_coordinate) VALUES(%s, %s, %s);""",
               "orders": """INSERT INTO tbl_wms_orders(timestamp, reference_id, quantity, destination) VALUES(%s, %s, %s, %s);"""
               }