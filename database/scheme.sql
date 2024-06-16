create database games;
use games;

-- Platform -- 
create table platform
(
name varchar(50) primary key
);

-- Game --
create table game
(
game_code int auto_increment primary key,
name varchar(100),
region varchar(20),
language varchar(100)
);


-- Has -- 
create table has
(
platform_name varchar(50),
game_code int,
constraint has_pk PRIMARY KEY (platform_name, game_code),
constraint platform_fk FOREIGN KEY (platform_name) REFERENCES platform (name)
ON UPDATE CASCADE ON DELETE CASCADE,
constraint games_fk FOREIGN KEY(game_code) REFERENCES game (game_code)
ON UPDATE CASCADE ON DELETE CASCADE
);

-- This procedure allows to input data in the "platform" table --
DELIMITER //
drop procedure if exists platform_input //
create procedure platform_input (P_NAME VARCHAR(50))
begin
	insert into platform 
    values (P_NAME);
end; //
DELIMITER ;

-- This procedure allows to input data in the "game" table --
DELIMITER //
drop procedure if exists game_input //
create procedure game_input (p_name varchar(100), p_region varchar(20), p_language varchar(100))
begin

	insert into game (name, region, language) values 
    (p_name, p_region, p_language);

end; //
DELIMITER ;

-- This procedure allows to input data in the "has" table --
DELIMITER //
drop procedure if exists has_input //
create procedure has_input (p_platform_name varchar(50), p_game_code int)
begin

	insert into has values 
    (p_platform_name, p_game_code);

end; //
DELIMITER ;