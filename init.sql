-- Таблица с данными о погоде за день
CREATE TABLE IF NOT EXISTS today_day_weather (
    today_day_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    date_id DATE NOT NULL,
    temp_avg FLOAT NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    wind_avg FLOAT NOT NULL,
    wind_min FLOAT NOT NULL,
    wind_max FLOAT NOT NULL,
    humidity_avg FLOAT NOT NULL,
    humidity_min FLOAT NOT NULL,
    humidity_max FLOAT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location_weather(location_id),
    FOREIGN KEY (date_id) REFERENCES date_weather(date_id)
);

-- Таблица с данными о погодных предупреждениях
CREATE TABLE IF NOT EXISTS alerts_weather (
    alerts_weather_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    date_id DATE NOT NULL,
    temperature FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location_weather(location_id),
    FOREIGN KEY (date_id) REFERENCES date_weather(date_id)
);

-- Таблица с данными реального времени о погоде
CREATE TABLE IF NOT EXISTS real_time_weather (
    real_time_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    retrieved_at DATETIME NOT NULL,
    temperature FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location_weather(location_id)
);

-- Таблица с данными о местоположении
CREATE TABLE IF NOT EXISTS location_weather (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    name_region VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Таблица с данными о датах
CREATE TABLE IF NOT EXISTS date_weather (
    date_id DATE PRIMARY KEY,
    day INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL
);

-- Таблица с прогнозом погоды
CREATE TABLE IF NOT EXISTS forecast_weather (
    forecast_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    date_id DATE NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    temp_avg FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location_weather(location_id),
    FOREIGN KEY (date_id) REFERENCES date_weather(date_id)
);

-- Таблица с логами API-запросов
CREATE TABLE IF NOT EXISTS api_requests_log (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    request VARCHAR(255) NOT NULL,
    location_id INT NOT NULL,
    request_time DATETIME NOT NULL,
    status_code INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location_weather(location_id)
);
