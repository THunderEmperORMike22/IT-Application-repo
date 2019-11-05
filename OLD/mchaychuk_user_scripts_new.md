**Чайчук Михаил – «HR-Bot»**

**Пользовательские сценарии**

**Группа: 10 – МИ – 2**

**Электронная почта:** [mishac22@yandex.ru](mailto:mishac22@yandex.ru)

**VK:** https://vk.com/mike_c22

**!!! В процессе разработки проекта могут быть добавлены новые сценарии. Сценарии могут быть изменены или удалены, в соответствии с требованиями заказчика. !!!**

**[ Сценарий 1 – Начало работы / приветствие]**

1.	Пользователь отправляет команду /start 
2.	Если в данный момент утро (5:00 – 12:00), то программа присылает пользователю сообщение «Доброе утро!».
3.	Если в данный момент день (13:00 – 17:00), то бот присылает сообщение «Добрый день!».
4.	Если в данный момент вечер (18:00 – 24:00), то пользователь получает сообщение «Добрый вечер!».
5.	Если действие происходит от 1:00 до 4:00, то пользователь получает одно из нескольких «нейтральных» приветственных сообщений («Привет!», «Здравствуйте!» и т.д.).
6.	Пользователь также может получить любое из «нейтральных» сообщений в независимости от времени суток.
7.	Если общение начато командой /start, пользователь получает краткое сообщение с описанием бота.

**[ Сценарий 2 – Начало работы ]**

1.	Бот спрашивает пользователя, хочет ли он начать общение и предлагает ответить ему в формате «Да» / «Нет».
2.	На экране появляется мини-клавиатура с возможностью выбора «Да» и «Нет».
3.	Если пользователь выбирает «Нет» на клавиатуре или отправляет сообщением, то бот прощается с пользователем одним из возможных сообщений, поясняет, как снова начать общение, если пользователь передумает и завершает работу.
4.	Если пользователь выбирает «Да» на клавиатуре или отправляет сообщением, то бот отсылает пользователя в Стартовое меню.
5.	На экране появляется клавиатура с возможностью быстрого выбора одного из вариантов.
6.  Пользователь может продолжить работу с ботом или завершить её.

**[ Сценарий 3 – Стартовое меню]**

1.	Если  пользователь в п.2 сц.2 выбрал утвердительный ответ, то он попадает в Стартовое меню.
2.	Бот присылает сообщение о том, что для работы с ботом необходима авторизация. Бот предлагает пользователю осуществить вход в систему, войти как гость, или получить контакты людей, отвечающих на вопросы в разделе обратная связь.
3.  На экране появляется клавиатура с возможностью выбора варианта.
4.	Если пользователь выбирает на клавиатуре «Обратная связь» или отправляет соответствующее сообщение, то бот открывает соответствующий раздел.
5.	Если пользователь выбирает на клавиатуре «Войти как гость» или отправляет соответствующее сообщение, то бот открывает Гостевое меню.
6.	Если пользователь выбирает на клавиатуре «Вход» или отправляет соответствующее сообщение, то бот начинает процедуру авторизации.

**[ Сценарий 4 – Гостевое меню]**
1.	Если по итогу сц.3 пользователь был направлен в Гостевое меню, то бот присылает пользователю сообщение о доступных в данном меню функциях. Пользователь может узнать историю компании, получить информацию о привилегиях, доступных сотрудникам, получить контакты людей, отвечающих на вопросы в разделе обратная связь или осуществить вход.
2.	На экране появляется клавиатура с возможностью выбора варианта.
3.	Если пользователь выбирает на клавиатуре «Обратная связь» или отправляет соответствующее сообщение, то бот открывает соответствующий раздел.
4.	Если пользователь выбирает на клавиатуре «История»/«Привилегии» или отправляет соответствующее сообщение, то бот запускает соответствующую функцию.
5.	Если пользователь выбирает на клавиатуре «Вход» или отправляет соответствующее сообщение, то бот начинает процедуру авторизации.

**[ Сценарий 5 – Вход]**

1.	Бот запрашивает у пользователя логин*.
2.	На экране появляется кнопка «Отмена», при нажатии которой бот возвращает пользователя в меню, из которого запущен процесс авторизации.
3.	Пользователь вводит логин или завершает процесс, нажатием кнопки «Отмена».
4.	Если введённый логин не существует, то бот сообщает об ошибке.
5.	Если введённый логин существует, то бот запрашивает у пользователя пароль*.
6.	Пользователь вводит пароль или завершает процесс, нажатием кнопки «Отмена».
7.	Если введённый пароль не совпадает с паролем от данного логина, то бот сообщает об этом и просит ввести пароль ещё раз. Повторяется шаг 6. 
8.	У пользователя есть 4 попытки ввести пароль, по истечении которых бот сообщает пользователю, что тот превысил лимит попыток ввода пароля и просит повторить попытку через минуту. Пользователь возвращается в меню, из которого начал авторизацию. Если он попробует войти снова меньше, чем через минуту, то бот вновь сообщит об оштюке и попросит подождать.
9.	Если пароль введён верно, то бот приветствует пользователя и запускает Главное меню.

*Логин и Пароль необходимо заранее получить у администратора

**[ Сценарий 6 – Главное меню]**
1.	Бот присылает пользователю сообщение с возможностями главного меню. Пользователь может узнать историю компании, получить информацию о сервисах и привилегиях, доступных сотрудникам, получить контакты людей, отвечающих на вопросы в разделе обратная связь, изменить свои данные или выйти из системы в личном кабинете. Если пользователь обладает уровнем доступа выше 0, то ему доступен также раздел «Администрирование».
2.	На экране появляется клавиатура с возможностью выбора варианта.
3.	После выбора варианта пользователем бот запускает соответствующую функцию.

**[ Сценарий 7 – История компании]**

1.	После вызова соответствующей функции в Гостевом/Главном меню, бот присылает пользователю сообщение с историей компании.
2.	На экране появляется клавиатура с возможностью возвращения в меню
3.	Если пользователь выбирает «Меню», то бот возвращает его в меню, из которого была запущена функция.


**[ Сценарий 8 - Получение информации о сервисах]**

1.	Пользователь выбирает вариант для получения информации о сервисах, с которыми взаимодействует компания, в Главном меню.
2.	На экране появляется клавиатура с названиями сервисов, о которых можно узнать и возможностью вернуться в Главное меню. 
3.	Пользователь выбирает вариант. 
4.  Бот присылает сообщение с необходимой информацией.
5.  Бот предлагает пользователю узнать о сервисах больше или вернуться в Главное меню.
6.	Если пользователь выбирает «Меню» в п.2 или п.3, то бот возвращает его в Главное меню.
7.	Если пользователь хочет узнать больше, то повторяется п.2. 

**[ Сценарий 9 – Получение информации о привилегиях сотрудника]**

1.	Пользователь выбирает вариант с получением информации о привилегиях, доступных сотрудникам компании, в Гостевом/Главном меню.
2.	На экране появляется клавиатура с названиями привилегий, о которых можно узнать и возможностью вернуться в меню.
3.	Пользователь выбирает вариант.
4.  Если пользователь выбирает «Меню», то бот возвращает его в меню, из которого была запущена функция.
5.	Если пользователь выбирает одну из привилегий, то в зависимости от типа привилегии, бот запускает соответствующую процедуру.
6.  Если выбранная привилегия представляет из себя сообщение о чём-то одном, то бот присылает соответствующую информацию и спрашивает пользователя, хочет он узнать больше или вернуться в Меню.
7.  Если пользователь выбирает «Меню», то бот возвращает его в меню, из которого была запущена функция.
8.  Если пользователь хочет узнать больше, то повторяется п.2.
9.  Если выбранная привилегия представляет из себя набор из нескольких возможностей, то на экране появляется клавиатура с возможностью выбора варианта.
10.  Пользователь делает выбор. Бот присылает соответствующую информацию и спрашивает пользователя, хочет он узнать больше о данной привилегии, о других привилегиях или вернуться в Меню.
11.  Если пользователь выбирает «Меню», то бот возвращает его в меню, из которого была запущена функция.
12.  Если пользователь хочет узнать больше о выбранном типе привилегий, то повторяется п.9.
13.  Если пользователь хочет узнать о других привилегиях, то повторяется п.2.

**[ Сценарий 10 – предоставление возможности экспорта ответов пользователя в файл]**

1.  В процессе работы пользователь получает от бота сообщение о том, что для получения той или иной информации/привилегии требуется заполнение определённого заявления.
2.  Бот предлагает пользователю помощь в создании подобного документа. 
3.  На экране появляется кнопка, позволяющая перейти к данной функции.
4.  Если пользователь нажимает на кнопку, бот последовательно запрашивает у него информацию, необходимую для заполнения шаблона заявления в формате вопрос-ответ.
5.  Бот спрашивает, в каком формате пользователь хотел бы получить заявление: сообщение или файл. Пользователь отвечает.
6.  В зависимости от выбора пользователя, бот либо присылает пользователю заявление сообщением, либо присылает готовый файл.
7.  Если пользователь не хочет заполнять заявление, то он игнорирует кнопку и продолжает/завершает работу.

**[ Сценарий 11 - Навигация по офису]**

1.	Пользователь выбирает вариант «Навигация» в Главном меню.
2.	Бот присылает пользователю сообщение о том, что представляет из себя данная функция и как её использовать.
3.	На экране появляется клавиатура с возможностью запуска функции или возвращения в Главное меню.
4.  Если пользователь выбирает «Меню», то бот возвращает его в Главное меню.
5.	Если пользователь запускает процесс, то бот просит его ввести id искомого сотрудника в системе или его ФИО. На экране появляются кнопки «Отмена» и «Список пользователей».
6.  При нажатии кнопки «Отмена» пользователь возвращается к п.2.
7.  При нажатии кнопки «Список пользователей», бот предлагает пользователю получить список сотрудников и их id, чтобы тот мог узнать необходимую для введения информацию.
8.  Пользователь может получить список всех пользователей, настроить список, выбрав определённое управление, отдел и т.д. в формате диалога с ботом, нажимая кнопки, появляющиеся на экране, или вернуться к п.2, нажав «Отмена».
9.  Бот присылает список пользователей и возвращается к п.4.
10. Пользователь вводит данные (или выбирает список/отменяет процесс).
11.	Если введены некорректные данные, пользователь получает сообщение об ошибке.
12.	Если данные введены корректно, то бот присылает необходимую информацию и возвращается к п.2.

**[ Сценарий 12 – Личный кабинет]**
1.	При переходе в Личный кабинет из Главного меню, бот присылает пользователю сообщение с функциями, доступными в данном разделе. Пользователь может сменить Логин/Пароль/Личную информацию/Фото или выйти из учётной записи.
2.	На экране появляется клавиатура с возможностью выбора варианта или возвращения в меню.
3.	Если пользователь выбирает «Меню», то бот возвращает его Главное меню.
4.	Если пользователь выбирает «Выход», то бот осуществляет выход данного пользователя из учётной записи и возвращает его в Стартовое меню, для доступа к основным функциям вновь потребуется авторизация. Запускается сц.3.
5.	Если пользователь выбирает смену фото, то бот запрашивает у пользователя новое фото.
6.	На экране появляется кнопка «Отмена», позволяющая отменить процесс.
7.	При нажатии кнопки «Отмена» пользователь возвращается к п.2.
8.	Пользователь отменяет процесс или присылает фото.
9.	Бот заменяет полученным фото старое, в случае возникновения ошибки, бот предлагает повторить попытку. Пользователь может попытаться снова или вернуться к п.2., нажав кнопку «Отмена», расположенную на экране.
10.	 Если пользователь выбирает смену личной информации, то бот присылает пользователю сообщение с его старой личной информацией (если она введена) и просит ввести новую. Пользователь также получает сообщение с рекомендациями по содержанию данной информации. 
11.	 На экране появляется кнопка «Отмена», позволяющая отменить процесс.
12.	 При нажатии кнопки «Отмена» пользователь возвращается к п.2.
13.	 Пользователь отменяет действие нажатием кнопки «Отмена» или вводит информацию, после чего бот вносит соответствующие изменения в базу данных и возвращает пользователя к п.2. 
14.  Если пользователь выбирает смену логина или пароля, то бот запускает соответствующие процессы см. сц.13 – 14.

**[ Сценарий 13 – Смена логина]**
1.	Если пользователь выбирает смену логина, то бот просит пользователя ввести новый логин. 
2.	На экране появляется кнопка «Отмена», позволяющая отменить процесс.
3.	При нажатии кнопки «Отмена» пользователь возвращается к сц.12 п.2.
4.	Пользователь отменяет процесс или вводит новый логин.
5.	Если введённый пользователем логин уже занят, то бот сообщает об этом и предлагает попробовать ещё раз.
6.	На экране появляется клавиатура с возможностью выбора «Да» или «Нет».
7.	Если пользователь выбирает «Нет», то бот запускает сц.12 п.2.
8.	Если пользователь выбирает «Да», то запускается п.1.
9.	Если введённый логин никем не занят, то бот вносит изменения, сообщает об этом и запускает сц.12 п.2.

**[ Сценарий 14 – Смена пароля]**
1.	Если пользователь выбирает смену пароля, то бот просит пользователя ввести старый пароль. 
2.	На экране появляется кнопка «Отмена», позволяющая отменить процесс.
3.	При нажатии кнопки «Отмена» пользователь возвращается к сц.12 п.2.
4.	Пользователь вводит старый пароль или отменяет процесс.
5.	Если старый пароль введён неверно, то бот сообщает об ошибке и предлагает попробовать ещё раз.
6.	На экране появляется клавиатура с возможностью выбора «Да» или «Нет».
7.	Если пользователь выбирает «Нет», то бот запускает сц.12 п.2.
8.	Если пользователь выбирает «Да», то запускается п.1.
9.	Если старый пароль введён верно, то бот просит пользователя ввести новый пароль, также пользователь получает сообщение с критериями создания пароля (длина и т.п.).
10.	 Пользователь вводит новый пароль или отменяет процесс.
11.	 Если новый пароль не соответствует критериям, то бот сообщает об этом и предлагает ввести новый пароль ещё раз
12.	 Пользователь отменяет процесс кнопкой «Отмена» или вводит новый пароль.
13.  Если новый пароль введён корректно, то бот вносит соответствующие изменения, сообщает об успешном завершении процедуры и запускает сц.12 п.1.

**[ Сценарий 15 – Обратная связь]**

1.	Пользователь выбирает вариант, позволяющий получить контакты людей, отвечающих на вопросы в Стартовом/Гостевом/Главном меню.
2.	Бот присылает информацию.
3.  На экране появляется кнопка «Меню».
4.  При нажатии на кнопку «Меню», бот возвращает пользователя в меню, из которого запущена процедура.

**[ Сценарий 16 –Администрирование]**

1.	Если пользователь обладает уровнем доступа администратора и запускает раздел Администрирование в Главном меню, то бот присылает пользователю сообщение с инструкцией по использованию данного раздела. Администратор может Добавить пользователя, Удалить пользователя или сделать рассылку.
2.	На экране появляется клавиатура с возможностью выбора варианта. Также Администратор может вернуться в Главное меню или ещё раз получить сообщение с подсказкой.
3.	Если администратор выбирает «Меню», то бот возвращает его Главное меню.
4.	Если администратор выбирает раздел «Помощь», то бот присылает ему подсказку по использованию данного раздела и повторяет п.2.
5.  Если пользователь выбирает одну из функций (Добавление, Удаление, Рассылка), то бот запускает соответствующий процесс см. сц.17 – 19.


**[ Сценарий 17 – Добавление пользователя]**

1.	Если запущен процесс добавления пользователя, то бот запрашивает у администратора ФИО добавляемого пользователя.
2.	На экране появляется кнопка «Отмена», позволяющая отменить процесс.
3.  При нажатии кнопки «Отмена» пользователь возвращается к сц.16 п.2.
4.	Администратор вводит имя пользователя или отменяет процесс.
5.	Бот запрашивает у администратора логин и пароль для нового пользователя, а также сообщает ему критерии этих логина и пароля.
6.	На экран добавляется кнопка «Сгенерировать», при нажатии на которую логин и пароль для нового пользователя генерируются автоматически, а администратор переходит на следующий шаг.
7.	Администратор вводит логин и пароль/генерирует логин и пароль/отменяет процесс.
8.	Бот запрашивает у администратора фото для нового пользователя.
9.	На экран добавляется кнопка «Пропустить», при нажатии на которую фото для нового пользователя добавляется автоматически (ставится картинка «заглушка»), а администратор переходит на следующий шаг.
10.	 Администратор присылает фото/пропускает шаг/отменяет процесс.
11.	 Бот запрашивает у администратора уровень доступа нового сотрудника и сообщение с объяснением значения этих уровней.
12.	 На экран добавляются кнопки с возможностью выбора уровня доступа.
13.  Администратор вводит уровень доступа/отменяет процесс.
14.	 Если уровень доступа равен 3, то бот переходит к п. 17, заполнив остальное автоматически.
15.	 Если уровень доступа меньше 3, то бот запрашивает у Администратора поочерёдно управление и отдел добавляемого пользователя (в каждом случае на экран добавляются кнопки с возможностью выбора одного из существующих управлений/отделов).
16.	 Администратор выбирает управление/отдел из существующих или вводит новое(-ый) или отменяет процесс.
17.	 Бот запрашивает у администратора должность добавляемого сотрудника.
18.	 Администратор вводит должность или отменяет процесс.
19.	 Бот добавляет пользователя в базу данных, сообщает об успешном завершении процесса и присылает сообщение с информацией о новом пользователе. После этого запускается сц.16 п.2.

**[ Сценарий 18 –Удаление пользователя]**

1.	Если запущен процесс удаления пользователя, то бот запрашивает у администратора id в системе или ФИО удаляемого пользователя.
2.	На экране появляются кнопки «Отмена» и «Список пользователей».
3.	При нажатии кнопки «Отмена» пользователь возвращается к сц.16 п.2.
4.	При нажатии кнопки «Список пользователей», бот предлагает администратору получить список сотрудников доступных для удаления и их id, чтобы тот мог узнать необходимую для введения информацию.
5.	Администратор может получить список всех доступных пользователей, настроить список, выбрав определённое управление, отдел и т.д. (если ему позволяет уровень доступа) в формате диалога с ботом, нажимая кнопки, появляющиеся на экране, или вернуться к сц.16 п.2, нажав «Отмена».
6.	Бот присылает список пользователей доступных для удаления и возвращается к п.2.
7.	Администратор вводит id или ФИО пользователя, которого хочет удалить.
8.	Если данные введены не корректно, то бот сообщает об ошибке, предлагает попробовать ещё раз и запускает п.1.
9.	Если данные корректны, то бот удаляет пользователя, сообщает об успешном завершении процесса и запускает сц.16 п.2. 

**[ Сценарий 19 – Рассылка]**
1.	Если запущен процесс рассылки, то бот, в зависимости от уровня доступа администратора, предлагает ему выбрать адресатов (админ с уровнем доступа 3 может сделать рассылку куда угодно, с уровнем 2 только в своё управление, но в любой отдел, с уровнем 1, только в свой отдел).
2.	Соответственно, админ может в формате диалога с ботом выбрать управление(-я) и/или отдел(-ы), в которые хочет сделать рассылку (на каждом этапе вводятся данные в указанном формате) или отправить сообщение всем (в пределах уровня доступа).
3.	Бот запрашивает сообщение для рассылки.
4.	Администратор вводит сообщение.
5.	Бот осуществляет рассылку и сообщает о её успешном завершении, после чего запускается сц.16 п.2.
