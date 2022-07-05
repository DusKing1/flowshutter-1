# Flowshutter
# Copyright (C) 2021  Hugo Chiang

# Flowshutter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Flowshutter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with flowshutter.  If not, see <https://www.gnu.org/licenses/>.
import settings
settings.read()
import task
task = task.Task()

from machine import Timer
timer0 = Timer(0) # 200Hz task scheduler
timer0.init(period=5, mode=Timer.PERIODIC, callback=task.scheduler)

if task.ui.camera.task_mode == "THREAD":
    import _thread
    import machine
    machine.freq(240000000)
    _thread.start_new_thread(task.ui.camera.uart_handler, ())

import uasyncio as asyncio
loop = asyncio.get_event_loop()
loop.create_task(task.fc_link.uart_handler())
loop.create_task(task.ui.buttons.checker('PAGE UP'))
loop.create_task(task.ui.buttons.checker('PAGE DOWN'))
loop.create_task(task.ui.buttons.checker('ENTER'))
loop.create_task(task.ui.battery.adc_handler())
if task.ui.camera.task_mode == "ASYNC":
    loop.create_task(task.ui.camera.uart_handler())
loop.run_forever()
