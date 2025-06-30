DROP TABLE assets;

CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(8)
);

insert into assets ( name ) 
values 
('ALUP4.SA'),
('BBAS3.SA'),
('BBDC3.SA'),
('CMIG4.SA'),
('ITSA4.SA'),
('ITUB3.SA'),
('TAEE3.SA');

select * from assets;
