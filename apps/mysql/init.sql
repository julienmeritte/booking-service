CREATE USER 'clo5_user'@'%' IDENTIFIED BY 'XZe&pR5%2397';
GRANT ALL PRIVILEGES ON * . * TO 'clo5_user'@'%';
FLUSH PRIVILEGES;


CREATE TABLE IF NOT EXISTS hotel (
    id INT AUTO_INCREMENT,
    name VARCHAR(100) , 
    address VARCHAR(100) , 
    phone_number VARCHAR(100) ,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id)
);

CREATE TABLE IF NOT EXISTS room_category (
    id INT AUTO_INCREMENT,
    name VARCHAR(100),
    max_occupancy INT,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id)
);


CREATE TABLE IF NOT EXISTS additional_service (
    id INT AUTO_INCREMENT,
    name VARCHAR(100),
    max_number INT NOT NULL,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id)
);

CREATE TABLE IF NOT EXISTS hotel_room (
    id INT AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    room_number VARCHAR(10),
    category_id INT NOT NULL,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id),
    foreign key(hotel_id) references hotel(id),
    foreign key(category_id) references room_category(id)
);

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT,
    mail VARCHAR(100),
    password VARCHAR(100),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id)
);

CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    number_occupants INT NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 
    
    primary key(id),
    foreign key(hotel_id) references hotel(id),
    foreign key(room_id) references hotel_room(id),
    foreign key(user_id) references user(id)
);

CREATE TABLE IF NOT EXISTS reservation_additional_service (
    id INT AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    additional_service_id INT NOT NULL,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id),
    foreign key(reservation_id) references reservation(id),
    foreign key(additional_service_id) references additional_service(id)
);

CREATE TABLE IF NOT EXISTS role_permission (
    id INT AUTO_INCREMENT,
    name VARCHAR(100),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id)
);

CREATE TABLE IF NOT EXISTS role_user (
    id INT AUTO_INCREMENT,
    role_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id),
    foreign key(role_id) references role_permission(id),
    foreign key(user_id) references user(id)
);

CREATE TABLE IF NOT EXISTS discount_type (
    id INT AUTO_INCREMENT,
    name VARCHAR(100),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    primary key(id)
);

CREATE TABLE IF NOT EXISTS discount (
    id INT AUTO_INCREMENT,
    discount_type_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp, 

    primary key(id),
    foreign key(discount_type_id) references discount_type(id)
);
