# sonraki CustomerID tamsayısını saklaması için
next_customer_id = None
next_customer_id_read = 0

class Customer :

    # Customerın veritabanında olup olmadığını bulmak için
    # veritabanında bulunursa 1, bulmazsa 0
    @staticmethod
    def check_customer_signin(pysql, email, Sifre) :
        sql_stmt =  'SELECT Customer_ID, Email, Sifre '\
                    'FROM Customer'
        pysql.run(sql_stmt)
        data = pysql.result

        for i in data :
            if i[1] == email and i[2] == Sifre :
                return i[0] 
        return False 

    @staticmethod
    def customer_signup(pysql, Ad, Soyad, email, Sifre, Telefon_no, Telefon_no2 ) :
        global next_customer_id
        global next_customer_id_read

        if not next_customer_id_read :
            sql_stmt =  'SELECT COUNT(*) ' \
                        'FROM Customer'
            pysql.run(sql_stmt)
            next_customer_id = pysql.scalar_result
            next_customer_id_read = 1 

        customer_id = 'C' + format(next_customer_id, '05d')

        sql_stmt =  'INSERT INTO Customer ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)' 

        try : 
            pysql.run(sql_stmt, (customer_id, Ad, Soyad, email, Sifre, Telefon_no, Telefon_no2))

            pysql.commit()
            
            sql_stmt =  'INSERT INTO Cart(Customer_ID) ' \
                        'VALUES (%s)'
            pysql.run(sql_stmt, (customer_id, ))
            pysql.commit()

            next_customer_id += 1
            return customer_id

        except :
            return 0



    @staticmethod
    def get_customer_profile(pysql, customer_id) :
        sql_stmt =  'SELECT Ad, Soyad, Email, Telefon_no, Telefon_no2 ' \
                    'FROM Customer ' \
                    'WHERE Customer_ID = %s'
        try :
            pysql.run(sql_stmt, (customer_id, )) 
            profile = pysql.result
            return profile

        except :
            return 0



    @staticmethod
    def update_customer_profile(pysql, customer_id, Ad, Soyad, email, Telefon_no, Telefon_no2) :
        sql_stmt =  'UPDATE Customer ' \
                    'SET Ad = '+ "\""+ Ad + "\""+ \
                        ', Soyad = '+ "\""+ Soyad + "\""+ \
                            ' ,Email = '+ "\""+ email + "\""+ \
                                ' ,Telefon_no = '+ "\""+ Telefon_no + "\""+ \
                                    ' ,Telefon_no2 = '+ "\""+ Telefon_no2 + "\""+ \
                                        'WHERE Customer_ID = '+ "\""+ customer_id + "\""
        print(sql_stmt)
        try :
            pysql.run(sql_stmt)
            pysql.commit()
            return 1

        except :
            return 0