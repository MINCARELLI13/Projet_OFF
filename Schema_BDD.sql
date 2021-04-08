-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema BDD_OFF
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema BDD_OFF
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `BDD_OFF` DEFAULT CHARACTER SET utf8 ;
USE `BDD_OFF` ;

-- -----------------------------------------------------
-- Table `BDD_OFF`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `BDD_OFF`.`category` ;

CREATE TABLE IF NOT EXISTS `BDD_OFF`.`category` (
  `id` INT NULL,
  `name` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BDD_OFF`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `BDD_OFF`.`product` ;

CREATE TABLE IF NOT EXISTS `BDD_OFF`.`product` (
  `id` INT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `brand` VARCHAR(100) NOT NULL,
  `url` VARCHAR(100) NOT NULL,
  `nutriscore` CHAR(1) NOT NULL,
  `ingredients` VARCHAR(200) NOT NULL,
  `stores` VARCHAR(150) NULL,
  `category_id` INT NOT NULL,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  UNIQUE INDEX `brand_UNIQUE` (`brand` ASC) VISIBLE,
  UNIQUE INDEX `url_UNIQUE` (`url` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  INDEX `fk_product_category_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `BDD_OFF`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BDD_OFF`.`substitutes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `BDD_OFF`.`substitutes` ;

CREATE TABLE IF NOT EXISTS `BDD_OFF`.`substitutes` (
  `product_id` INT NOT NULL,
  `substitute_id` INT NOT NULL,
  PRIMARY KEY (`product_id`, `substitute_id`),
  INDEX `fk_product_has_product_product2_idx` (`substitute_id` ASC) VISIBLE,
  INDEX `fk_product_has_product_product1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_product_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `BDD_OFF`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_product_product2`
    FOREIGN KEY (`substitute_id`)
    REFERENCES `BDD_OFF`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
