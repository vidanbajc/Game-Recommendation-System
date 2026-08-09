-- create database game_recommender;
-- use game_recommender;

create table games (
    id int primary key,
    name varchar(255) not null,
    released date,
    rating decimal(3,2),
    ratings_count int,
    metacritic int,
    playtime int,
    esrb_rating varchar(50),
    image_url varchar(500)
);

create table genres (
    id int primary key,
    name varchar(100) unique not null
);

create table game_genres (
    game_id int,
    genre_id int,
    primary key (game_id, genre_id),
    foreign key (game_id) references games(id),
    foreign key (genre_id) references genres(id)
);

create table platforms (
    id int primary key,
    name varchar(100) unique not null
);

create table game_platforms (
    game_id int,
    platform_id int,
    primary key (game_id, platform_id),
    foreign key (game_id) references games(id),
    foreign key (platform_id) references platforms(id)
);

create table tags (
    id int primary key,
    name varchar(100) unique not null
);

create table game_tags (
    game_id int,
    tag_id int,
    primary key (game_id, tag_id),
    foreign key (game_id) references games(id),
    foreign key (tag_id) references tags(id)
);