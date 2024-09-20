from users.models import User

def fill_new_user_mentor(message):

    new_mentor = User.objects.create(tg_id=message.from_user.id)
    new_mentor.set_password('12345')

    print(new_mentor)

    # self.user_text_input(message, new_mentor, 'name', self.db.insert_values, 'mentors', self.offer_next_actions)


"""def user_text_input(self, message, new_data, key, add_to_db_function, table_name, final_function):
    if key is not None:
        self.add_data_in_dict(new_data, key, message.text)

    mandatory = True
    next_key = ''
    for new_key, value in new_data.items():
        if value is None:
            next_key = new_key
            mandatory = True
            break
        elif value == '':
            next_key = new_key
            mandatory = False
            break

    if next_key and mandatory:
        msg = self.bot.send_message(message.chat.id,
                                    f'введите {next_key}:',
                                    reply_markup=self.add_options_keyboard(next_key))

        self.bot.register_next_step_handler(msg, self.user_text_input,
                                            new_data, next_key, add_to_db_function, table_name, final_function)
    elif next_key and not mandatory:
        msg = self.bot.send_message(message.chat.id,
                                    f'введите {next_key}, (чтобы пропустить введите /skip):',
                                    reply_markup=self.add_options_keyboard(next_key))

        self.bot.register_next_step_handler(msg, self.user_text_input,
                                            new_data, next_key, add_to_db_function, table_name, final_function)
    else:
        print(new_data)
        errors_or_None = add_to_db_function(new_data, table_name)
        if errors_or_None is None:
            text = f'добавлен {new_data["name"]}.'
        else:
            text = str(errors_or_None)

        msg = self.bot.send_message(message.chat.id,
                                    text,
                                    reply_markup=self.add_options_keyboard())
        self.bot.register_next_step_handler(msg, final_function)
"""
