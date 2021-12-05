-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Авг 13 2021 г., 10:58
-- Версия сервера: 10.4.20-MariaDB
-- Версия PHP: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `checkplace`
--

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Места для фото'),
(2, 'Памятники'),
(3, 'Необычные места'),
(4, 'Парки'),
(5, 'История');

-- --------------------------------------------------------

--
-- Структура таблицы `global_places`
--

CREATE TABLE `global_places` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `work_time` varchar(255) DEFAULT NULL,
  `more_description` varchar(255) DEFAULT NULL,
  `landmarks` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `geo_link` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `global_places`
--

INSERT INTO `global_places` (`id`, `name`, `description`, `work_time`, `more_description`, `landmarks`, `image`, `geo_link`, `category_id`) VALUES
(1, 'Памятник Тарасу Шевченко', 'Памятник украинскому поэту, писателю и художнику Шевченко Т.Г, был открыт в Ташкенте 20 декабря 2002 года. На открытии памятника присутствовал Президент Украины Леонид Кучма. Этот район города восстанавливался после ташкентского землетрясения в том числе и рабочими, приехавшими из Украинской ССР.', NULL, '-Огромная красочная мазайка на стене 110 школы, со всех ракурсов смотритсься красиво. \r\n-По дороге слева в сторону Цума  множество закусочных и магазинов', 'Ближайшее метро: выход Мингурюк (м. Айбек). Тратуары хорошие, район ухоженный', '0838085_b.jpeg', 'https://yandex.ru/maps/org/pamyatnik_tarasu_shevchenko/89673666950', 2);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `telegram_id` int(12) NOT NULL,
  `name` varchar(255) NOT NULL,
  `birth` varchar(255) NOT NULL,
  `last_place_post` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `telegram_id`, `name`, `birth`, `last_place_post`) VALUES
(1, 77415762, 'Cidarop', '19.07.2001', 1627830233),
(2, 90309172, 'Tanya', '06.07.1978', 1628843731);

-- --------------------------------------------------------

--
-- Структура таблицы `users_places`
--

CREATE TABLE `users_places` (
  `id` int(11) NOT NULL,
  `telegram_id` int(12) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `work_time` varchar(255) DEFAULT NULL,
  `more_description` varchar(255) DEFAULT NULL,
  `landmarks` varchar(255) DEFAULT NULL,
  `geo_link` varchar(500) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `status` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users_places`
--

INSERT INTO `users_places` (`id`, `telegram_id`, `name`, `description`, `work_time`, `more_description`, `landmarks`, `geo_link`, `filename`, `status`) VALUES
(10, 77415762, 'Test', 'Test', '', '', '', 'Test', '2986IMG_20210731_013405_123.jpg', 0),
(11, 77415762, 'Test2', 'Test2', '', '', '', 'Test2', '2300IMG_20210731_013409_232.jpg', 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `global_places`
--
ALTER TABLE `global_places`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users_places`
--
ALTER TABLE `users_places`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `global_places`
--
ALTER TABLE `global_places`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `users_places`
--
ALTER TABLE `users_places`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
