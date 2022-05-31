import vk_api

import matplotlib.pyplot as plt
import Database


def getGroupsId(keyWord):
    groupsId = []
    groups = session.method("groups.search", {"q": keyWord, "count": numberOfRequest})
    for group in groups["items"]:
        print(group)
        Database.insert_group(con, group["id"], group["name"])
        groupsId.append(group["id"])
    return groupsId



def getMembers(groupsId):
    progress = 0
    year = ""
    membersStr = ""
    try:
        for groupId in groupsId:
            progress += 1
            print("Обработано: ", progress, "Группа(ы)")
            #try:
            # Получаем id подписчиков
            members = session.method("groups.getMembers", {"group_id": groupId})["items"]
            # все id подписчиков помещаем в строку
            for memStr in members:
                membersStr += str(memStr) + ","
            # получаем информацию о подписчиков пачкой
            memberInfo = session.method("users.get", {"user_ids": membersStr, "fields": 'bdate'})
            membersStr = ""
            # проходимся по каждому пользоваетелю отдельно
            for i in range(0, len(memberInfo)):
                if Database.checkRepeats(con, memberInfo[i]["id"], groupId):
                    print(memberInfo[i])
                    # проверяем наличие поля с днем рождения и наличия года в нем
                    if 'bdate' in memberInfo[i] and len(memberInfo[i]["bdate"]) > 7:
                        # Преобразовываем год в число
                        for j in range(len(memberInfo[i]['bdate']) - 4, len(memberInfo[i]['bdate'])):
                            year += memberInfo[i]['bdate'][j]
                    else:
                        year = 0
                    Database.insert_members(con, memberInfo[i]["id"], groupId, memberInfo[i]["first_name"], memberInfo[i]["last_name"], int(year))
                    year = ""
    except:
        pass

def outGraph(y):
    fig, ax = plt.subplots()
    x = []
    for i in range(0,len(y)):
        x.append(i)
    ax.bar(x, y)
    plt.savefig('saved.png')
    sendPhoto()

def sendPhoto():
    upload = vk_api.VkUpload(session)
    upload_image = upload.photo_messages(photos='saved.png')[0]
    attachments = []
    attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
    session.method("messages.send", {"domain": domen, "random_id": 0, "message": "Ваш график", 'attachment': ','.join(attachments)})






con = Database.sql_connection()
Database.create_tables(con)


#
averageAge = []

token = input("Введите токен: ")
session = vk_api.VkApi(token=token)
vk = session.get_api()

keyWord = input("Введите ключевое(ые) слово(а) для определения среднего возраста: ").split()
dbAdd = ""
while dbAdd != "yes" and dbAdd != "no":
    dbAdd = input("Найти и добавить новую информацию для поиска или искать в базе?  yes/no ")
    if dbAdd != "yes" and dbAdd != "no":
        print("попробуйте снова")
domen = input("Введите домен пользователя, которому хотите отправить результат ")
if dbAdd == "yes":
    numberOfRequest = int(input("Укажите колличество групп для добавления в базу "))
    for key in keyWord:
        getMembers(getGroupsId(key))
for key in keyWord:
    averageAge.append(Database.getAverageAge(con, key))
    print("Средний возраст по слову: ", key, " = ", Database.getAverageAge(con, key))
outGraph(averageAge)
print("Success")

#ed4194b3dafb94be770ed8156a0cf9f543c7d1a79adb0f9cc65ce2fc29d68fe422b9c53a97114ba549a03

