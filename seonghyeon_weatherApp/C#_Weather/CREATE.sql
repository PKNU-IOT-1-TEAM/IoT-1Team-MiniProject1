CREATE TABLE `getfludmarksdata` (
  `Idx` int NOT NULL AUTO_INCREMENT,
  `OBJT_ID` int NOT NULL,
  `FLUD_SHIM` double NOT NULL,
  `FLUD_GD` int NOT NULL,
  `FLUD_AR` double NOT NULL,
  `FLUD_YEAR` varchar(4) NOT NULL,
  `FLUD_NM` varchar(50) NOT NULL,
  `FLUD_NM2` varchar(254) NOT NULL,
  `SAT_DATE` varchar(8) NOT NULL,
  `END_DATE` varchar(8) NOT NULL,
  `SAT_TM` varchar(4) NOT NULL,
  `END_TM` varchar(4) NOT NULL,
  `CTPRVN_CD` varchar(2) NOT NULL,
  `SGG_CD` varchar(5) NOT NULL,
  `EMD_CD` varchar(8) NOT NULL,
  PRIMARY KEY (`Idx`)
)