import kivy

kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock

import multiprocessing
import usbSerial

# check the queue for pending messages, and rely that to all connected clients
# def checkQueue():
#     if not input_queue.empty():
#         message = input_queue.get()
#         # for c in clients:
#         #    c.write_message(message)
#         print "Input: {}".format(message)
#     return True


class SerialTestingForm(BoxLayout):

    cmd_to_send = ObjectProperty
    cmd_results = ObjectProperty

    def send_command(self, value):
        self.cmd_results.text += 'Output: {}\n'.format(self.cmd_to_send.text)
        output_queue.put(self.cmd_to_send.text.encode('ascii'))
        self.cmd_to_send.text = ''
        self.cmd_to_send.focus = True

    def checkQueue(self):
        if not input_queue.empty():
            message = input_queue.get()
            # Need to access checkQueue from the App object???
            self.cmd_results.text += "Input: {}\n".format(message)
        return True


class SerialTestingApp(App):

    def build(self):
        # call checkQueue every 0.5 seconds
        Clock.schedule_interval(lambda dt: self.checkQueue(), 0.5)
        self.root.ids.cmd_to_send.focus = True

    def checkQueue(self):
        if not input_queue.empty():
            message = input_queue.get()
            # Need to access checkQueue from the App object???
            self.root.ids.cmd_results.text += "Input: {}\n".format(message)
            self.root.ids.cmd_to_send.focus = True
            self.root.ids.cmd_to_send.select_all()
        return True


if __name__ == '__main__':
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()


    # start the serial worker in background (as a daemon)
    sp = usbSerial.SerialProcess(output_queue, input_queue)
    sp.daemon = True
    sp.start()

    # start the Kivy application.
    SerialTestingApp().run()
