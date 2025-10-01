import random

import telebot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config.settings import TELEGRAM_BOT_API

bot = telebot.TeleBot(TELEGRAM_BOT_API)


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer: telebot.types.PollAnswer):
    from quiz.models import AnswersQuiz, PollUserSending

    poll_user_sending: PollUserSending = PollUserSending.objects.filter(id_quiz=poll_answer.poll_id).first()
    telegram_quiz = poll_user_sending.quiz

    telegram_quiz.count_view_answer += 1

    selected_option = poll_answer.option_ids[0]
    all_answers = telegram_quiz.answers.all()
    is_correct_answer: AnswersQuiz = all_answers[selected_option]
    if is_correct_answer.right_answer:
        telegram_quiz.count_current_answer += 1
        poll_user_sending.current_status = True
    else:
        telegram_quiz.count_wrong_answer += 1
    telegram_quiz.save()
    poll_user_sending.save()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    """Обрабатывает нажатия на кнопки под викторинами: лайк, дизлайк, жалоба или следующая викторина."""
    from quiz.models import FeedbackQuiz, TelegramQuiz
    from telegram_bot.models import TelegramUser

    id_quiz = str(call.data).split("_")[-1]

    if "next_poll_" in call.data:
        send_random_pool(call.message)
        return

    telegram_user = TelegramUser.objects.filter(id_user=call.from_user.id).first()
    find_quiz: TelegramQuiz = TelegramQuiz.objects.filter(pk=id_quiz).first()
    if find_quiz:
        find_feedback = FeedbackQuiz.objects.filter(quiz=find_quiz, telegram_user=telegram_user).first()
        if not find_feedback:
            FeedbackQuiz.objects.get_or_create(quiz=find_quiz, telegram_user=telegram_user)
            if "like_quest_" in call.data:
                find_quiz.feedback_like += 1
            elif "dislike_quest_" in call.data:
                find_quiz.feedback_dislike += 1
            elif "wrong_quest_" in call.data:
                find_quiz.feedback_wrong += 1
            find_quiz.save()
            bot.answer_callback_query(call.id, "Спасибо за отзыв")
        else:
            bot.answer_callback_query(call.id, "Вы уже оставляли отзыв по этой викторине!")


@bot.message_handler(commands=["start", "quiz"])
def quiz_send(message: Message):
    """Отправляет случайную викторину пользователю по команде /start или /quiz."""
    send_random_pool(message)


def send_random_pool(message):
    """Выбирает и отправляет случайную викторину из базы данных с кнопками обратной связи."""
    from quiz.models import PollUserSending, TelegramQuiz
    from telegram_bot.models import TelegramUser

    id_user = message.chat.id
    find_user: TelegramUser = TelegramUser.objects.filter(id_user=id_user).first()

    objects_quiz = TelegramQuiz.objects
    all_objects = objects_quiz.all()
    count_all_objects = all_objects.count()
    if count_all_objects == 0:
        bot.send_message(message.chat.id, "Викторины не добавлены!")
        return
    get_random_quiz = random.randint(0, count_all_objects - 1)

    poll = all_objects[get_random_quiz]
    poll.count_view_answer += 1
    poll.save()

    answers = []
    correct_answer = 0
    for i, answer in enumerate(poll.answers.all()):
        if answer.right_answer:
            correct_answer = i
        answers.append(answer.name)

    inline_list = InlineKeyboardMarkup(row_width=2)
    btn_like = InlineKeyboardButton("Лайк", callback_data=f"like_quest_{poll.pk}")
    btn_dislike = InlineKeyboardButton("Дизлайк", callback_data=f"dislike_quest_{poll.pk}")
    btn_wrong = InlineKeyboardButton("Некорректный вопрос/ответ", callback_data=f"wrong_quest_{poll.pk}")
    next_poll = InlineKeyboardButton("Следующая викториа", callback_data=f"next_poll_{poll.pk}")
    inline_list.add(btn_like, btn_dislike, btn_wrong)
    inline_list.add(next_poll)

    sending_pool = bot.send_poll(
        message.chat.id,
        question=f"#{poll.pk} {poll.quest}",
        options=answers,
        explanation=poll.hint,
        type="quiz",
        correct_option_id=correct_answer,
        message_thread_id=message.message_thread_id,
        is_anonymous=False,
        reply_markup=inline_list,
    )

    PollUserSending.objects.create(
        id_quiz=sending_pool.poll.id,
        quiz_user=poll.user,
        quiz=poll,
        telegram_user=find_user,
        current_status=False,
    )


@bot.message_handler(func=lambda message: True)
def get_all_message(message: Message):
    """Сохраняет или обновляет информацию о пользователе при получении любого сообщения."""
    from telegram_bot.models import TelegramUser

    id_user = message.from_user.id
    username_user = message.from_user.username
    first_name_user = message.from_user.first_name
    last_name_user = message.from_user.last_name

    find_user: TelegramUser = TelegramUser.objects.filter(id_user=id_user).first()
    if not find_user:
        TelegramUser.objects.create(
            id_user=id_user,
            username_user=username_user,
            first_name_user=first_name_user,
            last_name_user=last_name_user,
        )
    else:
        find_user.username_user = username_user
        find_user.first_name_user = first_name_user
        find_user.last_name_user = last_name_user
        find_user.save()
