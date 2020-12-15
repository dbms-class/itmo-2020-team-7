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
    

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_retail(self, drug_id, pharmacy_id, remainder, price):
          with create_connection(self.args) as db: 
              cur = db.cursor()
              cur.execute(
                  "SELECT * FROM Pharmacy_drug "
                  "WHERE id = %s AND pharmacy_shop_id = %s",
                  (drug_id, pharmacy_id)
                  )

              if cur.fetchone() is not None:
                  cur.execute(
                      "UPDATE Pharmacy_drug "
                      "SET amount = %s, price = %s "
                      "WHERE id = %s AND pharmacy_shop_id = %s",
                      (remainder, price, drug_id, pharmacy_id)
                      )
                  key = 'Data updated'
              else:
                      cur.execute(
                          "INSERT INTO Pharmacy_drug "
                          "(id, pharmacy_shop_id, sale_package_id, amount, price) "
                          "VALUES (%s, %s, %s, %s, %s)",
                          (drug_id, pharmacy_id, '1', remainder, price)
                          )
                      key = 'Data inserted'     
              db.commit()
          return {key : 'ok'}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status_retail(self, drug_id=None, min_remainder=0, max_price=None):

        with create_connection(self.args) as db:
            cur = db.cursor()
            if drug_id is None:
                cur.execute("SELECT id FROM Drug")
                drug_ids = cur.fetchall()
            else:
                drug_ids = [drug_id]
            result = []
            for drug in drug_ids:
                if max_price is not None:
                    price_filter = "AND price <= {}".format(max_price)
                else:
                    price_filter = ""
                cur.execute("SELECT tradename, intern_name FROM Drug WHERE id = %s", drug)
                tradename_internname = cur.fetchall()
                cur.execute("SELECT id FROM Sale_package WHERE drug_id = %s", drug)
                id_sale_package = cur.fetchall
                cur.execute("SELECT pharmacy_shop_id, price, amount FROM Pharmacy_drug "
                            "WHERE sale_package_id = %s AND amount >= %s " + price_filter, id_sale_package,
                            min_remainder)
                pharmacyID_price_amount = cur.fetchall()
                min_price_ = pharmacyID_price_amount[0][1]
                max_price_ = -1
                addresses = []
                for elem in pharmacyID_price_amount:
                    min_price_ = min(min_price_, elem[1])
                    max_price_ = max(max_price_, elem[1])
                    cur.execute("SELECT address FROM Pharmacy_shop WHERE id = %s", elem[0])
                    addresses.append(cur.fetchall())
                for i, elem in enumerate(pharmacyID_price_amount):
                    result.append({
                        "drug_id": drug,
                        "drug_trade_name": tradename_internname[0],
                        "drug_inn": tradename_internname[1],
                        "pharmacy_id": elem[0],
                        "pharmacy_address": addresses[i],
                        "remainder": elem[2],
                        "price": elem[1],
                        "min_price": min_price_,
                        "max_price": max_price_})
            return result

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8888,
})
cherrypy.quickstart(App(parse_cmd_line()))
