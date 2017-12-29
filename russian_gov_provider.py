import random as rnd
import locale
import datetime
from faker.providers import BaseProvider
from num2text import num2text


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class RussianGovProvider(BaseProvider):
    def inn(self):
        res = ''
        for _ in range(12):
            res = res + str(rnd.randrange(1,10))
        return res

    def kpp(self):
        res = ''
        for _ in range(4):
            res = res + str(rnd.randrange(1,10))
        res = res + rnd.choice(['43','44','45'])
        res = res + self.numerify()
        return res

    def car_manufacturer(self):
        car_brands = [
                'AC',
                'Acura',
                'Alfa Romeo',
                'Alpine',
                'AM General',
                'Ariel',
                'Aro',
                'Asia',
                'Aston Martin',
                'Audi',
                'Austin',
                'Autobianchi',
                'Baltijas Dzips',
                'Beijing',
                'Bentley',
                'Bertone',
                'Bitter',
                'BMW',
                'BMW Alpina',
                'Brabus',
                'Brilliance',
                'Bristol',
                'Bufori',
                'Bugatti',
                'Buick',
                'BYD',
                'Byvin',
                'Cadillac',
                'Callaway',
                'Carbodies',
                'Caterham',
                'Changan',
                'ChangFeng',
                'Chery',
                'Chevrolet',
                'Chrysler',
                'Citroen',
                'Cizeta',
                'Coggiola',
                'Dacia',
                'Dadi',
                'Daewoo',
                'DAF',
                'Daihatsu',
                'Daimler',
                'Dallas',
                'Datsun',
                'De Tomaso',
                'DeLorean',
                'Derways',
                'Dodge',
                'DongFeng',
                'Doninvest',
                'Donkervoort',
                'E-Car',
                'Eagle',
                'Eagle Cars',
                'Ecomotors',
                'FAW',
                'Ferrari',
                'Fiat',
                'Fisker',
                'Ford',
                'Foton',
                'FSO',
                'Fuqi',
                'Geely',
                'Geo',
                'GMC',
                'Gonow',
                'Great Wall',
                'Hafei',
                'Haima',
                'Hindustan',
                'Holden',
                'Honda',
                'HuangHai',
                'Hummer',
                'Hyundai',
                'Infiniti',
                'Innocenti',
                'Invicta',
                'Iran Khodro',
                'Isdera',
                'Isuzu',
                'IVECO',
                'JAC',
                'Jaguar',
                'Jeep',
                'Jensen',
                'JMC',
                'Kia',
                'Koenigsegg',
                'KTM',
                'Lamborghini',
                'Lancia',
                'Land Rover',
                'Landwind',
                'Lexus',
                'Liebao Motor',
                'Lifan',
                'Lincoln',
                'Lotus',
                'LTI',
                'Luxgen',
                'Mahindra',
                'Marcos',
                'Marlin',
                'Marussia',
                'Maruti',
                'Maserati',
                'Maybach',
                'Mazda',
                'McLaren',
                'Mega',
                'Mercedes-Benz',
                'Mercury',
                'Metrocab',
                'MG',
                'Microcar',
                'Minelli',
                'Mini',
                'Mitsubishi',
                'Mitsuoka',
                'Morgan',
                'Morris',
                'Nissan',
                'Noble',
                'Oldsmobile',
                'Opel',
                'Osca',
                'Pagani',
                'Panoz',
                'Perodua',
                'Peugeot',
                'Piaggio',
                'Plymouth',
                'Pontiac',
                'Porsche',
                'Premier',
                'Proton',
                'PUCH',
                'Puma',
                'Qoros',
                'Qvale',
                'Reliant',
                'Renault',
                'Renault Samsung',
                'Rolls-Royce',
                'Ronart',
                'Rover',
                'Saab',
                'Saleen',
                'Santana',
                'Saturn',
                'Scion',
                'SEAT',
                'ShuangHuan',
                'Skoda',
                'Smart',
                'Soueast',
                'Spectre',
                'Spyker',
                'Ssang Yong',
                'Subaru',
                'Suzuki',
                'Talbot',
                'TATA',
                'Tatra',
                'Tazzari',
                'Tesla',
                'Tianma',
                'Tianye',
                'Tofas',
                'Toyota',
                'Trabant',
                'Tramontana',
                'Triumph',
                'TVR',
                'Vauxhall',
                'Vector',
                'Venturi',
                'Volkswagen',
                'Volvo',
                'Vortex',
                'Wartburg',
                'Westfield',
                'Wiesmann',
                'Xin Kai',
                'Zastava',
                'Zotye',
                'ZX',
                'Ё-мобиль',
                'Автокам',
                'Астро',
                'Бронто',
                'ВАЗ',
                'ГАЗ',
                'ЗАЗ',
                'ЗИЛ',
                'ИЖ',
                'КамАЗ',
                'Канонир',
                'ЛУАЗ',
                'Москвич',
                'СМЗ',
                'СеАЗ',
                'ТагАЗ',
                'УАЗ',
                'Ultima',
                'Hawtai',
                'Renaissance'
        ]
        return rnd.choice(car_brands)

    def education_level(self):
        return rnd.choice(['высшее','среднее','среднее специальное', 'неоконченное высшее'])

    def region_number(self):
        return str(rnd.randrange(1, 800)).zfill(3)

    def ogrn(self):
        return str(rnd.randrange(1,10)) + self.region_number() + str(rnd.randrange(1, 800)).zfill(3) +  str(rnd.randrange(1, 9999)).zfill(4) + str(rnd.randrange(1,10))

    def sex(self):
        return rnd.choice(['муж.','женск.','мужской','женский'])

    def procent(self):
        return str(rnd.randrange(0, 100))

    def money(self, in_str=False):
        rub = int(self.random_int())
        cop = int(self.numerify())
        if in_str == True:
            return num2text(rub) + ' рублей ' + num2text(cop) + ' копеек' 
        return rnd.choice([str(rub) + '.' + str(cop), num2text(rub) + ' рублей ' + num2text(cop) + ' копеек' ])

    def snils(self):
        return str(rnd.randrange(1,1000)).zfill(3) + '-' + str(rnd.randrange(1,1000)).zfill(3) + '-' + str(rnd.randrange(1,1000)).zfill(3) + ' ' + str(rnd.randrange(1,100)).zfill(2)

    def date(self, in_str=False):
        year = rnd.choice(range(1950, 2001))
        month = rnd.choice(range(1, 13))
        day = rnd.choice(range(1, 29))
        rnd_date = datetime.datetime(year, month, day)
        if in_str == True:
            return rnd_date.strftime('%d %B %Y')
        return rnd.choice([rnd_date.strftime('%d %B %Y'), rnd_date.strftime('%d %m %Y')])

    def count(self, in_str=False):
        if in_str == False:
            return str(rnd.randint(1, 1000))
        return num2text(rnd.randint(1, 1000))

    def citizenship(self):
        return rnd.choice(['рф','россия','украина','укр.', 'нет'])
    #def product_name():

