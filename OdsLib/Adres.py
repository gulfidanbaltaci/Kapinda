next_adres_id = None
next_adres_id_read = 0
class Adres :
    @staticmethod
    def add_customer_adres(pysql, customer_id, pincode, street, landmark, state, addr_type, city) :

        global next_adres_id
        global next_adres_id_read

        if not next_adres_id_read :
            sql_stmt =  'SELECT COUNT(*) ' \
                        'FROM Adres'
            pysql.run(sql_stmt)
            next_adres_id = pysql.scalar_result
            next_adres_id_read = 1 

        adres_id = format(next_adres_id, '06d')
        print(adres_id)
        sql_stmt =  'INSERT INTO Adres ' \
                    'VALUES ('+ "\""+str(customer_id)+"\"" \
                        +","+ "\""+str(adres_id)+"\"" \
                            +","+ "\""+pincode+"\"" \
                                 +","+ "\""+street+"\"" \
                                    +","+ "\""+landmark+"\"" \
                                        +","+ "\""+state+"\"" \
                                            +","+ "\""+addr_type+"\"" \
                                                 +","+ "\""+str(city)+"\"" +")" 
        print(sql_stmt)

        try : 
            x = pysql.run(sql_stmt)
            print(x)
            y = pysql.commit()
            print(y)
            next_adres_id += 1
            return 1 
        except :
            print(customer_id, adres_id, pincode, street, landmark, city, state, addr_type)
            return 0


    @staticmethod
    def view_all_adres_of_customer(pysql, customer_id) :
            
        sql_stmt =  'SELECT Adres_ID, Pincode, Street, Landmark, City_Name, State, Type \
                    FROM Adres \
                    LEFT JOIN City \
                    ON Adres.City = City.City_ID \
                    WHERE Customer_ID = %s' 

        pysql.run(sql_stmt, (customer_id, ))
        adreses = pysql.result

        return adreses



