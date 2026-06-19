# 🛡️ SIEM-система на базе Elastic Stack для кадрового агентства

---

## 📌 Краткое описание

Данный проект представляет собой функциональный прототип SIEM-системы.

## 🛠️ Инструменты и технологии

| Компонент | Назначение |
|-----------|------------|
| **Elasticsearch** | Хранение и индексация логов |
| **Kibana** | Визуализация, дашборды, система оповещений |
| **Winlogbeat** | Сбор событий с Windows (AD, файловый сервер) |
| **Filebeat** | Сбор логов Suricata |
| **Suricata** | Обнаружение сетевых атак (NIDS) |
| **VirtualBox** | Виртуализация стенда |
| **CentOS 9** | Сервер Elastic Stack |
| **Windows 10 / Server 2019** | Клиентские системы |
| **Astra Linux** | Дополнительный агент 

## 🧪 Экспериментальная часть

### Топология стенда

Эксперимент проводился на гипервизоре **Virtual Box** с использованием сетевого моста (Bridge) для обеспечения взаимодействия между виртуальными машинами.

![Схема топологии](./images/cxema.jpg)

---

### Настройка Elastic Stack

На сервер CentOS 9 была выполнена установка Elasticsearch и Kibana. После запуска служб веб-интерфейс Kibana стал доступен с хостовой системы.

![Приветственная страница Kibana](./images/elasticwelcome.jpg)

В разделе **Discover** была проверена доставка логов от агентов.

![Логи в Discover](./images/logs.jpg)

---

### Настройка сбора событий Active Directory

Для сбора событий Active Directory был создан отдельный Data View в Kibana.

![Data View для AD](./images/ad_dataview.jpg)

В разделе Discover отображаются события, поступающие с контроллера домена через Winlogbeat.

![События AD в Discover](./images/ad_logs.jpg)

Было разработано правило для обнаружения попытки смены пароля в AD.

![Правило для AD](./images/ad_rule.jpg)

---

### Тестирование встроенных правил Elastic Security

#### Обнаружение сканирования портов

С помощью **nmap** было выполнено сканирование сетевых портов Elastic-сервера.

![Результат сканирования nmap](./images/nmap_result.jpg)

Система зафиксировала события типа **"Potential Network Scan"** и **"Potential SYN-Based Port Scan"**, что подтверждает эффективность встроенных правил.

---

#### Обнаружение Brute Force SSH

С помощью инструмента **Hydra** была выполнена атака подбора паролей на SSH-сервис.

![Hydra атака](./images/hydra1.jpg)

В Kibana зафиксировано событие **"Potential Password Spraying attack via SSH"**.

![Результат Hydra](./images/hydra1_result.jpg)

Аналогичная атака была проведена на агент с **Astra Linux**.

![Hydra на Astra](./images/hydra2.jpg)

Событие успешно зафиксировано в Kibana с указанием источника — агента Astra.

![Результат с агента Astra](./images/hydra2_result.jpg)

---

### Настройка пользовательских правил

#### Интеграция Suricata

В инфраструктуру была внедрена система обнаружения вторжений **Suricata**. Для проверки работы было создано сигнатурное правило, обнаруживающее ICMP Flood (превышение частоты ICMP-пакетов).

![Правило Suricata](./images/suricata_rule.jpg)

После проведения атаки в лог-файлах Suricata появились записи "ICMP FLOOD DETECTED".

![Логи Suricata](./images/suricata_logs.jpg)

События были успешно доставлены в Kibana через Filebeat.

![События Suricata в Kibana](./images/discover_suricata.jpg)

Запуск ICMP Flood атаки:

![ICMP Flood скрипт](./images/icmp_flood.jpg)

В разделе **Alerts** зафиксирован сигнал тревоги от правила Suricata.

![Результат ICMP Flood](./images/kibana_icmp_flood.jpg)




