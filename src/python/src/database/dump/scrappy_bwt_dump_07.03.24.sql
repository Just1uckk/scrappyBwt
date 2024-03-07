-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Мар 07 2024 г., 14:54
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `scrappy_bwt`
--

-- --------------------------------------------------------

--
-- Структура таблицы `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('d8a57762ed94');

-- --------------------------------------------------------

--
-- Структура таблицы `business_model`
--

CREATE TABLE `business_model` (
  `id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bbb_id` varchar(255) NOT NULL,
  `name` text,
  `address` varchar(768) DEFAULT NULL,
  `category` text,
  `web_url` varchar(768) DEFAULT NULL,
  `img_url` varchar(768) DEFAULT NULL,
  `detailed_url` varchar(768) NOT NULL,
  `phone` bigint UNSIGNED DEFAULT NULL,
  `fax` bigint UNSIGNED DEFAULT NULL,
  `hours` json DEFAULT NULL,
  `stars` varchar(255) DEFAULT NULL,
  `customer_reviews` varchar(255) DEFAULT NULL,
  `bbb_rating` varchar(255) DEFAULT NULL,
  `accredited_date` varchar(255) DEFAULT NULL,
  `social_media` json DEFAULT NULL,
  `years` varchar(255) DEFAULT NULL,
  `started_date` varchar(255) DEFAULT NULL,
  `parse_date` varchar(255) DEFAULT NULL,
  `contact_information` json DEFAULT NULL,
  `management` json DEFAULT NULL,
  `sent_to_customer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `sitemap_model`
--

CREATE TABLE `sitemap_model` (
  `id` bigint UNSIGNED NOT NULL,
  `status` mediumint UNSIGNED NOT NULL DEFAULT '0',
  `sitemap_url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `priority` mediumint UNSIGNED DEFAULT NULL,
  `attempt` mediumint UNSIGNED DEFAULT '0',
  `exception` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Индексы таблицы `business_model`
--
ALTER TABLE `business_model`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_business_model_bbb_id` (`bbb_id`),
  ADD KEY `ix_business_model_fax` (`fax`),
  ADD KEY `ix_business_model_phone` (`phone`);

--
-- Индексы таблицы `sitemap_model`
--
ALTER TABLE `sitemap_model`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_sitemap_model_priority` (`priority`),
  ADD KEY `ix_sitemap_model_status` (`status`),
  ADD KEY `ix_sitemap_pages_sitemap_url` (`sitemap_url`),
  ADD KEY `ix_sitemap_attempt` (`attempt`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `business_model`
--
ALTER TABLE `business_model`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `sitemap_model`
--
ALTER TABLE `sitemap_model`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
