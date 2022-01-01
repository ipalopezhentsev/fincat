Takes monthly dump of your transactions in Raiffeisen Bank Russia (you download it from your personal account in Raiffeisen Online)
and categorizes them into broad categories like groceries, gifts etc using supplied rules file which is simple substring matcher.
It finds subtotals of each group so you can easily record your monthly expenses as part of home accounting.

Run it like this (no extra libraries are needed):

```python3 fincat.py --rules-file rules.csv account_statement_01.12.21-01.01.22.csv```

Example of `rules.csv` file that will categorize as Photo expenses having titles including text 'Adobe', 'AWS', or 'FOTOSEYL':
```
SRC_SUBSTRING;TRG_CATEGORY
Adobe;Photo
AWS;Photo
FOTOSEYL;Photo
```

Example of transactions file `account_statement_01.12.21-01.01.22.csv`:
```
Дата транзакции;Описание;Валюта операции;Сумма в валюте операции;Валюта счета;Сумма в валюте счета
29.12.2021 00:00;APPLE.COM/BILL MOSKVA RUS;RUB;-59.00;RUB;-59.00
```

Note that by default files downloaded from Raiffeisen Online will be in 'alien' encoding that will display Russian
characters incorrectly on a Mac. You need to convert it to UTF8 first prior to running the program:
```commandline
iconv -f WINDOWS-1251 -t UTF-8 account_statement_01.12.21-01.01.22.csv > account_statement_01.12.21-01.01.22.csv
```