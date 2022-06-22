import random
next_product_id = None
next_product_id_read = 0
product_shortforms = {'Hamburger'  : 'HAM', 
                      'Pizza'  : 'PIZ', 
                      'Pide'   : 'PDE',
                      'Kebap'  : 'KBP',
                      'Doner': 'DNR'}


class Product :

    @staticmethod
    def get_product_details(pysql, product_id) :
        sql_stmt =  'SELECT Product_ID, Name, Category, Seller, Price ' \
                    'FROM Product ' \
                    'WHERE Product_ID = %s'

        pysql.run(sql_stmt, (product_id, ))
        products = pysql.result

        return products


    @staticmethod
    def check_if_in_stock(pysql, customer_id, product_id, quantity) :
        sql_stmt =  'SELECT Quantity ' \
                    'FROM Product ' \
                    'WHERE Product_ID = %s'

        pysql.run(sql_stmt, (product_id, ))
        ans = pysql.result

        if (ans[0][0] - quantity) < 0 :
            return 0
        else :
            ans = ans[0][0] - quantity
            sql_stmt =  'SELECT Prod_ID1, Prod_ID2, Prod_ID3, Prod_ID4, Prod_ID5 ' \
                        'FROM Cart ' \
                        'WHERE Customer_ID = %s'

            pysql.run(sql_stmt, (customer_id, ))
            row = pysql.result
            for i in range(0, 5) :
                if row[0][i] is not None :
                    if row[0][i] == product_id :
                        ans = ans - 1
                        if ans < 0 :
                            return 0
            return 1


    @staticmethod
    def get_product_by_category(pysql, category) :
        sql_stmt =  'SELECT Product_ID, Name, Price, Rating, Seller_Name ' \
                    'FROM Product ' \
                    'LEFT JOIN Seller ' \
                    'ON Product.Seller = Seller.Seller_ID ' \
                    'WHERE Category = %s'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products

    @staticmethod
    def get_product_sorted_by_price_asc(pysql) :
        sql_stmt =  'SELECT Name, Seller, Rating, Price ' \
                    'FROM Product ' \
                    'ORDER BY Price ASC'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products

    @staticmethod
    def get_product_sorted_by_price_desc(pysql) :
        sql_stmt =  'SELECT Name, Seller, Rating, Price ' \
                    'FROM Product ' \
                    'ORDER BY Price DESC'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products


    @staticmethod
    def get_product_sorted_by_rating_desc(pysql) :
        sql_stmt =  'SELECT Name, Seller, Rating, Price ' \
                    'FROM Product ' \
                    'ORDER BY Rating DESC'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products

    # Minimum fiyata sahip en yuksek puanli urunuleri vermesi icin
    @staticmethod
    def get_product_sorted_by_price_asc_rating_desc(pysql) :
        sql_stmt =  'SELECT Name, Seller, Rating, Price ' \
                    'FROM Product ' \
                    'ORDER BY Rating DESC, Price ASC'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products

    @staticmethod
    def get_product_sorted_by_rating_desc_price_asc(pysql) :
        sql_stmt =  'SELECT Name, Seller, Rating, Price ' \
                    'FROM Product ' \
                    'ORDER BY Price ASC, Rating DESC'

        pysql.run(sql_stmt, (category, ))
        products = pysql.result

        return products

    