INSERT INTO Form (name) VALUES ('Box');
INSERT INTO Form (name) VALUES ('Package');

INSERT INTO Producer (name) VALUES ('Тай Юн Медикал');
INSERT INTO Producer (name) VALUES ('Шариф Индастриз');
INSERT INTO Producer (name) VALUES ('Амбрелла Корп.');
INSERT INTO Producer (name) VALUES ('Биомагус Инк.');

INSERT INTO Laboratory (name, sndname_boss) VALUES ('Лаборатория в Китае', 'Фармацевт без диплома');
INSERT INTO Laboratory (name, sndname_boss) VALUES ('Психушка в outlast', 'Безумный док');
INSERT INTO Laboratory (name, sndname_boss) VALUES ('Домашняя лаборатория', 'Мамкин ученый');

INSERT INTO Certificate (number, validity, laboratory_id) VALUES (1, '2020-12-12', 1);
INSERT INTO Certificate (number, validity, laboratory_id) VALUES (2, '2020-12-12', 2);
INSERT INTO Certificate (number, validity, laboratory_id) VALUES (3, '2020-12-12', 3);

INSERT INTO Active_agent (name, formula) VALUES ('Водичка', 'H2O');
INSERT INTO Active_agent (name, formula) VALUES ('Водочка', 'C2H5OH');

INSERT INTO Drug (tradename, intern_name, form_id, producer_id, certificate_id, active_agent_id)
VALUES ('Панацелин', 'Лекарство намбер 1', 1, 4, 2, 1);
INSERT INTO Drug (tradename, intern_name, form_id, producer_id, certificate_id, active_agent_id)
VALUES ('Озверин', 'от стресса', 2, 3, 1, 2);
INSERT INTO Drug (tradename, intern_name, form_id, producer_id, certificate_id, active_agent_id)
VALUES ('Боевой стимулятор', 'Легальный допинг', 2, 2, 3, 2);

INSERT INTO Package_type (name)
VALUES ('Капсула');
INSERT INTO Package_type (name)
VALUES ('Таблетка');

INSERT INTO Pharmacy_shop (address) VALUES ('Иванова 6');
INSERT INTO Pharmacy_shop (address) VALUES ('Петрова 8');
INSERT INTO Pharmacy_shop (address) VALUES ('Ковалева 11');
INSERT INTO Pharmacy_shop (address) VALUES ('Козлова 1');

INSERT INTO Sale_package (drug_id, package_type_id, price) 
VALUES (1, 1, 10)

INSERT INTO Pharmacy_drug (pharmacy_shop_id, sale_package_id, price, amount)
VALUES (1, 1, 10, 2)
=======
VALUES (1, 1, 10);

INSERT INTO Pharmacy_drug (pharmacy_shop_id, sale_package_id, price, amount)
VALUES (1, 1, 10, 2);
