CREATE TABLE `weather` (
  `fcstDate` date DEFAULT NULL COMMENT '\\n',
  `fcstTime` time DEFAULT NULL COMMENT '\\n',
  `TMP` float DEFAULT NULL COMMENT '1시간 온도',
  `VEC` float DEFAULT NULL COMMENT '풍향',
  `WSD` float DEFAULT NULL COMMENT '풍속',
  `SKY` int DEFAULT NULL COMMENT '하늘 상태',
  `PTY` int DEFAULT NULL COMMENT '강수 형태',
  `POP` float DEFAULT NULL COMMENT '강수확률',
  `PCP` varchar(5) DEFAULT NULL COMMENT '1시간 강수량',
  `REH` float DEFAULT NULL COMMENT '습도',
  `SNO` varchar(5) DEFAULT NULL COMMENT '1시간 신적설',
  `TMN` float DEFAULT NULL COMMENT '하루 최저 기온',
  `TMM` float DEFAULT NULL COMMENT '하루 최고 기온\n'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
