import cherrypy

from connect import parse_cmd_line
from connect import create_connection

from random import randint



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
     with create_connection(self.args) as db1:
      with create_connection(self.args) as db2:           
        with create_connection(self.args) as db:
            print(self.args)
            cur = db.cursor()
            #cur.execute("SELECT id, tradename, intern_name FROM Drug")
            cur.execute("SELECT * FROM Drug")
            drugs = cur.fetchall()
        return [{"id": str(drug[0]),
                 "tradename": drug[1],
                 "inn": drug[2]} for drug in drugs]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        num = randint(0, 9)
        if (num % 2) == 0:
           with create_connection(self.args) as db:
               pass
           return {"rake":""}
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

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8888,
})
cherrypy.quickstart(App(parse_cmd_line()))
