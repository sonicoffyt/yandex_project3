from aiogram import types

admin_keyboard = types.InlineKeyboardMarkup()
admin_keyboard.row(types.InlineKeyboardButton('Сделать рассылку', callback_data='mailing'))
admin_keyboard.row(types.InlineKeyboardButton('Забанить/разбанить пользователя', callback_data='ban'),
                   types.InlineKeyboardButton('Количество пользователей', callback_data='count'))
admin_keyboard.row(types.InlineKeyboardButton('В главное меню', callback_data='return_to_main_menu'))


return_to_main_admin_menu_kb = types.InlineKeyboardMarkup()
return_to_main_admin_menu_button = types.InlineKeyboardButton('Вернуться в главное меню', callback_data='admin_panel')
return_to_main_admin_menu_kb.row(return_to_main_admin_menu_button)

return_to_main_menu_kb = types.InlineKeyboardMarkup()
return_to_main_menu_button = types.InlineKeyboardButton('Вернуться в главное меню', callback_data='return_to_main_menu')
return_to_main_menu_kb.row(return_to_main_menu_button)

return_to_help_menu_kb = types.InlineKeyboardMarkup()
return_to_main_menu_button = types.InlineKeyboardButton('Назад', callback_data='help')
return_to_help_menu_kb.row(return_to_main_menu_button)

return_to_profile_menu_kb = types.InlineKeyboardMarkup()
return_to_main_menu_button = types.InlineKeyboardButton('Назад', callback_data='profile')
return_to_profile_menu_kb.row(return_to_main_menu_button)

