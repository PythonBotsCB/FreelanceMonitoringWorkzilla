import requests
import json
import fake_useragent

keys = ['презен', 'сайт', 'скрипт', 'найти', 'транскриб', 'телеграм', 'бот', 'приложение', 'power', 'excel',
        'python', 'pascal', 'база', 'данные', 'данных', 'собрать', 'базу', 'базы', 'рерайт', 'tg', 'тг']

# данные запросов

cookie = 'lang=ru; _gid=GA1.2.230034781.1688485589; _ym_uid=1688485589447144532; _ym_d=1688485589; _ym_isad=2; _ym_visorc=w; .AspNetCore.Session=CfDJ8JV3b1ASMLJEhHFrtD8l4rlsOH9P1XL7h%2Fktl4FAjEYsthLZeQIXD0CHQ82y2H0SMlCGkRAp4ZdKRtvc2v0SAY0Yl3UiB9%2By66Xr2F6kINuY6yCVimP2Ps7QDAWDdEMzLOPjnx3j5IXp9pqmPRMEA4RzENDr0l6L7dMhHiScD5tI; BrowserId=0882fa48-c912-4279-8e04-df0d5d2d54ca; __stripe_mid=af581cb6-d934-47de-ab86-96aca5239f4fa5ea8b; __stripe_sid=a2e1095e-6dc9-42f1-b9b3-17b0a5aea3b0a3f7b7; Bearer=CfDJ8JV3b1ASMLJEhHFrtD8l4rn1Ofvvz0K3JhAYLzdSI2WrBqTnhhuKpU_0VJr5mo4M4eglsIDqN5nutidhbiBW8J3McI8Ta7_JH1Oyq7CT6IluNHt-Vqu81h4n9U7UHSSGFVHtvSrH2CSpH47sxB3Ns5t9g08p-2HhT7GMuNOP5ppZyDBgaDj4JpSdCauxv4ZHCa8nJCFqo_XRZqpW5QC0-ESKFPimzo1M4RWP_3y4EeNji3UrrU3NCznO0hMe6XjEoEh11mhMb3fxsDn7MGvx4ze7Vkna0-q6rBzGAWh1P9ddvEPt84Jb0HYI2iKXaRJmNJEKOpqleuH8MZJ8liekgiLTjKGaDldBdkj1TsaN3Nw5HCY4xsPmcT68taeHnwNnWRqmun3a7mCgOfk3irX4lFU56cQ7DMNPyiIKVCPez-aId4HRjhibct6Ef7Swewj_ie6Nr0zFDZpGKhBAWRND_wsA0pxsA8lIa8QZCMjdrmUHKaMV7JGNv70zewd04ZBAtSQ6MQMAZHlH1cOA2bEhbWtahJEmJuCOIFBFLMcJNw0fdUyUSGkUmk0rbjc9iFXT6HCqvBP3e4Beb6EgdZ_4ucSMWAZSFNXes_h_CJM3WpyArRBSafMPI8m6yARIJkGB-MEQdc0CSV9zmAxTU8i2sAsLFk5IYUJso2N-QKRAbcg7ktoTGoiIKvOpxe5ib8kpKUddV-l6ksKSE6v-iZna2Ho; _ga_NHGQ9RK9FC=GS1.1.1688494576.2.1.1688495626.60.0.0; _ga=GA1.2.100167203.1688485589; _gat_UA-12171510-1=1'
user = fake_useragent.UserAgent().random

url = 'https://client.work-zilla.com/api/order/v4/list/open?hideInsolvoOrders=false'

headers = {
    'cookie': cookie,
    'user-agent': user,
    'agentid': 'fp21-5a94f2a37add5535f398a27720b9a547'
}

def check_intresting():
    ''' сборка данных с сайта и проверка на ключи '''

    request = requests.get(url, headers=headers)
    data = request.json()
    total = 0


    with open('intresting.json', encoding='utf-8') as file:
        data_json = json.load(file)
        result = []
        for i in data_json:
            result.append(i)
        total = len(result)

    tasks = data.get('data').get('intrestring') + data.get('data').get('other') if data.get('data').get('intrestring') is not None else data.get('data').get('other')

    for task in tasks:
        name = task.get('description')
        price = task.get('price')
        freelancerEarn = task.get('freelancerEarn')
        for key in keys:
            if key in name.lower() and 'авито' not in name.lower():
                tasker = {
                        'name' : name,
                        'price' : price,
                        'freelancerEarn' : freelancerEarn
                    }
                if tasker not in result:
                    result.append(tasker)
                break
            if 'написать' in result and int(price) > 300:
                tasker = {
                    'name': name,
                    'price': price,
                    'freelancerEarn': freelancerEarn
                }
                if tasker not in result:
                    result.append(tasker)
                break

    with open('intresting.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    if len(result) - total > 0:
        return True

    return False

def check_tasks():
    ''' создаст файл с интересующими заданиями для дальнейшей выгрузки в телеграм '''

    request = requests.get(url, headers=headers)
    data = request.json()
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    ''' сначала записываются данные, затем в боте считываются и отправляются сообщениями в личку '''