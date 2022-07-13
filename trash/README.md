Анимация для предмета, лятещего сверху вниз. Помогает отобразить перемещение мусора по орбите.

Движение предмета строго вертикально. Выберите номер колонки и запустите корутину, она полетит сверху вниз:

```python3

with open('garbage.txt', "r") as garbage_file:
  frame = garbage_file.read()

coroutine = fly_garbage(canvas, column=10, garbage_frame=frame)
```