-- ============================================
-- KATEGORIA
-- ============================================
INSERT INTO Kategoria (id_kat, nazwa, opis) VALUES
(1, 'Laptopy', 'Komputery przenośne do pracy i rozrywki'),
(2, 'Smartfony', 'Nowoczesne telefony komórkowe'),
(3, 'Akcesoria komputerowe', 'Myszy, klawiatury i inne urządzenia peryferyjne'),
(4, 'Telewizory', 'Telewizory LED, OLED i QLED różnych rozmiarów'),
(5, 'Sprzęt audio', 'Głośniki, słuchawki, soundbary i inne urządzenia dźwiękowe'),
(6, 'Monitory', 'Ekrany do komputerów stacjonarnych'),
(7, 'Drukarki', 'Urządzenia drukujące i skanujące');

-- ============================================
-- PRODUCENT
-- ============================================
INSERT INTO Producent (id_firmy, nazwa, opis, id_kat) VALUES
(1, 'Dell', 'Producent komputerów i akcesoriów biurowych', 1),
(2, 'Samsung', 'Producent elektroniki użytkowej i AGD', 2),
(3, 'Logitech', 'Producent akcesoriów komputerowych i audio', 3),
(4, 'Sony', 'Producent sprzętu audio-wideo i gier', 5),
(5, 'HP', 'Producent laptopów, drukarek i sprzętu biurowego', 7),
(6, 'LG', 'Producent monitorów i telewizorów', 4),
(7, 'Apple', 'Producent sprzętu komputerowego i mobilnego klasy premium', 2);

-- ============================================
-- PRODUKT
-- ============================================
INSERT INTO Produkt (id_prod, nazwa, opis, cena, stan_rzeczywisty, stan_wirtualny, id_kat, id_firmy, jednostka, ilosc) VALUES
(1, 'Dell Inspiron 15', 'Laptop 15.6" z procesorem Intel i5, 16GB RAM, SSD 512GB', 3299.00, 8, 8, 1, 1, 'szt.', 1),
(2, 'Dell XPS 13', 'Ultrabook premium z ekranem dotykowym', 5499.00, 5, 5, 1, 1, 'szt.', 1),
(3, 'Samsung Galaxy S24', 'Smartfon 6.2", 256GB, aparat 50MP', 3999.00, 12, 12, 2, 2, 'szt.', 1),
(4, 'Apple iPhone 15', 'Flagowy smartfon Apple 128GB', 4899.00, 10, 9, 2, 7, 'szt.', 1),
(5, 'Logitech MX Master 3S', 'Bezprzewodowa mysz ergonomiczna', 399.00, 15, 15, 3, 3, 'szt.', 1),
(6, 'Logitech G Pro Keyboard', 'Klawiatura mechaniczna gamingowa', 549.00, 10, 9, 3, 3, 'szt.', 1),
(7, 'Sony WH-1000XM5', 'Bezprzewodowe słuchawki z ANC', 1599.00, 7, 7, 5, 4, 'szt.', 1),
(8, 'Sony HT-S400', 'Soundbar 2.1 z subwooferem', 1199.00, 4, 4, 5, 4, 'szt.', 1),
(9, 'LG OLED55C3', 'Telewizor OLED 55" 4K HDR', 6299.00, 3, 3, 4, 6, 'szt.', 1),
(10, 'Samsung QLED50Q80', 'Telewizor QLED 50" 4K', 4299.00, 6, 6, 4, 2, 'szt.', 1),
(11, 'HP LaserJet Pro M255dw', 'Drukarka laserowa kolorowa Wi-Fi', 1099.00, 9, 9, 7, 5, 'szt.', 1),
(12, 'LG UltraGear 27GP850', 'Monitor 27" QHD, 165Hz, Nano IPS', 1899.00, 8, 8, 6, 6, 'szt.', 1),
(13, 'Apple AirPods Pro 2', 'Słuchawki bezprzewodowe z ANC', 1399.00, 11, 11, 5, 7, 'szt.', 1),
(14, 'HP Envy 13', 'Laptop 13" i7, 16GB RAM, SSD 1TB', 4799.00, 6, 6, 1, 5, 'szt.', 1),
(15, 'Logitech Z407', 'Głośniki 2.1 Bluetooth', 499.00, 10, 10, 5, 3, 'szt.', 1);
