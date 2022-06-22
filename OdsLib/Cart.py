class Cart :
    @staticmethod
    def add_product_to_cart(pysql, customer_id, product_id) :
        sql_stmt =  'SELECT * FROM Cart ' \
                    'WHERE Customer_ID = %s'

        pysql.run(sql_stmt, (customer_id, ))
        row = pysql.result

        i = 1
        while (i < 6) :
            if row[0][i] is None :
                break
            i += 1
        
        if i == 6 :
            return 0

        sql_stmt =  'UPDATE Cart ' \
                    'SET Prod_ID%s = %s ' \
                    'WHERE Customer_ID = %s'
        try :
            pysql.run(sql_stmt, (i, product_id, customer_id))
            pysql.commit()
            return 1

        except :
            print('Cart is Full')
            return 0

    @staticmethod
    def get_no_of_products_in_cart(pysql, customer_id) :

        sql_stmt =  'SELECT * FROM Cart ' \
                    'WHERE Customer_ID = %s'

        pysql.run(sql_stmt, (customer_id, ))
        row = pysql.result

        i = 1
        while (i < 6) :
            if row[0][i] is None :
                break
            i += 1
        
        return (i - 1)

    @staticmethod
    def clear_cart(pysql, customer_id) :

        sql_stmt =  'UPDATE Cart ' \
                    'SET Prod_ID1 = %s, Prod_ID2 = %s, Prod_ID3 = %s, Prod_ID4 = %s, Prod_ID5 = %s ' \
                    'WHERE Customer_ID = %s'

        pysql.run(sql_stmt, (None, None, None, None, None, customer_id))
        pysql.commit()

        return 1

    @staticmethod
    def get_prod_in_cart(pysql, customer_id) :
        sql_stmt =  'SELECT Prod_ID1, Prod_ID2, Prod_ID3, Prod_ID4, Prod_ID5 ' \
                    'FROM Cart ' \
                    'WHERE Customer_ID = %s'

        pysql.run(sql_stmt, (customer_id, ))
        products = pysql.result
        return products
   
    @staticmethod
    def get_total(pysql, customer_id) :

        product_ids = Cart.get_prod_in_cart(pysql, customer_id)

        total = 0
        for i in range(0, Cart.get_no_of_products_in_cart(pysql, customer_id)) :

            sql_stmt =  'SELECT Price ' \
                        'FROM Product ' \
                        'WHERE Product_ID = %s'

            pysql.run(sql_stmt, (product_ids[0][i], ))
            ans = pysql.result
            total += int(ans[0][0])
   
        return total 