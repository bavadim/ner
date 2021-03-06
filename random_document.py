#!/usr/bin/env python3

import os
import random
from faker import Faker
import glob
import uuid
from nltk.tokenize import word_tokenize
import re
from jinja2 import Template, Environment, FileSystemLoader
from russian_gov_provider import RussianGovProvider


fake = Faker('ru_RU')
fake.add_provider(RussianGovProvider)

def tokenize(s):
    return re.findall(r"[\w]+|[‑–—“”€№…’\"#$%&\'()+,-./:;<>?]", s)

def fill_template():
    variables = {
            '%': (fake.procent(), 'O'),
            '№ ': (fake.isbn13(), 'DOC-NUMBER'),
            '№': (fake.isbn13(), 'DOC-NUMBER'),
            'E-mail': (fake.email(), 'EMAIL'),
            'ID инвестиционного проекта': (fake.isbn13(), 'O'),
            'Адрес': (fake.address(), 'ADDRESS'),
            'Адрес места жительства заявителя': (fake.address(), 'ADDRESS'),
            'Адрес Общества': (fake.address(), 'ADDRESS'),
            'Адрес получателя письма': (fake.address(), 'ADDRESS'),
            'Адрес получателя претензии': (fake.address(), 'ADDRESS'),
            'Адрес судебного органа': (fake.address(), 'ADDRESS'),
            'Артикул': (fake.ean(), 'O'),
            'Банк': (fake.company(), 'COMPANY-NAME'),
            'БИК': (fake.iban() , 'BIK'),
            #'Биометрические персональные данные': (fake.text(), 'O'),
            #'Блок реквизитов': (fake.text(), 'O'),
            'Брутто': (fake.random_int(), 'MASS'),
            'Величина постынвестиционной оценки проекта': (fake.money(), 'MONEY'),
            #'Вероятность наступления угрозы': (fake.text(), 'O'),
            'Всего наименований': (fake.random_number(), 'COUNT'),
            'ГГ': (fake.year(), 'YEAR'),
            'Год ': (fake.year(), 'YEAR'),
            'Год': (fake.year(), 'YEAR'),
            'Год изготовления ТС': (fake.year(), 'YEAR'),
            'Год прохождения курсов': (fake.year(), 'YEAR'),
            'Гражданство': (fake.citizenship(), 'CITIZENSHIP'),
            'Гражданство или лицо без гражданства': (fake.citizenship(), 'CITIZENSHIP'),
            'Дата ': (fake.date(), 'DATE'),
            'Дата': (fake.date(), 'DATE'),
            'Дата выдачи':  (fake.date(), 'DATE'),
            'Дата документа': (fake.date(), 'DATE'),
            'Дата заключения': (fake.date(), 'DATE'),
            'Дата заключения договора': (fake.date(), 'DATE'),
            'Дата или событие': (fake.date(), 'DATE'),
            'Дата исполнения': (fake.date(), 'DATE'),
            'Дата окончания выплат': (fake.date(), 'DATE'),
            'Дата определения': (fake.date(), 'DATE'),
            'Дата ответа': (fake.date(), 'DATE'),
            'Дата подписания': (fake.date(), 'DATE'),
            'Дата предоплаты': (fake.date(), 'DATE'),
            'Дата претензии': (fake.date(), 'DATE'),
            'Дата расчета долга': (fake.date(), 'DATE'),
            'Дата регистрации': (fake.date(), 'DATE'),
            'Дата рождения': (fake.date(), 'DATE'),
            'Дата свидетельства': (fake.date(), 'DATE'),
            'Дата смены': (fake.date(), 'DATE'),
            'Дата совершения доверенности прописью': (fake.date(), 'DATE'),
            'Дата составления': (fake.date(), 'DATE'),
            'ДД': (fake.date(), 'DATE'),
            '№ Доверенности': (fake.random_number(), 'DOC-NUMBER'),
            '№ Договора': (fake.random_number(), 'DOC-NUMBER'),
            #'Должность ': (fake.text(), 'POSITION'), #TODO !!!!
            #'Должность': (fake.text(), 'POSITION'), #TODO !!!!
            #'Должность руководителя': (fake.text(), 'POSITION'), #TODO !!!!
            #'Должность уполномоченного лица': (fake.text(), 'POSITION'), #TODO !!!!
            'Дом': (fake.building_number(), 'BUILDING-NUMBER'),
            'Ед.': (fake.random_int(), 'COUNT'),
            'Идентификационный номер': (fake.numerify(), 'O'),
            'Имя': (fake.name(), 'NAME'),
            'Индекс': (fake.postcode(), 'POSTCODE'),
            'ИНН': (fake.inn(), 'INN'),
            'ИНН должника': (fake.inn(), 'INN'),
            'ИНН заявителя': (fake.inn(), 'INN'),
            'ИНН уполномоченного органа': (fake.inn(), 'INN'),
            #'Иное': (fake.text(), 'OTHER'),
            #'Иное (например, выполнение / действительность каких-либо из Предварительных Условий Финансирования)': (fake.text(), 'OTHER'),
            #'Информация о поощрениях, наградах или взысканиях': (fake.text(), 'O'),
            #'Иные доказательства': (fake.text(), 'O'),
            #'Иные нормативные акты': (fake.text(), 'O'),
            #'Иные обязанности': (fake.text(), 'O'),
            #'Иные работники': (fake.text() , 'O'),
            #'Иные расходы': (fake.text(), 'O'),
            #'Иные требования': (fake.text(), 'O'),
            #'Источник угроз ИСПдн': (fake.text(), 'O'),
            #'Исходные данные при разработке Модели угроз': (fake.text(), 'O'),
            'Итого': (fake.random_int(), 'COUNT'),
            #'Категория ТС': (fake.text(), 'O'),
            'Квартира': (fake.random_int(), 'FLAT-NUMBER'),
            #'Кворум': (fake.text(), 'O'),
            #'Кем выдан': (fake.text(), 'O'),
            'Код': (fake.random_int(), 'O'),
            'Код подразделения': (fake.random_int(), 'O'),
            'Количество': (fake.random_int(), 'COUNT'),
            'Количество акций': (fake.random_int(), 'COUNT'),
            'Количество акций прописью': (fake.count(True), 'COUNT'),
            'Количество голосов': (fake.random_int(), 'COUNT'),
            'Количество дней': (fake.random_int(), 'COUNT'),
            'Количество дней прописью': (fake.random_int(), 'COUNT'),
            'Количество единиц продукции': (fake.random_int(), 'COUNT'),
            'Количество листов': (fake.random_int(), 'COUNT'),
            'Количество мест': (fake.random_int(), 'COUNT'),
            'Количество мест прописью': (fake.count(True), 'COUNT'),
            'Количество номеров': (fake.random_int(), 'COUNT'),
            'Количество прописью': (fake.random_int(), 'COUNT'),
            'Количество экземпляров': (fake.random_int(), 'COUNT'),
            'Корпус': (fake.random_int(), 'O'),
            'Корреспондентский счет': (fake.iban(), 'ACCOUNT-NUMBER'),
            'КПП': (fake.kpp(), 'KPP'),
            #'Кузов (кабина, прицеп)': (fake.text(), 'O'),
            'Листов': (fake.random_int(), 'COUNT'),
            #'Личные качества работника': (fake.text(), 'O'),
            'Марка транспортного средства': (fake.car_manufacturer(), 'CAR-MANUFACTURER'),
            'Масса брутто': (fake.random_int(), 'MASS'),
            'Масса нетто': (fake.random_int(), 'MASS'),
            'Место возврата': (fake.address(), 'ADDRESS'),
            'Место жительства': (fake.address(), 'ADDRESS'),
            'Место заключения': (fake.address(), 'ADDRESS'),
            'Местонахождение': (fake.address(), 'ADDRESS'),
            'Место нахождения':  (fake.address(), 'ADDRESS'),
            'Место передачи': (fake.address(), 'ADDRESS'),
            'Место регистрации': (fake.address(), 'ADDRESS'),
            'Место рождения': (fake.address(), 'ADDRESS'),
            'Место смены': (fake.address(), 'ADDRESS'),
            'Место совершения доверенности прописью': (fake.address(), 'ADDRESS'),
            'Место составления': (fake.address(), 'ADDRESS'),
            'Месяц': (fake.month_name(), 'MONTH'),
            'ММ': (fake.month_name(), 'MONTH'),
            'Модель, № двигателя': (fake.random_number(), 'O'),
            #'Назначение аванса': (fake.text(), 'O'),
            'Наименование ': (fake.company(), 'COMPANY-NAME'),
            'Наименование': (fake.company(), 'COMPANY-NAME'),
            #'Наименование арбитражного суда': (fake.text(), 'O'),
            #'Наименование арбитражного управялющего': (fake.text(), 'O'),
            'Наименование Доверителя': (fake.company(), 'COMPANY-NAME'),
            #'Наименование договора': (fake.text(), 'O'),
            #'Наименование документа': (fake.text(), 'O'),
            #'Наименование документов': (fake.text(), 'O'),
            'Наименование должника':  (fake.company(), 'COMPANY-NAME'),
            'Наименование Должника': (fake.company(), 'COMPANY-NAME'),
            #'Наименование должности': (fake.text(), 'O'),
            'Наименование заявителя':  (fake.company(), 'COMPANY-NAME'),
            'Наименование заявителя претензии': (fake.company(), 'COMPANY-NAME'),
            #'Наименование информационной системы персональных данных': (fake.text(), 'O'),
            'Наименование и реквизиты': (fake.company(), 'COMPANY-NAME'),
            #'Наименование и реквизиты документа': (fake.text(), 'O'),
            'Наименование конкурсного кредитора': (fake.company(), 'COMPANY-NAME'),
            'Наименование контрагента': (fake.company(), 'COMPANY-NAME'),
            'Наименование контрагента 1': (fake.company(), 'COMPANY-NAME'),
            'Наименование места требования': (fake.address(), 'O'),
            'Наименование населенного пункта': (fake.address(), 'O'),
            'Наименование образовательного учреждения': (fake.company(), 'COMPANY-NAME'),
            'Наименование ООО': (fake.company(), 'COMPANY-NAME'),
            'Наименование оператора': (fake.company(), 'COMPANY-NAME'),
            #'Наименование органа': (fake.text(), 'O'),
            #'Наименование органа, выдавшего свидетельство': (fake.text(), 'O'),
            #'Наименование органа, осуществившего регистрацию': (fake.text(), 'O'),
            'Наименование организации':  (fake.company(), 'COMPANY-NAME'),
            'Наименование организации, выдавшей ПТС': (fake.company(), 'COMPANY-NAME'),
            'Наименование организации (т.п.)': (fake.company(), 'COMPANY-NAME'),
            'Наименование организации/учреждения': (fake.company(), 'COMPANY-NAME'),
            'Наименование получателя': (fake.company(), 'COMPANY-NAME'),
            'Наименование получателя претензии': (fake.company(), 'COMPANY-NAME'),
            #'Наименование продукции': (fake.text(), 'O'),
            'Наименование работодателя': (fake.company(), 'COMPANY-NAME'),
            #'Наименование регистрирующего органа': (fake.text(), 'O'),
            #'Наименование результата интеллектуальной деятельности': (fake.text(), 'O'),
            #'Наименование, реквизиты документов': (fake.text(), 'O'),
            'Наименование саморегулируемой организации': (fake.company(), 'COMPANY-NAME'),
            'Наименование Стороны': (fake.company(), 'COMPANY-NAME'),
            'Наименование стороны договора': (fake.company(), 'COMPANY-NAME'),
            #'Наименование суда': (fake.text(), 'O'),
            #'Наименование ТС': (fake.text(), 'O'),
            #'Наименование уполномоченного органа': (fake.text(), 'O'),
            'Наименование участника Общества': (fake.company(), 'COMPANY-NAME'),
            #'Наименование финансовой санкции': (fake.text(), 'O'),
            'Наименование (ФИО) участника': (fake.name(), 'O'),
            'Наименование/ФИО учредителя': (fake.name(), 'O'),
            'Наименование фонда': (fake.company(), 'COMPANY-NAME'),
            '№ накладной': (fake.random_number(), 'DOC-NUMBER'),
            #'Нарушенные права': (fake.text(), 'O'),
            'Населенный пункт': (fake.city(), 'CITY'),
            #'Неисполненное обязательство': (fake.text(), 'O'),
            'Нетто': (fake.random_int(), 'MASS'),
            'Номер': (fake.random_number(), 'O'),
            'Номер договора': (fake.random_number(), 'DOC-NUMBER'),
            'Номер документа': (fake.random_number(), 'DOC-NUMBER'),
            'Номер ответа на претензию': (fake.random_number(), 'DOC-NUMBER'),
            'Номер письма': (fake.random_number(), 'DOC-NUMBER'),
            'Номер претензии':  (fake.random_number(), 'DOC-NUMBER'),
            'Номер приложения': (fake.random_number(), 'DOC-NUMBER'),
            'Номер свидетельства': (fake.random_number(), 'DOC-NUMBER'),
            'Номер соглашения': (fake.random_number(), 'DOC-NUMBER'),
            'Номер счета': (fake.iban(), 'ACCOUNT-NUMBER'),
            'Номер телефона': (fake.phone_number(), 'PHONE'),
            'Номер телефона должника': (fake.phone_number(), 'PHONE'),
            'Номер чека': (fake.random_number(), 'O'),
            'Номинальная стоимость': (fake.money(), 'MONEY'),
            'Номинальная стоимость акции': (fake.money(), 'MONEY'),
            'Номинальная стоимость доли ': (fake.money(), 'MONEY'),
            'Номинальная стоимость доли': (fake.money(), 'MONEY'),
            #'Обжалуемые действия (бездействие)': (fake.text(), 'O'),
            'Образование': (fake.education_level(), 'EDUCATION-LEVEL'),
            'Общая масса': (fake.random_int(), 'MASS'),
            #'Общая характеристика источника угроз ИСПДн': (fake.text(), 'O'),
            #'Обязанности заявителя по договору': (fake.text(), 'O'),
            #'Обязанности по договору': (fake.text(), 'O'),
            #'Обязательство': (fake.text(), 'O'),
            'ОГРН': (fake.ogrn(), 'OGRN'),
            'ОГРН Долждника': (fake.ogrn(), 'OGRN'),
            'ОГРН должника': (fake.ogrn(), 'OGRN'),
            'ОГРН заявителя': (fake.ogrn(), 'OGRN'),
            'ОГРНИП': (fake.ogrn(), 'OGRN'),
            'ОГРНИП заявителя': (fake.ogrn(), 'OGRN'),
            'ОГРН уполномоченного органа': (fake.ogrn(), 'OGRN'),
            'ОКПО': (fake.ogrn(), 'OKPO'),
            #'Описание курса': (fake.text(), 'O'),
            #'Описание новации долга': (fake.text(), 'O'),
            #'Описание обязательств': (fake.text(), 'O'),
            #'Описание угрозы ИСПДн': (fake.text(), 'O'),
            '№ определения': (fake.random_number(), 'DOC-NUMBER'),
            #'Основание задолженности': (fake.text(), 'O'),
            #'Основание полномочий подписанта': (fake.text(), 'O'),
            #'Основание полномочий представителя': (fake.text(), 'O'),
            #'Основные группы уязвимости ИСПДн': (fake.text(), 'O'),
            'Остаток': (fake.random_number(), 'O'),
            'Отчество': (fake.middle_name(), 'MIDDLE-NAME'),
            #'Паспортные данные': (fake.text(), 'O'),
            'Перерасход': (fake.random_number, 'O'),
            #'Перечень обязанностей, выполняемых Работником': (fake.text(), 'O'),
            'Перечень полномочий': (fake.text(), 'O'),
            #'Период': (fake.text(), 'O'), #TODO
            #'Период времени': (fake.text(), 'O'), # TODO
            #'Период оплаты': (fake.text(), 'O'), # TODO
            #'Подтверждающие документы': (fake.text(), 'O'),
            #'Подтверждающий документ': (fake.text(), 'O'),
            #'Подход к моделированию угроз безопасности': (fake.text(), 'O'),
            #'Пожалуйста, укажите другую необходимую информацию о проекте': (fake.text(), 'O'),
            'Пол': (fake.sex(), 'SEX'),
            #'Поле ввода': (fake.text(), 'O'),
            'Полное наименование': (fake.company(), 'COMPANY-NAME'),
            'Полное наименование учредителя': (fake.company(), 'COMPANY-NAME'),
            #'Порядок': (fake.text(), 'O'),
            #'Порядок начисления финансовой санкции': (fake.text(), 'O'),
            #'Порядок оплаты, срок ': (fake.text(), 'O'),
            #'Порядок расчета материального ущерба': (fake.text(), 'O'),
            #'Порядок расчета упущенной выгоды': (fake.text(), 'O'),
            #'Порядок удовлетворения требований': (fake.text(), 'O'),
            'Почтовый адрес': (fake.address(), 'ADDRESS'),
            #'Предмет доверенности': (fake.text(), 'O'),
            '№ Приложения': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Акт об исполнении обязательств': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Акт приема-передачи': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Акт приема-передачи материалов': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Акт приема-передачи транспортного средства': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Возмещение имущественных потерь': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Документы, подтверждающие право': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Заверения сторон': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Ключевые показатели эффективности': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Лист с подписями сторон': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Опционный договор': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Основные активы Общества': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Перечень транспортных средств': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Предварительные условия финансирования': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Прейскурант': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Раскрытие информации': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Смета': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Спецификация': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Спецификация объекта договора': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Спецификация тары': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Творческое задание': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Техническое задание': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Форма договора залога доли': (fake.random_number(), 'DOC-NUMBER'),
            '№ Приложения - Форма устава Общества': (fake.random_number(), 'DOC-NUMBER'),
            #'Принятое решение': (fake.text(), 'O'),
            #'Причины уязвимости ИСПДн': (fake.text(), 'O'),
            #'Производства по делу с указанием номера дела и суда': (fake.text(), 'O'),
            'пункт': (fake.random_number(), 'O'),
            '№ Пункт': (fake.random_number(), 'O'),
            '№ пункта ': (fake.random_number(), 'O'),
            'Пункт договора': (fake.random_number(), 'O'),
            'Размер': (fake.money(), 'MONEY'),
            'Размер балансовой стоимости имущества': (fake.money(), 'MONEY'),
            'Размер вознаграждения': (fake.money(), 'MONEY'),
            'Размер вознаграждения автора': (fake.money(), 'MONEY'),
            'Размер выкупной цены': (fake.money(), 'MONEY'),
            'Размер госпошлины': (fake.money(), 'MONEY'),
            'Размер доли': (fake.procent(), 'O'),
            'Размер доли после вклада Инвестора': (fake.procent(), 'O'),
            'Размер доли участника': (fake.procent(), 'O'),
            'Размер доли фонда ': (fake.procent(), 'O'),
            'Размер задолженности': (fake.money(), 'MONEY'),
            'Размер иных расходов': (fake.money(), 'MONEY'),
            'Размер компенсации за фактическую потерю времени': (fake.money(), 'MONEY'),
            'Размер материального ущерба': (fake.money(), 'MONEY'),
            'Размер неустойки': (fake.money(), 'MONEY'),
            'Размер платы': (fake.money(), 'MONEY'),
            'Размер почтовых расходов': (fake.money(), 'MONEY'),
            'Размер прописью': (fake.money(True)),
            'Размер процентов': (fake.money(), 'O'),
            'Размер расходов ': (fake.money(), 'MONEY'),
            'Размер расходов': (fake.money(), 'MONEY'),
            'Размер суммы долга': (fake.money(), 'MONEY'),
            'Размер упущенной выгоды': (fake.money(), 'MONEY'),
            'Размер уставного капитала': (fake.money(), 'MONEY'),
            'Размер уставного капитала прописью': (fake.money(), 'MONEY'),
            'Размер финансовой санкции': (fake.money(), 'MONEY'),
            'Размер штрафа': (fake.money(), 'MONEY'),
            'Размер штрафа при повреждении тары': (fake.money(), 'MONEY'),
            #'Район': (fake.city(), 'O'), #TODO
            'Расходы': (fake.money(), 'MONEY'),
            'Расчетный счет': (fake.iban(), 'ACCOUNT-NUMBER'),
            'Расчет суммы долга': (fake.money(), 'O'),
            'Расчет упущенной выгоды': (fake.money(), 'O'),
            'Расчет ущерба': (fake.money(), 'O'),
            'Расчет финансовой санкции': (fake.money(), 'O'),
            #'Регион': (fake.city(), 'O'), #TODO
            #'Реквизиты документа': (fake.text(), 'O'),
            '№ решения': (fake.random_number(), 'DOC-NUMBER'),
            #'Серия': (fake.random_number(), 'O'), #TODO
            'Серия/Номер': (fake.random_number, 'O'),
            'СНИЛС': (fake.snils(), 'SNILS'),
            #'Сокращенное наименование': (fake.text(), 'O'),
            #'Специальность': (fake.text(), 'O'),
            #'Способ передачи': (fake.text(), 'O'),
            #'Средства защиты информации': (fake.text(), 'O'),
            'Срок': (fake.date(), 'DATE'),
            'Срок действия': (fake.date(), 'DATE'),
            'Срок доверенности прописью': (fake.date(), 'DATE'),
            #'Срок отсрочки': (fake.text(), 'O'), #TODO
            #'Срок передачи': (fake.text(), 'O'),
            #'Срок полномочий': (fake.text(), 'O'),
            #'Срок полномочий прописью': (fake.text(), 'O'),
            #'Срок полномочий совета директоров': (fake.text(), 'O'),
            #'Срок предоплаты': (fake.text(), 'O'),
            #'Срок предоставления': (fake.text(), 'O'),
            #'Срок прописью': (fake.text(), 'O'),
            #'Срок рассмотрения': (fake.text(), 'O'),
            #'Срок рассрочки': (fake.text(), 'O'),
            #'Срок удовлетворения требований': (fake.text(), 'O'),
            'Стоимость услуг переводчика': (fake.money(), 'MONEY'),
            'Стоимость услуг представителя': (fake.money(), 'MONEY'),
            'Стоимость услуг специалиста': (fake.money(), 'MONEY'),
            'Стоимость услуг эксперта': (fake.money(), 'MONEY'),
            #'Стоимость цифрами': (fake.money(), 'MONEY'), #TODO
            'Страна регистрации': (fake.country(), 'COUNTRY'),
            'Строение': (fake.building_number(), 'BUILDING-NUMBER'),
            #'Структурное подразделение': (fake.text(), 'O'),
            'Сумма': (fake.money(), 'MONEY'),
            'Сумма в валюте': (fake.money(), 'MONEY'),
            'Сумма вознаграждения': (fake.money(), 'MONEY'),
            'Сумма вознаграждения прописью': (fake.money(True), 'MONEY'),
            'Сумма в рублях': (fake.money(), 'MONEY'),
            'Сумма договора': (fake.money(), 'MONEY'),
            'Сумма задолженности': (fake.money(), 'MONEY'),
            'Сумма задолженности по данным требованиям': (fake.money(), 'MONEY'),
            'Сумма налогов': (fake.money(), 'MONEY'),
            'Сумма отчета': (fake.money(), 'MONEY'),
            'Сумма предоплаты': (fake.money(), 'MONEY'),
            'Сумма претензии': (fake.money(), 'MONEY'),
            'Сумма прописью': (fake.money(), 'MONEY'),
            'Сумма расчета': (fake.money(), 'MONEY'),
            'сумма, руб': (fake.money(), 'MONEY'),
            'Сумма страхования': (fake.money(), 'MONEY'),
            'Сумма цифрами': (fake.money(), 'MONEY'),
            'Сумма штрафа': (fake.money(), 'MONEY'),
            #'Суть инвестиционного проекта': (fake.text(), 'O'),
            #'Существо требования': (fake.text(), 'O'),
            'счет, субсчет': (fake.iban(), 'ACCOUNT-NUMBER'),
            'Тек. остаток': (fake.money(), 'O'),
            'Телефон': (fake.phone_number(), 'PHONE'),
            'Телефон Должника': (fake.phone_number(), 'PHONE'),
            #'Тип акций': (fake.text(), 'O'),
            #'Тип должности': (fake.text(), 'O'),
            'Типовая формула ликвидационной привилегии': (fake.text(), 'O'),
            #'Угроза ИСПДн': (fake.text(), 'O'),
            'Укажите адрес': (fake.address(), 'ADDRESS'),
            'Укажите адрес элекронной почты': (fake.email(), 'EMAIL'),
            'Укажите адрес электнной почты': (fake.email(), 'EMAIL'),
            'Укажите адрес электронной почты': (fake.email(), 'EMAIL'),
            'Укажите контактное лицо': (fake.name(), 'NAME'),
            #'Укажите механизмы разрешения Тупиковых ситуаций': (fake.text(), 'O'),
            'Укажите представителей Сторон': (fake.name(), 'NAME'),
            'Указать дату': (fake.date(), 'DATE'),
            'Указать дату регистрации': (fake.date(), 'DATE'),
            'Указать номер': (fake.random_number(), 'O'),
            'Указать серию': (fake.random_number(), 'O'),
            'Улица': (fake.street_name(), 'STREET'),
            'Утверждающий орган': (fake.company(), 'O'),
            'Факс': (fake.phone_number, 'O'),
            'Факс должника':  (fake.phone_number(), 'O'),
            'Факс Должника': (fake.phone_number(), 'O'),
            'Фамилия': (fake.last_name(), 'LAST-NAME'),
            #'Фамилия и инициалы': (fake.last_name(), 'LAST-NAME'), #TODO !!!!!!
            'Фамилия и инициалы исполнителя': (fake.last_name(), 'LAST-NAME'),
            'Фамилия и инициалы подписанта': (fake.last_name(), 'LAST-NAME'),
            'Фамилия и инициалы члена комиссии': (fake.last_name(), 'LAST-NAME'),
            'Фамилия, имя, отчество': (fake.name(), 'NAME'),
            'Фамилия Имя Отчество':  (fake.name(), 'NAME'),
            'Фамилия, имя, отчество работника': (fake.name(), 'NAME'),
            #'Фамилия, инициалы': (fake.last_name(), 'LAST-NAME'), #TODO
            'Фамилия, инициалы руководителя': (fake.last_name(), 'NAME'),
            'Филиал и представительство': (fake.company(), 'COMPANY'),
            'ФИО': (fake.name(), 'NAME'),
            'ФИО арбитражного управляющего': (fake.name(), 'NAME'),
            'ФИО Бухгалтера': (fake.name(), 'NAME'),
            'ФИО временного управляющего': (fake.name(), 'NAME'),
            'ФИО Главного бухгалтера': (fake.name(), 'NAME'),
            'ФИО Доверителя': (fake.name(), 'NAME'),
            'ФИО доверителя (и.п.)': (fake.name(), 'NAME'),
            'ФИО единственного участника': (fake.name(), 'NAME'),
            'ФИО заявителя': (fake.name(), 'NAME'),
            'ФИО конкурсного кредитора': (fake.name(), 'NAME'),
            'ФИО подписанта': (fake.name(), 'NAME'),
            'Ф.И.О представителя': (fake.name(), 'NAME'),
            'ФИО Представителя': (fake.name(), 'NAME'),
            'ФИО работника': (fake.name(), 'NAME'),
            'Ф.И.О. руководителя': (fake.name(), 'NAME'),
            'ФИО руководителя': (fake.name(), 'NAME'),
            'Ф.И.О уполномоченного лица': (fake.name(), 'NAME'),
            'ФИО уполномоченного лица': (fake.name(), 'NAME'),
            'Ф.И.О. участника': (fake.name(), 'NAME'),
            'Ф.И.О. учредителя': (fake.name(), 'NAME'),
            #'Форма реального ущерба': (fake.text(), 'O'),
            #'Формула ликвидационной привилегии': (fake.text(), 'O'),
            #'Формула расчета финансовой санкции': (fake.text(), 'O'),
            #'Формулировка': (fake.text(), 'O'),
            #'Характеристика уязвимостей ИСПДн': (fake.text(), 'O'),
            'Цвет кузова (кабины, прицепа)': (fake.color_name(), 'COLOR'),
            #'Цель использования': (fake.text(), 'O'),
            'Цена (на единицу продукции)': (fake.money(), 'MONEY'),
            #'Шасси (рама)': (fake.text(), 'O'),
            'Электронный адрес': (fake.email(), 'EMAIL'),
            'Электронный адрес должника': (fake.email(), 'EMAIL'),
            'Юридический адрес': (fake.address(), 'ADDRESS'),
            'Юридический адрес Должника': (fake.address(), 'ADDRESS'),
            'Юридический адрес кредитора': (fake.address(), 'ADDRESS'),
            'Юридический адрес саморегулируемой организации': (fake.address(), 'ADDRESS'),
    }

    qstn_tmp = {}
    tmp_sbst = {}
    for k,v in variables.items():
        sbst = str(uuid.uuid1()).replace('-', '')
        qstn_tmp[k] = sbst
        tmp_sbst[sbst] = v

    template = random.choice([filename for filename in glob.iglob(os.path.dirname(os.path.abspath(__file__)) + '/filt_templates/**/_*', recursive=True)])
    j2_env = Environment(loader=FileSystemLoader('/'), trim_blocks=True)
    doc = tokenize(j2_env.get_template(template).render(variables=qstn_tmp))
    res = []
    for w in doc:
        if w in tmp_sbst:
            sw, t = tmp_sbst[w]
            sw = tokenize(str(sw))
            if t == 'O':
                for ow in sw:
                    res.append(ow + ' O')
            else:
                res.append(sw.pop(0) + ' B-' + t)
                for ow in sw:
                    res.append(ow + ' I-' + t)
        else:
            res.append(w + ' O')

    return '\n'.join(res)


print(fill_template())
