# online_school_DRF_project  
## Описание  
Проект включает в себя api сервер для онлайн школы, системы пользователей, покупки кусров и уроков. Проведена интеграция с системой платежей Stripe.  

## Первоначальная настройка  
- Создать виртуальное окружение и войти в него.  
- Установка зависимостей --> `pip install -r r.txt`
- Установить redis --> `apt install redis`
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
### Модератор  
- Команда: `python manage.py cmoder`  
- Назначение: Создание пользователя и группы модераторов. Модераторы имеют права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые.  
- Логин: moder@gmail.com  
- Пароль: moder  
### Уроки и курсы  
- Команда: `python manage.py add_learn_material`  
- Назначение: создает пять курсов по пять уроков  
### Оплаты  
- Команда: `python manage.py add_payments`  
- Назначение: создает записи оплаты
### Включение блокировки неактивных пользователей  
- Команда: `python manage.py per_task_block_inactive_users`  
- Назначение: создает периодическую задачу по блокирвке неактивных пользователей (не заходили более 30 дней).  
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
### Шаг третий  
- Знакомство с Simple_jwt.  
- Настрено использование JWT-авторизации и закрыт каждый эндпоинт авторизацией.  
- Заведена группа модераторов и для нее описаны права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые.  
- Описаны права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть и редактировать только свои курсы и уроки.  
- Для профиля пользователя введены ограничения, чтобы авторизованный пользователь мог просматривать любой профиль, но редактировать только свой.  
- При просмотре чужого профиля доступна только общая информация, в которую не входят: пароль, фамилия, история платежей.  
- При изменении профиля пользователи не могут редактировать поля: пароль, is_superuser, is_staff, почта, 'is_active', группы, права доступа пользователя.  
### Шаг четвертый  
- Знакомство с валидаторами, пагинацией, тестированием DRF.  
- Для сохранения уроков и курсов реализована дополнительная проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.  
- Добавлена модель подписки на обновления курса для пользователя. Реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.  
- При выборке данных по курсу пользователю теперь присылается признак подписки текущего пользователя на курс.  
- Реализована пагинацию для вывода всех уроков и курсов.  
- Написаны тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.  
### Шаг пятый  
- Знакомство с Swagger, Redoc.  
- Знакомство с CORS для обеспечения безопасности связки фронт-бек.  
- Подключена документация для проекта.  
- Интегрирован Stripe для проведения платежей при покупке курсов/уроков. Инвойс выдается в виде ссылки оплаты через stripe.  
- Добавлена страница проверки статусов платежей stripe. При успешной оплате платеж добавляется в таблицу БД платежей.    
### Шаг шестой  
- Знакомство с Celery, Celery-beat.  
- Проект настроен для работы с Celery. Также настроен celery-beat для выполнения последующих задач.  
- Рассылка рассылку писем пользователям об обновлении материалов курса изменена на асинхронную.  
- Добавлена проверка покупки курса/урока при попытке сделать retrieve.  
- Добавлена периодическая задача для блокировки пользователей, которые заходили более 30 дней назад.  


