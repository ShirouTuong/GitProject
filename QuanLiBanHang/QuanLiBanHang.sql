CREATE DATABASE IF NOT EXISTS QuanLyBanHang;

USE QuanLyBanHang;

CREATE TABLE Customer (
    cID INT PRIMARY KEY,
    cName VARCHAR(100) NOT NULL,
    cAge INT,
    CONSTRAINT chk_customer_age CHECK (cAge > 0)
);

CREATE TABLE Product (
    pID INT PRIMARY KEY,
    pName VARCHAR(100) NOT NULL,
    pPrice DECIMAL(12,2) NOT NULL,
    CONSTRAINT chk_product_price CHECK (pPrice > 0)
);

CREATE TABLE `Order` (
    oID INT PRIMARY KEY,
    cID INT NOT NULL,
    oDate DATE NOT NULL,
    oTotalPrice DECIMAL(12,2) NOT NULL DEFAULT 0,

    CONSTRAINT fk_order_customer
        FOREIGN KEY (cID)
        REFERENCES Customer(cID),

    CONSTRAINT chk_order_total
        CHECK (oTotalPrice >= 0)
);

CREATE TABLE OrderDetail (
    oID INT NOT NULL,
    pID INT NOT NULL,
    odQTY INT NOT NULL,

    PRIMARY KEY (oID, pID),

    CONSTRAINT fk_orderdetail_order
        FOREIGN KEY (oID)
        REFERENCES `Order`(oID),

    CONSTRAINT fk_orderdetail_product
        FOREIGN KEY (pID)
        REFERENCES Product(pID),

    CONSTRAINT chk_orderdetail_qty
        CHECK (odQTY > 0)
);