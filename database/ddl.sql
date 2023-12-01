SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

CREATE OR REPLACE TABLE Product_Types

(
    product_type_id int  NOT NULL,
    description integer NOT NULL,
    PRIMARY KEY (product_type_id)
);

CREATE OR REPLACE TABLE Customers
(
    customer_id integer       NOT NULL AUTO_INCREMENT,
    name        varchar(255) NOT NULL,
    email       varchar(255) NOT NULL,
    password    varchar(255) NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE OR REPLACE TABLE Orders
(
    order_id    integer        NOT NULL AUTO_INCREMENT,
    customer_id integer        NOT NULL,
    order_date  date           NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
);

CREATE OR REPLACE TABLE Scents
(
    scent_id    integer      NOT NULL AUTO_INCREMENT,
    description varchar(255) NOT NULL,
    PRIMARY KEY (scent_id)
);

CREATE OR REPLACE TABLE Products
(
    product_id integer            NOT NULL AUTO_INCREMENT,
    scent          integer        NOT NULL,
    price          decimal(19, 2) NOT NULL,
    product_type   integer        NOT NULL,
    inventory      integer        NOT NULL,
    PRIMARY KEY (product_id),
    FOREIGN KEY (scent) REFERENCES Scents (scent_id)
);

CREATE OR REPLACE TABLE Orders_Products
(
    order_id          integer NOT NULL,
    product_id        integer NOT NULL,
    product_quantitiy integer NOT NULL,
    CONSTRAINT FK_Order_Product PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products (product_id) ON UPDATE CASCADE
);

INSERT INTO Product_Types (product_type_id, description)
VALUES ('1', 'Bath Soap'),
       ('2', 'Shaving Soap'),
       ('3', 'Shampoo');

INSERT INTO Customers (name, email, password)
VALUES ('Briana Dickerson', 'Briana@email.com', 'password'),
       ('Tristan Hunter', 'Tristan@email.com', 'password'),
       ('Jewell Carpenter', 'Jewell@email.com', 'password'),
       ('Heath Allen', 'Heath@email.com', 'password');

INSERT INTO Orders (customer_id, order_date)
VALUES (2, '2022-10-01'),
       (4, '2023-02-22'),
       (3, '2023-06-15'),
       (1, '2023-10-15');

INSERT INTO Scents (scent_id, description)
VALUES ('1', 'Bergamot Blast'),
       ('2', 'Bay Rum'),
       ('3', 'Peppermint Patty');

INSERT INTO Products (scent, price, product_type, inventory)
VALUES ('1', 7.00, '1', 20),
       ('2', 20.00, '2', 10),
       ('3', 8.00, '3', 16);

INSERT INTO Orders_Products (order_id, product_id, product_quantitiy)
VALUES (1, 1, 2),
       (1, 3, 1),
       (2, 2, 1),
       (3, 3, 3),
       (3, 2, 1),
       (4, 1, 1);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
