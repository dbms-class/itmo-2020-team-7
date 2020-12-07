import cherrypy

from connect import parse_cmd_line
from connect import create_connection


@cherrypy.expose
class App:
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "This web application was made by ITMO team 7"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            print(self.args)
            cur = db.cursor()
            cur.execute("SELECT id, tradename, intern_name FROM Drug")
            drugs = cur.fetchall()
        return [{"id": str(drug[0]),
                 "tradename": drug[1],
                 "inn": drug[2]} for drug in drugs]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, address FROM Pharmacy_shop")
            pharmacies = cur.fetchall()
        return [{"id": pharmacy[0], "address": pharmacy[1]} for pharmacy in pharmacies]
    
    """
    def get_drug_id(cursor, new_drug_id, new_pharmacy_id, new_price):
        cursor.execute(f"SELECT id from Pharmacy_drug where id={new_drug_id} AND pharmacy_shop_id={new_pharmacy_id} AND price={new_price}")
        res = []
        new_drug_ids = cursor.fetchall()
        for drug in new_drug_ids:
            res.append(drug[0])
        if len(new_drug_ids) == 0:
            return None
        return res[0]
    """
    
    @cherrypy.expose
    def update_retail(self, drug_id: int, pharmacy_id: int, remainder: int, price: float):
        with create_connection(self.args) as db:
            cur = db.cursor()      
            cur.execute("INSERT INTO Pharmacy_drug (id, pharmacy_shop_id, amount, price) "
                        "VALUES (%s, %s, %s, %s) ON CONFLICT (id, pharmacy_shop_id, price) DO UPDATE "
                        "SET amount = %s", (drug_id, pharmacy_id, remainder, price, remainder))
            
        db.commit()
        return "Data inserted"
        

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8888,
})
cherrypy.quickstart(App(parse_cmd_line()))
