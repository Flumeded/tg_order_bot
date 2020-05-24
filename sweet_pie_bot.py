#!/usr/bin/env python
# coding: utf-8



import config
import telebot
import pipline_bot

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

print('hello')

lst_to_add = []


test_number = 10
test_number_status = 10
num_ready = {}

bot = telebot.TeleBot(config.token)
dict_insert = {}


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="order_correct"),
                               InlineKeyboardButton("Нет", callback_data="order_incorrect"), InlineKeyboardButton("Назад", callback_data="back_to_priority"))
    return markup


def check_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Мои заказы", callback_data = "my_orders"),
               InlineKeyboardButton("Мой последний заказ", callback_data = "my_last_order"),
               InlineKeyboardButton("По уникальному номеру заказа", callback_data = "unique_order"),
               InlineKeyboardButton("Назад", callback_data="back_to_main"))
    return markup


def readines_change_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="change_order"),
                               InlineKeyboardButton("Нет", callback_data="no_change_order")
)
    return markup



def back_to_main_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_main"))
    return markup


def back_to_link(): 
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_link"))
    return markup

def back_to_qty():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_qty"))
    return markup


def back_to_priority():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_qty"))
    return markup

def priority_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('low', callback_data = 'low'),
               types.InlineKeyboardButton('medium', callback_data = 'medium'),
               types.InlineKeyboardButton('high', callback_data = 'high'),
               types.InlineKeyboardButton('Назад', callback_data = 'back_to_qty'))
    return markup

def main_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Добавить заказ на печать', callback_data='add_print'),
               types.InlineKeyboardButton('Удалить заказ на печать', callback_data='delete_print'),
               types.InlineKeyboardButton('Уточнить статус', callback_data='check_print'))
    return markup

def back_to_info_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_info_menu"))
    return markup



@bot.message_handler(content_types=['text'])




def start_message(message):
    if message.text == 'Start': 
        bot.send_message(message.from_user.id, "Добрый день,  Вас приветсвует бот Щ.И.К.А.Р.Н.О 4000. Пожалуйста выберете ниже желаемое дейсвтие", reply_markup=main_markup())
        dict_insert[str(message.from_user.id)] = {}
        dict_insert[str(message.from_user.id)]['customer_name'] = str(message.from_user.last_name) +' '+ str(message.from_user.first_name)
        dict_insert[str(message.from_user.id)]['customer_unique_number'] = message.from_user.id
        dict_insert[str(message.from_user.id)]['back'] = '0'
    elif message.text == 'Peterform' and (message.from_user.id == 303177484 or message.from_user.id == 504967952):
        bot.send_message(message.from_user.id, 'Введи номер заказа который готов')
        bot.register_next_step_handler(message, update_status)
    else:
        bot.send_message(message.from_user.id, 'Введи: Start')


def link_catch(message):
    if dict_insert[str(message.from_user.id)]['back'] != 'not_to_link':
        bot.send_message(message.from_user.id, "Сколько изделий тебе нужно",reply_markup=back_to_link())
        lst_to_add.append(message.text)
        dict_insert[str(message.from_user.id)]['link'] = message.text
        dict_insert[str(message.from_user.id)]['back'] = '2'
        bot.register_next_step_handler(message, qty_catch)




def qty_catch(message):
        if dict_insert[str(message.from_user.id)]['back'] != 'not_to_qty':
            lst_to_add.append(message.text)
            bot.send_message(message.from_user.id, "Каков приоритет печати", reply_markup=priority_markup())
            dict_insert[str(message.from_user.id)]['quantity'] = message.text
            dict_insert[str(message.from_user.id)]['back'] = '0'

def order_confirm(message):
        markup = types.InlineKeyboardMarkup(row_width =3)
        item1 = types.InlineKeyboardButton('Да', callback_data = 'order_correct')
        item2 = types.InlineKeyboardButton('Нет', callback_data = 'order_incorrect')
        item3 = types.InlineKeyboardButton('Назад', callback_data = 'back_to_priority')
        bot.send_message(message.from_user.id, 'Твой заказ: '+str(lst_to_add[0])+' кол-во '+lst_to_add[1]+' приоритет '+lst_to_add[2]+'?', reply_markup=markup)

def del_confirm(message):
    if dict_insert[str(message.from_user.id)]['back'] != 'not_to_link':
        bot.send_message(message.from_user.id, pipline_bot.order_delete(customer_unique_number = str(message.from_user.id), uniq_number = int(message.text)))
        dict_insert[str(message.from_user.id)]['back'] =  '0'
        bot.send_message(504967952, 'Пользователь {} {} удалил заказ № {} '.format(str(message.from_user.last_name), str(message.from_user.first_name), str(message.text)))

def check_number_confirm(message):
        t3 = pipline_bot.order_check_func(customer_unique_number = str(dict_insert[str(message.from_user.id)]['customer_unique_number']), unique_number = int(message.text))
        bot.send_message(message.from_user.id, t3, reply_markup=back_to_info_menu())

def update_status(message):
    bot.send_message(message.from_user.id,'Ты точно хочешь изменить статуc заказа №' + message.text+ ' на готово', reply_markup=readines_change_markup())
    num_ready['number'] = int(message.text)
 


def order_confirm(message):
    bot.send_message(call.from_user.id,
                     'Твой заказ: ' + str(dict_insert[str(call.from_user.id)]['link']) + ' кол-во ' + str(
                         dict_insert[str(call.from_user.id)]['quantity']) + ' приоритет ' + str(
                         dict_insert[str(call.from_user.id)]['priority']) + '?', reply_markup=gen_markup())



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'add_print':
                message = bot.send_message(call.message.chat.id, 'кинь свой линк, мразь', reply_markup=back_to_main_markup());
                if dict_insert[str(call.from_user.id)]['back'] != 'not_to_link':
                    bot.register_next_step_handler(message, link_catch);
            elif call.data == 'delete_print':
                message = bot.send_message(call.from_user.id, 'введи уникальный номер печати на удаление', reply_markup=back_to_main_markup());
                if dict_insert[str(call.from_user.id)]['back'] != 'not_to_link':
                    bot.register_next_step_handler(message, del_confirm);
            elif call.data == 'check_print':
                message = bot.send_message(call.from_user.id, "Тип проверки:", reply_markup=check_markup());

                
# вопрос о приоретете печати
            elif call.data == 'low':
                lst_to_add.append('low');
                dict_insert[str(call.from_user.id)]['priority'] = 'low';
                if dict_insert[str(call.from_user.id)]['back'] != 'not_to_confirm':
                    bot.send_message(call.from_user.id, 'Твой заказ: '+str(dict_insert[str(call.from_user.id)]['link'])+' кол-во '+str(dict_insert[str(call.from_user.id)]['quantity'])+' приоритет '+str(dict_insert[str(call.from_user.id)]['priority'])+'?', reply_markup=gen_markup())
            elif call.data == 'medium':
                lst_to_add.append('medium');
                dict_insert[str(call.from_user.id)]['priority'] = 'medium';
                if dict_insert[str(call.from_user.id)]['back'] != 'not_to_confirm':
                    bot.send_message(call.from_user.id, 'Твой заказ: '+str(dict_insert[str(call.from_user.id)]['link'])+' кол-во '+str(dict_insert[str(call.from_user.id)]['quantity'])+' приоритет '+str(dict_insert[str(call.from_user.id)]['priority'])+'?', reply_markup=gen_markup())
            elif call.data == 'high':
                lst_to_add.append('high');
                dict_insert[str(call.from_user.id)]['priority'] = 'high';
                if dict_insert[str(call.from_user.id)]['back'] != 'not_to_confirm':
                    bot.send_message(call.from_user.id, 'Твой заказ: '+str(dict_insert[str(call.from_user.id)]['link'])+' кол-во '+str(dict_insert[str(call.from_user.id)]['quantity'])+' приоритет '+str(dict_insert[str(call.from_user.id)]['priority'])+'?', reply_markup=gen_markup())

                
# проверка пользователем коректен ли заказ               
            elif call.data == 'order_correct':
                message = bot.send_message(call.message.chat.id, "Спасибо заказ сохранен");
                pipline_bot.insert_order(dict_insert[str(call.from_user.id)])

            elif call.data == 'order_incorrect':
                message = bot.send_message(call.message.chat.id, "Заказ отменен");

            elif call.data == 'my_orders':
                t1 = pipline_bot.order_check_func(customer_unique_number = str(dict_insert[str(call.from_user.id)]['customer_unique_number']), unique_number = 'all');
                message = bot.send_message(call.message.chat.id, t1, reply_markup=back_to_info_menu());

# выбери тип проверки
            elif call.data == 'my_last_order':
                t2 = pipline_bot.order_check_func(customer_unique_number = str(dict_insert[str(call.from_user.id)]['customer_unique_number']), unique_number = 'last');
                message = bot.send_message(call.message.chat.id, t2, reply_markup=back_to_info_menu());

            elif call.data == 'unique_order':
                message = bot.send_message(call.message.chat.id, "Введи номер заказа")
                bot.register_next_step_handler(message, check_number_confirm);
            
            elif call.data == 'change_order':
                message = bot.send_message(call.message.chat.id, "Статус заказа {} изменен готово".format(str(num_ready)) )
                #pipline_bot.order_statu_update(num_ready['number'])
                bot.send_message(pipline_bot.order_statu_update(num_ready['number']), "Статус заказа {} изменен готово".format(str(num_ready)) )
            elif call.data == 'no_change_order':
                message = bot.send_message(call.message.chat.id, "статус заказа остался прежним")


            elif call.data == "back_to_main":
                 dict_insert[str(call.from_user.id)]['back'] = 'not_to_link'
                 message = bot.send_message(call.message.chat.id, "Введи Start")
                 bot.register_next_step_handler(message, start_message);
            elif call.data == "back_to_link":
                 dict_insert[str(call.from_user.id)]['back'] = 'not_to_qty'
                 message = bot.send_message(call.message.chat.id, "кинь свой линк, мразь")
                 bot.register_next_step_handler(message, link_catch);
            elif call.data == "back_to_qty":
                 dict_insert[str(call.from_user.id)]['back'] = 'not_to_priority'
                 message = bot.send_message(call.message.chat.id, "Сколько изделий тебе нужно")
                 bot.register_next_step_handler(message, qty_catch);
            elif call.data == "back_to_priority":
                 dict_insert[str(call.from_user.id)]['back'] = 'not_to_confir1'
                 message = bot.send_message(call.message.chat.id, "Каков приоритет печати", reply_markup=priority_markup())
            elif call.data == 'back_to_info_menu':
                 message = bot.send_message(call.from_user.id, "Тип проверки:", reply_markup=check_markup());



  
            bot.edit_message_text(chat_id =call.message.chat.id, message_id=call.message.message_id, text = 'Заебато ответил', reply_markup = None)





    except Exception as e:
        print(repr(e))




print('zdarova_chuvaki :')
print(num_ready)




bot.polling(none_stop=True)

print(dict_insert)
