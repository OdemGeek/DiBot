import discord
import os
from replit import db


class dataManagment():

    warningLimit = 3
    callback = ()

    def __init__(self, warningLimit, callback):
        # body of the constructor
        self.warningLimit = warningLimit
        self.callback = callback

    #добавляем нарушение
    async def addViolation(self, member: discord.Member, channel, cause: str):
        #если у нас уже есть такой ключ то добавляем 1 нарушение
        if f'violations{member.id}' in db.keys():
            db[f'violations{member.id}'] = db[f'violations{member.id}'] + 1
        else:  #иначе создаём ключ
            db[f'violations{member.id}'] = 1
        #if db[f'violations{member.id}'] >= self.warningLimit:
        await self.callback(member, channel, cause)

    #уменьшаем нарушения
    def substructViolation(self, member: discord.Member, count: int = 1):
        #если у нас уже есть такой ключ то уменьшаем
        if f'violations{member.id}' in db.keys():
            db[f'violations{member.id}'] = db[f'violations{member.id}'] - count
            if db[f'violations{member.id}'] <= 0:
                #если 0 нарушений после выычитания убираем ключ
                del db[f'violations{member.id}']

    #убираем нарушение
    def deleteViolation(self, member: discord.Member):
        #если у нас уже есть такой ключ то уменьшаем 
        if f'violations{member.id}' in db.keys():
            del db[f'violations{member.id}']

       
    #берём количество нарушений пользователя
    def getViolation(self, member: discord.Member) -> int:
        #если у пользователя были нарушения то берём кол-во из списка
        if f'violations{member.id}' in db.keys():
            return db[f'violations{member.id}']
        else:
            return 0

        
