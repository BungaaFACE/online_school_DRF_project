# online_school_DRF_project  
## Описание  
Проект включает в себя api сервер для онлайн школы

## Первоначальная настройка  
- Создать виртуальное окружение и войти в него.  
- Установка зависимостей --> `pip install -r r.txt`  
- Переименовать файл .env.tpl --> .env и заполнить его.
- Создание БД --> `python manage.py migrate`
## Наполнение данными  
### Superuser  
- Команда: `python manage.py csu`
- Логин: admin@gmail.com
- Пароль: admin
### Пользователи  
- Команда: `python manage.py add_users`  
- Назначение: создает пользователей user1 - user5 @gmail.com  
- Пароль: user  
### Уроки и курсы  
- Команда: `python manage.py add_learn_material`  
- Назначение: создает пять курсов по пять уроков  
### Оплаты  
- Команда: `python manage.py add_payments`  
- Назначение: создает записи оплаты  
## Шаги реализации  
### Шаг первый  
- Знакомство с ModelViewSet и Generics для создания API.
- Знакомство с PostMan для отладки API.  
- Созданы модели: Пользователь, Курс, урок.  
- Описаны CRUD для моделей курса и урока, но при этом для курса сделаны через ViewSets, а для урока — через Generic-классы.  
- Реализован эндпоинт для редактирования профиля любого пользователя и просмотра списка профилей на основе Generic.  
### Шаг второй  
- Знакомство с вложенными сериализаторами, кастомными полями сериализатора, GenericForeignKey.  
- Для модели курса в сериализатор добавлено поле вывода количества уроков.  
- Создана новая модель платежи с полями:  
  - пользователь  
  - дата оплаты  
  - оплаченный курс или урок  
  - сумма оплаты  
  - способ оплаты: наличные или перевод на счет  
- Для сериализатора модели курса реализовано поле вывода уроков.  
- Настроена фильтрация для эндпоинтов вывода списка платежей с возможностями:  
  - менять порядок сортировки по дате оплаты  
  - фильтровать по названию курса или урока  
  - фильтровать по способу оплаты  
- Для профиля пользователя сделан вывод истории платежей.  