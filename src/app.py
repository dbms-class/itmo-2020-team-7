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
                    price_filter = "AND PD.price <= {} ".format(max_price)
                else:
                    price_filter = ""

                cur.execute("SELECT D.tradename, D.intern_name, PS.id, PS.address, PD.amount, "
                            "PD.price, min(PD.price) OVER(), max(PD.price) OVER() "
                            "FROM Drug D "
                            "JOIN Sale_package SP ON SP.drug_id = D.id "
                            "JOIN Pharmacy_drug PD ON PD.sale_package_id = SP.id "
                            "JOIN Pharmacy_shop PS ON PS.id = PD.pharmacy_shop_id "
                            "WHERE D.id = %s AND PD.amount >= %s " + price_filter,
                            (drug, min_remainder))

                drug_result = cur.fetchall()
                for i, elem in enumerate(drug_result):
                    print(elem)
                    result.append({
                        "drug_id": drug,
                        "drug_trade_name": elem[0],
                        "drug_inn": elem[1],
                        "pharmacy_id": elem[2],
                        "pharmacy_address": elem[3],
                        "remainder": elem[4],
                        "price": elem[5],
                        "min_price": elem[6],
                        "max_price": elem[7]})

            return result

          
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drug_move(self, drug_id, min_remainder, target_income_increase):
        current_income = 0
        result = []
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(
                "SELECT pd.id, amount, pharmacy_shop_id, pd.price FROM Drug d "
                "JOIN Sale_package sp ON d.id=sp.drug_id "
                "JOIN Pharmacy_drug pd ON sp.id=pd.sale_package_id "
                "WHERE d.id=%s"
                "ORDER BY pd.price",
                drug_id
            )
            query_result = cur.fetchall()
            negative_remainder = [data for data in query_result if (data[1] - int(min_remainder)) < 0]
            positive_remainder = [data for data in query_result if (data[1] - int(min_remainder)) >= 0]
            for to_be_increased in reversed(negative_remainder):
                i_id, i_amount, i_shop_id, i_price = to_be_increased
                for to_be_decreased in positive_remainder:
                    if current_income > int(target_income_increase):
                        break
                    d_id, d_amount, d_shop_id, d_price = to_be_decreased
                    to_add = int(d_amount) - int(min_remainder)
                    # Обновим значения для аптеки, в которой число лекарств увеличилось
                    cur.execute(
                        "UPDATE Pharmacy_drug SET amount=%s WHERE id=%s",
                        (int(i_amount) + int(to_add), i_id)
                    )
                    # Обновим значения для аптеки, в которой число лекарств уменьшилось
                    cur.execute(
                        "UPDATE Pharmacy_drug SET amount=%s WHERE id=%s",
                        (min_remainder, d_id)
                    )
                    result.append({
                        "from_pharmacy_id": d_shop_id,
                        "to_pharmacy_id": i_shop_id,
                        "price_difference": int(i_price) - int(d_price),
                        "count": to_add
                    })
                    current_income += int(i_price) * (int(i_amount) + int(to_add)) - int(d_price) * int(to_add)
        return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8888,
})
cherrypy.quickstart(App(parse_cmd_line()))
