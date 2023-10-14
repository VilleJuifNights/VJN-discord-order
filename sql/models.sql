create table orders (
    id uuid primary key,
    user_id varchar(255) not null,
    pretty_id varchar(255) not null,
    status varchar(255) not null,
    timestamp timestamp not null,
    total_cost float not null,
    category varchar(255) not null
);

create table order_toppings (
    id uuid primary key,
    order_id uuid not null,
    name varchar(255) not null,
    foreign key (order_id) references orders(id)
);

