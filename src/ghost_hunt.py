import random

random.seed(int(input()))
rooms = ["Гостиная", "Кухня", "Спальня", "Ванная", "Подвал"]
evidences_all = ["Минусовая температура", "Ультрафиолет", 
                 "Детектор ЭМП (ур. 5)", "Радиоприёмник", 
                 "Записи в блокноте", "Лазерный проектор", 
                 "Призрачный огонёк"]
ghosts = ["Джин", "Морой", "Полтергейст", "Банши", "Демон"]
ghost_evidences = [
    ["Минусовая температура", "Ультрафиолет", "Детектор ЭМП (ур. 5)"],   # Джин
    ["Радиоприёмник", "Записи в блокноте", "Минусовая температура"],     # Морой
    ["Радиоприёмник", "Ультрафиолет", "Записи в блокноте"],              # Полтергейст
    ["Лазерный проектор", "Ультрафиолет", "Призрачный огонёк"],          # Банши
    ["Ультрафиолет", "Записи в блокноте", "Минусовая температура"]       # Демон
]
sanity = 100
collected_evidence = []

current_room = random.choice(rooms)
hiding_spots = random.sample(rooms, k=3)
game_over = False

def recovery_func():
    if current_room in hiding_spots:
        global sanity
        sanity = sanity + (recovery := random.randint(5, 10))
        if sanity > 100:
            sanity = 100
        print(f'Вы отдохнули в укрытии. Рассудок восстановлен на {recovery}')
    else:
        print('В этой комнате нет укрытия.')

while not game_over:
    print(f'Рассудок: {sanity}')
    print(f'Текущая комната: {current_room}')
    print(f'Комнаты с укрытиями: {", ".join(hiding_spots)}')
    print('''Выберите действие:
1 — Исследовать комнату
2 — Спрятаться
3 — Перейти в другую комнату
4 — Определить тип призрака''')
    action = int(input("Ваш выбор: "))

    match action:
        case 1:
            if random.randint(0, 1):
                sanity = sanity - (damage := random.randint(5, 15))
                print(f'Вы увидели паранормальное явление! Потеря рассудка: {damage}')
                if sanity <= 0:
                    print("Вы че угараете? В какую дурку? *звуки сирены*")
                    game_over = True
            else:
                if len(collected_evidence ) < 3:
                    random.shuffle(evidences_all)
                    for i in evidences_all:
                        if i not in collected_evidence:
                            collected_evidence.append(i)
                            print(f'Вы нашли улику: {i}')
                            break
                else:
                    print('Улики уже собраны.')
        case 2:
            if 0 < sanity < 25:
                if random.randint(0, 1):
                    print('Призрак начал охоту!')
                    if current_room in hiding_spots:
                        sanity = sanity + (recovery := random.randint(5, 10))
                        if sanity > 100:
                            sanity = 100
                        print(f'Вы спрятались, призрак вас не нашёл! Рассудок восстановлен на {recovery}')
                    else:
                        print("В этой комнате нет укрытия. Призрак нашёл вас, игра окончена!")
                        game_over = True
                else:
                    recovery_func()
            else:
                recovery_func()
        case 3:
            while True:
                target = input("Куда хотите перейти? ").capitalize()
                if target in rooms:
                    current_room = target
                    print(f'Вы перешли в комнату: {current_room}')
                    break
                else:
                    print('Комната не найдена, попробуйте снова.')
        case 4:
            if len(collected_evidence) == 3:
                print(f'Найденные улики: {", ".join(collected_evidence)}')
                print('''Выберите тип призрака:
- Джин
- Морой
- Полтергейст
- Банши
- Демон''')
                ghost = input("Ваш выбор: ").capitalize()
                if ghost in ghosts:
                    count_evidence = 0
                    for i in collected_evidence:
                        if i in ghost_evidences[ghosts.index(ghost)]:
                            count_evidence += 1
                    if count_evidence == 3:
                        print(f'Вы правильно определили призрака: {ghost}! Победа!')
                        game_over = True
                    else:
                        print('Вы ошиблись! Игра окончена.')
                        game_over = True
                else:
                    print('Такого призрака нет.')
            else:
                print('Для определения типа призрака необходимо собрать все 3 улики.')
    print('')