from datetime import datetime
from bot import Handle
import pickle

DATE_FILE = "deadlines/dates"


class Deadlines_Handle(Handle):
    command = "deadlines"

    dates = []

    def __init__(self):
        super().__init__()
        self.load_dates()

    def on_message(self, bot, client, message, raw_message):
        msg_array = message.split()

        try:
            if len(msg_array) == 0 or msg_array[0] == "list":
                self.list_dates(bot)
            elif msg_array[0] == "add":
                self.add_date(msg_array[1], " ".join(msg_array[2:len(msg_array)]))
                bot.send_message("```Date has been added```")
            elif msg_array[0] == "edit":
                self.edit_date(int(msg_array[1]), msg_array[2], " ".join(msg_array[3:len(msg_array)]))
                bot.send_message("```Date has been updated```")
            elif msg_array[0] == "remove":
                self.remove_date(int(msg_array[1]))
                bot.send_message("```Date has been removed```")
            else:
                raise Exception("Unknown argument: " + msg_array[0] + ". See man " + self.command)
        except IndexError:
            raise IndexError("Wrong number of arguments: " + " ".join(msg_array) + ". See man " + self.command)
        except ValueError:
            raise ValueError("Wrong format: " + " ".join(msg_array[1:len(msg_array)]) + ". See man " + self.command)

    def man(self):
        return [
            "usage: !deadlines [add|edit|remove|list] args",
            "Manages a list of deadlines",
            "Arguments:",
            "  !deadlines list or !deadlines :",
            "    lists all currently saved deadlines",
            "  !deadlines add <dd>.<mm>.<yy>:<HH>:<MM> <description>",
            "    adds new deadline of given date and description",
            "  !deadlines remove <id>",
            "    removes the date of the id, id given by list",
            "  !deadlines edit <id> <dd>.<mm>.<yy>:<HH>:<MM> <description>",
            "    changes data of the date of the id, id given by list",
            "Example: !deadlines add 01.03.37:16:20 Modellierung V5R15"
        ]

    def save_dates(self):
        with open(DATE_FILE, "wb") as file:
            pickle.dump(self.dates, file, pickle.HIGHEST_PROTOCOL)

    def load_dates(self):
        try:
            with open(DATE_FILE, "rb") as file:
                self.dates = pickle.load(file)
                self.update()
        except:
            # TODO
            pass

    def list_dates(self, bot):
        self.update()
        if len(self.dates) == 0:
            bot.send_message("404")
            return
        id_size = len(str(len(self.dates)))
        desc_size = max([len(date["module"]) for date in self.dates])
        date_str = "```--------DEADLINES--------\n"
        for date in self.dates:
            date_str += ("ID: " + str(date["id"]).rjust(id_size) + " --- DESC: " + date["module"].ljust(desc_size)
                         + " --- DATE: " + date["date"].strftime("%d.%m.%y %H:%M Uhr") + " |\n")
        bot.send_message(date_str + "```")

    def add_date(self, date_str, module_str):
        date = {
            "id": len(self.dates),
            "date": datetime.strptime(date_str, "%d.%m.%y:%H:%M"),
            "module": module_str
        }
        self.dates.append(date)
        self.update()

    def edit_date(self, date_id, date, desc):
        self.remove_date(date_id)
        self.add_date(date, desc)

    def remove_date(self, date_id):
        self.dates = [date for date in self.dates if date["id"] != date_id]
        self.update()

    def update(self):
        self.dates = [date for date in self.dates if date["date"] > datetime.now()]
        self.dates.sort(key=lambda date: date["date"])
        for i in range(0, len(self.dates)):
            self.dates[i]["id"] = i
        self.save_dates()
