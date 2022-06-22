import random
from OdsLib.Cart import Cart
next_order_id = None
next_order_id_read = 0

class Orders :

    @staticmethod
    def place_order(pysql, customer_id, adres_id, payment_method) :

        letters = list(map(chr, range(ord('A'), ord('Z')+1)))
        l1 = letters[random.choice([i for i in range(0, 26)])]
        l2 = letters[random.choice([i for i in range(0, 26)])]

        global next_order_id
        global next_order_id_read

        if not next_order_id_read :
            sql_stmt =  'SELECT COUNT(*) ' \
                        'FROM Orders'
            pysql.run(sql_stmt)
            next_order_id = pysql.scalar_result
            next_order_id_read = 1

        order_id = l1 + l2 + '-' + format(next_order_id, '07d')

        # Toplamı bulmak için product ve cart tabloları
        total = Cart.get_total(pysql, customer_id)

        sql_stmt =  'INSERT INTO Orders ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, (SELECT CURRENT_TIMESTAMP))'

        try :
            pysql.run(sql_stmt, (order_id, customer_id, adres_id, total, payment_method, "Not Delivered"))

            pysql.commit()

            next_order_id += 1

            # order_id, product_id ile beraber OrderDetails Tablosuna ekleniyor
            sql_stmt =  'SELECT * ' \
                        'FROM Cart ' \
                        'WHERE Customer_ID = %s'
            pysql.run(sql_stmt, (customer_id, ))
            row = pysql.result

            for i in range(1, 6) :
                if row[0][i] is not None :
                    sql_stmt =  'INSERT INTO OrderDetails ' \
                                'VALUES (%s, %s)'
                    pysql.run(sql_stmt, (order_id, row[0][i]));
                    pysql.commit()

            # Stoktaki ürün miktarını azaltmak için
            for i in range(1, 6) :
                if row[0][i] is not None :
                    sql_stmt =  'UPDATE Product ' \
                                'SET Quantity = Quantity - 1 ' \
                                'WHERE Product_ID = %s'
                    pysql.run(sql_stmt, (row[0][i], ))
                    pysql.commit()

            # Ürün miktarı sıfır olursa (stokta yok), kaldırmak için
            sql_stmt =  'DELETE FROM Product ' \
                        'WHERE Quantity = 0'
            pysql.run(sql_stmt)
            pysql.commit()


            # Sepeti Boşalt
            Cart.clear_cart(pysql, customer_id)


        except :
            return 0
           
    # Tüm siparişleri görmek için 
    @staticmethod
    def get_order_details(pysql, customer_id) :

        sql_stmt =  'WITH T1 AS ( ' \
                        'SELECT Orders.Order_ID, Order_Date, Payment_Method, Product_ID ' \
                        'FROM Orders INNER JOIN OrderDetails ' \
                        'ON Orders.Order_ID = OrderDetails.Order_ID ' \
                        'WHERE Customer_ID = %s) ' \
                    'SELECT Order_Date, Order_ID, Product.Product_ID, Name, Payment_Method, Price ' \
                    'FROM Product INNER JOIN T1 ' \
                    'ON T1.Product_ID = Product.Product_ID ' \
                    'ORDER BY Order_ID'

        pysql.run(sql_stmt, (customer_id, ))
        orders = pysql.result

        return orders
