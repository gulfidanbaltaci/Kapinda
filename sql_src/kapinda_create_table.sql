-- Drop database ODS if exists
DROP DATABASE IF EXISTS kapinda;
CREATE DATABASE kapinda;
USE kapinda;

-- Delete the schemas

DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Adres;
DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Cart;
DROP TABLE IF EXISTS Delivery;
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS Rating;

-- Create the schemas

CREATE TABLE Customer (
    Customer_ID     CHAR(6),
    Ad      VARCHAR(20),
    Soyad       VARCHAR(20),
    Email           VARCHAR(40),
    Sifre        VARCHAR(20),
    Telefon_no          CHAR(10),
    Telefon_no2          CHAR(10),
    CONSTRAINT Customer_PK PRIMARY KEY (Customer_ID)
);

CREATE TABLE City (
    City_ID        char(4), 
    City_Name       VARCHAR(70),
    CONSTRAINT City_PK PRIMARY KEY (City_ID)
);

CREATE TABLE Adres (
    Customer_ID     CHAR(6),
    Adres_ID      CHAR(6),
    Pincode         CHAR(6),
    Street          VARCHAR(20),
    Landmark        VARCHAR(20),
    State           VARCHAR(20),
    Type            CHAR(5),
    City			CHAR(6),
    CONSTRAINT Cart_City_FK FOREIGN KEY (City) REFERENCES City (City_ID) ON DELETE SET NULL,
    CONSTRAINT Adres_FK FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE CASCADE,
    CONSTRAINT Adres_PK PRIMARY KEY (Customer_ID, Adres_ID)
);

CREATE TABLE Orders (
    Order_ID            CHAR(10),
    Customer_ID         CHAR(6),
    Adres_ID          CHAR(6),
    Total_Price         NUMERIC(6, 0) UNSIGNED DEFAULT 0,
    Payment_Method      ENUM ("Cash On Delivery", "Debit Card", "Credit Card", "Net Banking"),
    Status              ENUM ("Delivered", "Not Delivered"),
    Order_Date          TIMESTAMP, 
    CONSTRAINT Orders_PK PRIMARY KEY (Order_ID),
    CONSTRAINT Orders_FK FOREIGN KEY (Customer_ID, Adres_ID) REFERENCES Adres (Customer_ID, Adres_ID) ON DELETE CASCADE
);


CREATE TABLE Delivery (
    Order_ID        CHAR(10), 
    ID              CHAR(6),
    CONSTRAINT Delivery_FK_1 FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID) ON DELETE CASCADE,
    CONSTRAINT Delivery_PK PRIMARY KEY (Order_ID, ID)
);

CREATE TABLE Seller (
    Seller_ID        CHAR(10), 
    Seller_Name       VARCHAR(70),
    CONSTRAINT Seller_PK PRIMARY KEY (Seller_ID)
);

CREATE TABLE Product (
    Product_ID      CHAR(10),
    Name            VARCHAR(20),
    Category        VARCHAR(20),
    Price           NUMERIC(6, 0) UNSIGNED DEFAULT 0,
    Rating          NUMERIC(2, 1) UNSIGNED DEFAULT 0,
    Seller          CHAR(10),
    Quantity        NUMERIC(3, 0) UNSIGNED DEFAULT 0,
    CONSTRAINT Cart_Seller_FK FOREIGN KEY (Seller) REFERENCES Seller (Seller_ID) ON DELETE SET NULL,
    CONSTRAINT Product_PK PRIMARY KEY (Product_ID)
);

CREATE TABLE Cart (
    Customer_ID     CHAR(6),
    Prod_ID1        CHAR(10),
    Prod_ID2        CHAR(10),
    Prod_ID3        CHAR(10),
    Prod_ID4        CHAR(10),
    Prod_ID5        CHAR(10),
    CONSTRAINT Cart_Customer_ID_FK FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE CASCADE,
    CONSTRAINT Cart_Prod_ID1_FK FOREIGN KEY (Prod_ID1) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID2_FK FOREIGN KEY (Prod_ID2) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID3_FK FOREIGN KEY (Prod_ID3) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID4_FK FOREIGN KEY (Prod_ID4) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID5_FK FOREIGN KEY (Prod_ID5) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Customer_PK PRIMARY KEY (Customer_ID)
);

CREATE TABLE OrderDetails (
    Order_ID        CHAR(10),
    Product_ID      CHAR(10),
    CONSTRAINT OrderDetails_FK_1 FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID) ON DELETE CASCADE,
    CONSTRAINT OrderDetails_FK_2 FOREIGN KEY (Product_ID) REFERENCES Product (Product_ID) ON DELETE CASCADE
);

CREATE TABLE Rating (
 Rating_ID int NOT NULL AUTO_INCREMENT,
 Order_ID int NOT NULL,
 Rate int NOT NULL,
 Comment varchar(30) DEFAULT NULL,
 PRIMARY KEY (Rating_ID)
);