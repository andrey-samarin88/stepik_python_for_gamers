# Список изменений в версии mod_v1.0:
# 1. Игрок исследует дом - перемещается из комнаты в комнату в поисках улик +
# 1.1 В начале катки случайно выбрается один призрак +
# 1.2 Улики раскиданы по комнатам случайным образом, если в комнате отсутствуют/закончились улики, то сообщаем об этом игроку после исследования комнаты +
# 1.3 добавлен п.5 - изучить энциклопедию о призраках +
# 1.4 определять тип призрака можно в любой момент но один раз, так же как пить метиловый спирт +

# 2. Игрок ищет укрытие
# 2.1 При падении рассудка < 25 оповестить игрока о том, что призрак начал охоту +
# 2.2 Игрок не знает в каких комнатах есть укрытие, и имеет 50% шанс на успешное использование укрытия если призрак начал охоту +
# 2.3 Нельзя прятаться в одном и том же укрытии 2 раза подряд

import random

#random.seed(int(input()))  #удалить перед выпуском в продакшин
rooms = ["Гостиная", "Кухня", "Спальня", "Ванная", "Подвал"]
#evidences_all = ["Минусовая температура", "Ультрафиолет",
 #                "Детектор ЭМП (ур. 5)", "Радиоприёмник",
  #               "Записи в блокноте", "Лазерный проектор",
   #              "Призрачный огонёк"]
ghosts = ["Джин", "Морой", "Полтергейст", "Банши", "Демон"]
ghost_evidences = [
    ["Минусовая температура", "Ультрафиолет", "Детектор ЭМП (ур. 5)"],   # Джин
    ["Радиоприёмник", "Записи в блокноте", "Минусовая температура"],     # Морой
    ["Радиоприёмник", "Ультрафиолет", "Записи в блокноте"],              # Полтергейст
    ["Лазерный проектор", "Ультрафиолет", "Призрачный огонёк"],          # Банши
    ["Ультрафиолет", "Записи в блокноте", "Минусовая температура"]       # Демон
]

events = ['1 — Исследовать комнату', '2 — Спрятаться', '3 — Перейти в другую комнату', '4 — Определить тип призрака', '5 — Изучить энциклопедию о призраках']
sanity = 100
collected_evidence = []
game_over = False
hunt = False
rested = False

# Комната в которой находится игрок
current_room = random.choice(rooms)

# Список комнат в которые игрок может перейти (здесь творится какая то необъяснимая дичь!!!)
evailable_rooms = []
evailable_rooms = evailable_rooms + rooms
evailable_rooms.remove(current_room)

# Комнаты с укрытием
hiding_spots = random.sample(rooms, k=3)

# Призрак
ghost = random.choice(ghosts)

# Улики раскидываем по комнатам
room_evidences = [[] for _ in range(len(rooms))]
for i in ghost_evidences[ghosts.index(ghost)]:
    room_evidences[random.randint(0, 4)].append(i)

# Вступление
print(f'''Вы — охотник за привидениями, которого наняли провести расследования в старом заброшенном особняке.
В доме происходят странные явления: слышны шаги, скрипы, а иногда даже голоса.
Ваша задача — собрать доказательства, определить тип призрака и безопасно покинуть дом.

Будьте осторожны: призрак может быть опасен, а уровень вашего рассудка будет падать.
Если рассудок опустится до нуля, вы рискуете сойти с ума или стать жертвой призрака.''')

print('Начать игру? (Да/Нет)')
if input('Ваш выбор: ').capitalize() == 'Да':
    while not game_over:
        hunt = (0 < sanity < 25)  # Флаг охоты
        print(f'\nРассудок: {sanity}', '(призрак почуял ваш страх 💩 и начал охоту, будьте осторожны!)' if hunt else '')
        print(f'Текущая комната: {current_room}')
        print(f'Доступные комнаты: {", ".join(evailable_rooms)}')
        print(f'Найденные улики:  {", ".join(collected_evidence)}')
        print(f'Выберите действие:')
        print('\n'.join(events))

        # Защита от ввода недопустимых значений
        while True:
            action = input('Ваш выбор: ')
            len_events = len(events)
            if action.isdigit():
                if int(action) in range(1, len_events + 1):
                    action = int(action)
                    break
            print(f'Выбор неверный, введите цифру от 1 до {len_events}')
        match action:
            case 1:  # Исследовать комнату
                rested = False
                if random.randint(0, 1):
                    sanity = sanity - (damage := random.randint(15, 25))
                    print(f'Вы увидели паранормальное явление! Потеря рассудка: {damage}')
                    if sanity <= 0:
                        print("Вы че угараете? В какую дурку? *звуки сирены*")
                        game_over = True
                else:
                    for i in room_evidences[rooms.index(current_room)]:
                        if i not in collected_evidence:
                            collected_evidence.append(i)
                            room_evidences[rooms.index(current_room)].remove(i)
                            print(f'Вы нашли улику: {i}')
                            break
                    else:
                        print('Улики не найдены')
            case 2:  # Спрятаться
                if hunt:
                    if random.randint(0, 1):
                        if current_room in hiding_spots:
                            print('Вы попытались спрятаться, но неудачно. Призрак нашёл вас, игра окончена!')
                        else:
                            print("В этой комнате нет укрытия. Призрак нашёл вас, игра окончена!")
                        game_over = True
                        break
                if current_room in hiding_spots:
                    if not rested:
                        sanity = sanity + (recovery := random.randint(5, 10))
                        if sanity > 100:
                            sanity = 100
                        rested = True
                        print(f'Вы отдохнули в укрытии. Рассудок восстановлен на {recovery}')
                    else:
                        print(f'Отдыхать в этом укрытии слишком опасно, нужно поискать другое')
                else:
                    print('В этой комнате нет укрытия.')
            case 3:  # Перейти в другую комнату
                rested = False
                while True:
                    print('Куда хотите перейти?')
                    target = input('Ваш выбор: ').capitalize()
                    if target in evailable_rooms:
                        # Обновляем список комнат в которые можно перейти
                        evailable_rooms.append(current_room)
                        evailable_rooms.remove(target)
                        # Обновляем название комнаты в которой находимся
                        current_room = target
                        print(f'Вы перешли в комнату: {current_room}')
                        break
                    elif target == current_room:
                        print('Вы уже находитесь в этой комнате')
                        break
                    else:
                        print('Комната не найдена, попробуйте снова.')
            case 4:  # Определить тип призрака
                print('''Выберите тип призрака:
- Джин
- Морой
- Полтергейст
- Банши
- Демон''')
                choise = input("Ваш выбор: ").capitalize()
                if choise in ghosts:
                    if choise == ghost:
                        print(f'Вы правильно определили призрака: {choise}! Победа!')
                        game_over = True
                    else:
                        print('Вы ошиблись! Игра окончена.')
                        game_over = True
                else:
                    print('Такого призрака нет, введите название из списка')
            case 5:  # Изучить энциклопедию о призраках
                print('===Энциклопедия о призраках===')
                for i in range(len(ghosts)):
                    print(f'{ghosts[i]}: {", ".join(ghost_evidences[i])}')
