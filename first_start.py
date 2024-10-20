import time
from MyLife import MyLife

my_life = MyLife.create_first_process()
time.sleep(1)
my_life.act('Первое сообщение в первом процессе')
time.sleep(1)
first_person = my_life.act('NEW_PERSON', official=True)
time.sleep(1)
first_person.act('Первое сообщение во втором процессе')
time.sleep(1)
second_person = my_life.act('NEW_PERSON', official=True)
time.sleep(1)
second_person.act('Первое сообщение в третьем процессе')
time.sleep(1)
first_person.act("CHANGE_NAME Jonny", official=True)
time.sleep(1)
second_person.act("CHANGE_NAME Richard", official=True)
time.sleep(1)
second_person.act(f'CROSS {first_person.get_identifier()[0]}', official=True)
time.sleep(1)
my_life.act('Второе сообщение в первом процессе')
time.sleep(1)
first_person.act('Второе сообщение во втором процессе')
time.sleep(1)
second_person.act('Второе сообщение в третьем процессе')
time.sleep(1)

debt1 = first_person.act('NEW_DEBT', official=True)
time.sleep(1)
debt1.act('Первое сообщение в четвёртом процессе')
time.sleep(1)

debt2 = second_person.act('NEW_DEBT', official=True)
time.sleep(1)
debt2.act('Первое сообщение в пятом процессе')
time.sleep(1)

debt1.act('Второе сообщение в четвёртом процессе')
time.sleep(1)
debt1.act('TAKE 100', official=True)
time.sleep(1)
debt2.act('Второе сообщение в пятом процессе')
time.sleep(1)
debt1.act('GIVE 100', official=True)
time.sleep(1)
debt2.act('GIVE 50', official=True)
time.sleep(1)
debt2.act('TAKE 50', official=True)
time.sleep(1)


debt11 = first_person.act('NEW_DEBT', official=True)
time.sleep(1)
first_person.act('Третье сообщение во втором процессе')
time.sleep(1)
debt11.act('TAKE 50', official=True)
time.sleep(1)
debt11.act('Первое сообщение в 6 процессе')
time.sleep(1)

debt21 = second_person.act('NEW_DEBT', official=True)
time.sleep(1)
debt11.act('GIVE 30', official=True)
debt11.act('24.06.2025-15:00:00 Мне будет 38 лет')
time.sleep(1)
debt21.act('Первое сообщение в 7 процессе')
time.sleep(1)

print(my_life)
print(first_person)
print(second_person)
