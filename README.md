В ./python_stripe_test сконфигурировать .env с переменными STRIPE_SECRET_KEY,
STRIPE_PUBLISHABLE_KEY, SECRET_KEY (django secret key), DATABASE_URL.

Установка и запуск с помощью Poetry:
$ poetry install
$ poetry migrate
$ poetry python_stripe_test/manage.py runserver

Решение на Replit: https://python-stripe-test--vtitova1.replit.app