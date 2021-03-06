import git

from bot import Handle


class Restart_Handle(Handle):
    command = "restart"

    def on_message(self, bot, client, message, raw_message):
        g: git.Git = git.Git(".")
        ans = g.pull("https://github.com/pearisgreen/htwk_bot.git", "master")

        bot.send_message("git:" + ans)

        # os.execv(sys.executable, ["python3"] + sys.argv)
        exit(0)

    def man(self):
        return [
            "usage: !restart",
            "makes the bot pull all pending changes",
            "and restarts itself"
        ]
