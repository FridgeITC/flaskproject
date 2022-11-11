CREATE TABLE `zone` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `local` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `zoneId` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (zoneId) REFERENCES zone(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `fridge` (
  `id` int NOT NULL AUTO_INCREMENT,
  `localId` int NOT NULL,
  `capacity` int NOT NULL,
  `rows` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (localId) REFERENCES local(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `catalog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `imageRecord` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fridgeId` int NOT NULL,
  `resource` varchar(255) NOT NULL,
  `at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (fridgeId) REFERENCES fridge(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `productId` int DEFAULT NULL,
  `productLocationX` int NOT NULL,
  `productLocationY` int NOT NULL,
  `imageId` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (productId) REFERENCES catalog(id),
  FOREIGN KEY (imageId) REFERENCES imageRecord(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(89) NOT NULL,
  `password` varchar(255) NOT NULL,
  `localId` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (localId) REFERENCES local(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;