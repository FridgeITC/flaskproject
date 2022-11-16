CREATE DATABASE nds;
USE nds;

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
  `id` int NOT NULL,
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

INSERT INTO catalog(id, name, price)
    VALUES
        (0, "topo_chico_600ml", 85),
        (1, "sprite_600ml", 18),
        (2, "fanta_600ml", 18),
        (3, "del_valle_frut_600ml", 15),
        (4, "senzao_600ml",17),
        (5, "coca_cola_355ml", 18),
        (6, "coca_cola_sin_azucar_botella_355ml",20),
        (7, "coca_cola_sin_azucar_600ml", 23),
        (8, "coca_cola_light_600ml", 18),
        (9, "fresca_600ml", 17),
        (10, "fuzetea_600ml", 15),
        (11, "sidral_manzana_600ml", 12),
        (12, "del_valle_manzana_413ml", 14),
        (13, "sidral_sangria_600ml", 13),
        (14, "limon_y_nada_600ml", 23),
        (15, "del_valle_guayaba_355ml", 20),
        (16, "naranja_y_nada_600ml", 19),
        (17, "coca_cola_light_botella_355ml", 16),
        (18, "coca_cola_sin_azucar_lata_355ml", 23),
        (19, "vitamin_water_ponche_frutas_500ml", 22),
        (20, "vitamin_water_citrico_tropical_500ml", 25),
        (21, "powerade_moras_600ml", 18),
        (22, "ciel_gasificada_pina_355ml", 12),
        (23, "ciel_natural_1l", 12),
        (24, "ciel_fresa_1l",  17),
        (25, "ciel_natural_600ml", 18),
        (26, "del_valle_durazno_413ml", 19),
        (27, "ciel_limon_1l", 22);
  /*
          This also are in the model, but cannot be infered yet
          28: vacio
          29: con_precio
          30: sin_precio
   */