## Описание
Простой скрипт для получения информации о температуре из городов, написанные в ```Cities.txt```.
## Запуск:
Написать в консоли ```python <место расположения скрипта>```. Например ```python c:/script.py```. 

Для работы скрипта файл ```Cities.txt``` должен находиться в той же директории, что и скрипт.
## Пример вывода:
```
Date:  11.10.2026 23:31:39

Cities:
City                Country               Temp  Humidity    Wind
----------------------------------------------------------------
Moscow              Russia              +11 °C      60 % 10 km/h
Khabarovsk          Russia               +6 °C      67 %  5 km/h
Saint-Petersburg    Russia               +8 °C      94 %  7 km/h
Vienna              Austria             +14 °C      51 % 16 km/h
Izhevsk             Russia               +7 °C      82 % 14 km/h
Perm                Russia               +9 °C      79 % 17 km/h
NhaTrang            Vietnam             +25 °C      91 % 12 km/h
Villach             Austria              +4 °C      88 %  4 km/h
----------------------------------------------------------------

Grouped by country:
Country    Cities    Avg    Min    Max    Humidity    Wind
----------------------------------------------------------
Austria         2  +9 °C  +4 °C +14 °C        70 % 10 km/h
Russia          5  +8 °C  +6 °C +11 °C        76 % 11 km/h
Vietnam         1 +25 °C +25 °C +25 °C        91 % 12 km/h
----------------------------------------------------------
```