-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 10, 2026 at 05:34 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `devfest_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `adm_id` bigint(20) NOT NULL,
  `adm_role` enum('super','manager') NOT NULL,
  `adm_full_name` varchar(150) NOT NULL,
  `adm_email` varchar(150) NOT NULL,
  `adm_password_hash` varchar(255) NOT NULL,
  `adm_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`adm_id`, `adm_role`, `adm_full_name`, `adm_email`, `adm_password_hash`, `adm_created_at`) VALUES
(1, 'super', 'Super Administrator', 'admin@devfest.com', 'scrypt:32768:8:1$u2vO4ngqfJeA15I7$6ea6f76fa88959bb044d1f459d5c4de7704018b36d64426c84dcae04b73c1a40407893f1a3fb599eccf9a402926583bb27719baa580a276c104e552bde755221', '2026-03-10 16:17:44');

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('197bdc37085b');

-- --------------------------------------------------------

--
-- Table structure for table `conversations`
--

CREATE TABLE `conversations` (
  `con_id` bigint(20) NOT NULL,
  `con_title` varchar(200) DEFAULT NULL,
  `con_content` text NOT NULL,
  `con_created_by` bigint(20) DEFAULT NULL,
  `con_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `conversations`
--

INSERT INTO `conversations` (`con_id`, `con_title`, `con_content`, `con_created_by`, `con_created_at`) VALUES
(1, 'I am looking forward to meet fellow coders like me', 'I am very excited tpo attend the developers\' festival.I can\'t wait!!!', 10, '2026-03-05 14:07:24'),
(2, 'Who is Driving to the venue?', 'I will like to go with anyine who us driving down. Just comment here annd let me know', 10, '2026-03-05 14:08:17'),
(3, 'Is there any WhatsApp group for prospective participant?', 'It is a nice idea for us to communicate on Whatspp. If you dont mind, I will create one. My phone number is 008765678999', 11, '2026-03-05 14:15:52');

-- --------------------------------------------------------

--
-- Table structure for table `conversation_messages`
--

CREATE TABLE `conversation_messages` (
  `msg_id` bigint(20) NOT NULL,
  `msg_conversation_id` bigint(20) NOT NULL,
  `msg_user_id` bigint(20) DEFAULT NULL,
  `msg_message` text NOT NULL,
  `msg_sent_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `ord_id` bigint(20) NOT NULL,
  `ord_user_id` bigint(20) NOT NULL,
  `ord_ticket_id` bigint(20) DEFAULT NULL,
  `ord_order_ref` varchar(50) DEFAULT NULL,
  `ord_total_amount` decimal(10,2) NOT NULL,
  `ord_status` enum('pending','paid','cancelled','refunded') DEFAULT NULL,
  `ord_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`ord_id`, `ord_user_id`, `ord_ticket_id`, `ord_order_ref`, `ord_total_amount`, `ord_status`, `ord_created_at`) VALUES
(1, 11, 1, 'ebbb0e3b40b282e7d631', 20000.00, 'pending', '2026-03-10 14:16:18'),
(2, 11, 2, 'c539abef3cc866c59387', 10000.00, 'pending', '2026-03-10 14:31:00'),
(3, 11, 2, 'b56088c003dc1870c032', 10000.00, 'pending', '2026-03-10 14:40:01'),
(4, 11, 2, 'e6e243a3a7b83b16cc1b', 10000.00, 'pending', '2026-03-10 15:38:19'),
(5, 11, 1, 'a74b697e102a9854a5fa', 20000.00, 'pending', '2026-03-10 15:43:14'),
(6, 11, 2, '51ba498a043fc8e8b769', 10000.00, 'pending', '2026-03-10 15:51:07'),
(7, 11, 1, 'd6c50f486d0f4a0b9b94', 20000.00, 'paid', '2026-03-10 16:13:43');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `pay_id` bigint(20) NOT NULL,
  `pay_order_id` bigint(20) NOT NULL,
  `pay_payment_ref` varchar(100) DEFAULT NULL,
  `pay_amount` decimal(10,2) NOT NULL,
  `pay_status` enum('pending','successful','failed') NOT NULL,
  `pay_paid_at` datetime DEFAULT NULL,
  `pay_created_at` datetime DEFAULT NULL,
  `pay_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`pay_data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`pay_id`, `pay_order_id`, `pay_payment_ref`, `pay_amount`, `pay_status`, `pay_paid_at`, `pay_created_at`, `pay_data`) VALUES
(1, 4, 'e6e243a3a7b83b16cc1b', 10000.00, 'pending', NULL, '2026-03-10 15:38:21', NULL),
(2, 4, 'e6e243a3a7b83b16cc1b', 10000.00, 'pending', NULL, '2026-03-10 15:40:27', NULL),
(3, 4, 'e6e243a3a7b83b16cc1b', 10000.00, 'pending', NULL, '2026-03-10 15:40:52', NULL),
(4, 4, 'e6e243a3a7b83b16cc1b', 10000.00, 'pending', NULL, '2026-03-10 15:43:05', NULL),
(5, 5, 'a74b697e102a9854a5fa', 20000.00, 'pending', NULL, '2026-03-10 15:43:16', NULL),
(6, 6, '51ba498a043fc8e8b769', 10000.00, 'pending', NULL, '2026-03-10 15:51:09', NULL),
(7, 7, 'd6c50f486d0f4a0b9b94', 20000.00, 'successful', NULL, '2026-03-10 16:13:45', '{\"id\": 5921447660, \"domain\": \"test\", \"status\": \"success\", \"reference\": \"d6c50f486d0f4a0b9b94\", \"receipt_number\": null, \"amount\": 2000000, \"message\": null, \"gateway_response\": \"Successful\", \"paid_at\": \"2026-03-10T16:13:55.000Z\", \"created_at\": \"2026-03-10T16:13:47.000Z\", \"channel\": \"card\", \"currency\": \"NGN\", \"ip_address\": \"154.118.40.142\", \"metadata\": {\"referrer\": \"http://127.0.0.1:8081/\"}, \"log\": {\"start_time\": 1773159231, \"time_spent\": 5, \"attempts\": 1, \"errors\": 0, \"success\": true, \"mobile\": false, \"input\": [], \"history\": [{\"type\": \"action\", \"message\": \"Attempted to pay with card\", \"time\": 4}, {\"type\": \"success\", \"message\": \"Successfully paid with card\", \"time\": 5}]}, \"fees\": 40000, \"fees_split\": null, \"authorization\": {\"authorization_code\": \"AUTH_qm66po63gz\", \"bin\": \"408408\", \"last4\": \"4081\", \"exp_month\": \"12\", \"exp_year\": \"2030\", \"channel\": \"card\", \"card_type\": \"visa \", \"bank\": \"TEST BANK\", \"country_code\": \"NG\", \"brand\": \"visa\", \"reusable\": true, \"signature\": \"SIG_zrbfIfyjPNYFLzHlGr24\", \"account_name\": null, \"receiver_bank_account_number\": null, \"receiver_bank\": null}, \"customer\": {\"id\": 345986350, \"first_name\": null, \"last_name\": null, \"email\": \"soji@yahoo.com\", \"customer_code\": \"CUS_xfbnxk3hahiifxx\", \"phone\": null, \"metadata\": null, \"risk_action\": \"default\", \"international_format_phone\": null}, \"plan\": null, \"split\": {}, \"order_id\": null, \"paidAt\": \"2026-03-10T16:13:55.000Z\", \"createdAt\": \"2026-03-10T16:13:47.000Z\", \"requested_amount\": 2000000, \"pos_transaction_data\": null, \"source\": null, \"fees_breakdown\": null, \"connect\": null, \"transaction_date\": \"2026-03-10T16:13:47.000Z\", \"plan_object\": {}, \"subaccount\": {}}');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `ses_id` bigint(20) NOT NULL,
  `ses_title` varchar(200) NOT NULL,
  `ses_description` text DEFAULT NULL,
  `ses_track_id` bigint(20) DEFAULT NULL,
  `ses_start_time` datetime DEFAULT NULL,
  `ses_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`ses_id`, `ses_title`, `ses_description`, `ses_track_id`, `ses_start_time`, `ses_created_at`) VALUES
(1, 'Opening Keynote: The Future of AI and Coders', 'Join industry leaders as they discuss the transformative power of Artificial Intelligence in software development. ', 4, '2026-03-06 14:05:13', '2026-03-06 09:05:27'),
(2, 'Panel: Diversity & Inclusion in Tech', 'A candid conversation about building inclusive teams and products.', 4, '2026-03-06 14:06:07', '2026-03-06 14:06:07'),
(3, 'How to Install Laravel App', 'In this session, attendees learn the basis of Laravel installation', 1, '2026-03-06 14:07:24', '2026-03-06 14:07:24'),
(4, 'Developing a Distributed System', 'This is an advaced session for those who have the mind to face advanced tpopics', 3, '2026-03-06 14:08:02', '2026-03-06 14:08:02'),
(5, 'Finding Mid-Level Jobs as a Developer', 'This session invites all intermediate developers to a serious matter', 2, '2026-03-06 14:08:02', '2026-03-06 14:08:02');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `tkt_id` bigint(20) NOT NULL,
  `tkt_name` varchar(150) NOT NULL,
  `tkt_description` text DEFAULT NULL,
  `tkt_price` decimal(10,2) NOT NULL,
  `tkt_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`tkt_id`, `tkt_name`, `tkt_description`, `tkt_price`, `tkt_created_at`) VALUES
(1, 'VIP Ticket', 'This ticket allows you to sit in the front', 20000.00, '2026-03-10 13:22:25'),
(2, 'Regular', 'Access all conference proceedings with handfan', 10000.00, '2026-03-10 13:23:26');

-- --------------------------------------------------------

--
-- Table structure for table `tracks`
--

CREATE TABLE `tracks` (
  `trk_id` bigint(20) NOT NULL,
  `trk_level` enum('general','intermediate','advanced','junior') NOT NULL,
  `trk_created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tracks`
--

INSERT INTO `tracks` (`trk_id`, `trk_level`, `trk_created_at`) VALUES
(1, 'junior', '2026-03-06 09:20:13'),
(2, 'intermediate', '2026-03-06 03:58:40'),
(3, 'advanced', '2026-03-06 05:58:57'),
(4, 'general', '2026-03-06 05:59:18');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `usr_id` bigint(20) NOT NULL,
  `usr_firstname` varchar(150) NOT NULL,
  `usr_lastname` varchar(100) NOT NULL,
  `usr_email` varchar(150) NOT NULL,
  `usr_password_hash` varchar(255) NOT NULL,
  `usr_summary` varchar(150) DEFAULT NULL,
  `usr_image` varchar(150) DEFAULT NULL,
  `usr_track_id` bigint(20) DEFAULT NULL,
  `usr_created_at` datetime DEFAULT NULL,
  `usr_updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`usr_id`, `usr_firstname`, `usr_lastname`, `usr_email`, `usr_password_hash`, `usr_summary`, `usr_image`, `usr_track_id`, `usr_created_at`, `usr_updated_at`) VALUES
(10, 'Tinubu', 'Ahmed', 'ahmed@yahoo.com', 'scrypt:32768:8:1$sibHLIoyo9R3YHt3$4190f2acf16e587fb54b4d5907ab24fa2a657869b399ba9e98f0a060f85c2749563a75769de9582870f63b67c26b24b6dd703a27f383039c3b135573229a6f99', NULL, NULL, NULL, '2026-03-05 08:16:25', NULL),
(11, 'Adeola', 'Bakare', 'soji@yahoo.com', 'scrypt:32768:8:1$u2vO4ngqfJeA15I7$6ea6f76fa88959bb044d1f459d5c4de7704018b36d64426c84dcae04b73c1a40407893f1a3fb599eccf9a402926583bb27719baa580a276c104e552bde755221', 'Hello world', '88692f0ad578d4c0677b.jpg', 4, '2026-03-05 14:13:55', '2026-03-06 14:12:38');

-- --------------------------------------------------------

--
-- Table structure for table `user_session`
--

CREATE TABLE `user_session` (
  `use_id` int(11) NOT NULL,
  `use_userid` bigint(20) NOT NULL,
  `use_sessionid` bigint(20) NOT NULL,
  `use_datereg` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`adm_id`),
  ADD UNIQUE KEY `adm_email` (`adm_email`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`con_id`),
  ADD KEY `con_created_by` (`con_created_by`);

--
-- Indexes for table `conversation_messages`
--
ALTER TABLE `conversation_messages`
  ADD PRIMARY KEY (`msg_id`),
  ADD KEY `msg_conversation_id` (`msg_conversation_id`),
  ADD KEY `msg_user_id` (`msg_user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`ord_id`),
  ADD UNIQUE KEY `ord_order_ref` (`ord_order_ref`),
  ADD KEY `ord_ticket_id` (`ord_ticket_id`),
  ADD KEY `ord_user_id` (`ord_user_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`pay_id`),
  ADD KEY `pay_order_id` (`pay_order_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`ses_id`),
  ADD KEY `ses_track_id` (`ses_track_id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`tkt_id`);

--
-- Indexes for table `tracks`
--
ALTER TABLE `tracks`
  ADD PRIMARY KEY (`trk_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`usr_id`),
  ADD UNIQUE KEY `usr_email` (`usr_email`),
  ADD KEY `usr_track_id` (`usr_track_id`);

--
-- Indexes for table `user_session`
--
ALTER TABLE `user_session`
  ADD PRIMARY KEY (`use_id`),
  ADD KEY `use_sessionid` (`use_sessionid`),
  ADD KEY `use_userid` (`use_userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `adm_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `conversations`
--
ALTER TABLE `conversations`
  MODIFY `con_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `conversation_messages`
--
ALTER TABLE `conversation_messages`
  MODIFY `msg_id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `ord_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `pay_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `ses_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `tkt_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tracks`
--
ALTER TABLE `tracks`
  MODIFY `trk_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `usr_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `user_session`
--
ALTER TABLE `user_session`
  MODIFY `use_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `conversations`
--
ALTER TABLE `conversations`
  ADD CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`con_created_by`) REFERENCES `users` (`usr_id`) ON DELETE SET NULL;

--
-- Constraints for table `conversation_messages`
--
ALTER TABLE `conversation_messages`
  ADD CONSTRAINT `conversation_messages_ibfk_1` FOREIGN KEY (`msg_conversation_id`) REFERENCES `conversations` (`con_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `conversation_messages_ibfk_2` FOREIGN KEY (`msg_user_id`) REFERENCES `users` (`usr_id`) ON DELETE SET NULL;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`ord_ticket_id`) REFERENCES `tickets` (`tkt_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`ord_user_id`) REFERENCES `users` (`usr_id`) ON DELETE CASCADE;

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`pay_order_id`) REFERENCES `orders` (`ord_id`) ON DELETE CASCADE;

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`ses_track_id`) REFERENCES `tracks` (`trk_id`) ON DELETE SET NULL;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`usr_track_id`) REFERENCES `tracks` (`trk_id`) ON DELETE SET NULL;

--
-- Constraints for table `user_session`
--
ALTER TABLE `user_session`
  ADD CONSTRAINT `user_session_ibfk_1` FOREIGN KEY (`use_sessionid`) REFERENCES `sessions` (`ses_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_session_ibfk_2` FOREIGN KEY (`use_userid`) REFERENCES `users` (`usr_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
