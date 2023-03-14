# import signal

from pytest_celery.api.container import CeleryTestContainer


class CeleryWorkerContainer(CeleryTestContainer):
    def ready(self) -> bool:
        return super().ready()
        if "tomer" not in self.attrs["Config"]["Env"][0]:
            super().ready()
            # self.attrs["Config"]["Env"][0] = "CELERY_BROKER_URL=memory://tomer"
            env_vars = self.env
            env_vars["CELERY_BROKER_URL"] = "memory://tomer"
            self.exec_run(f"export CELERY_BROKER_URL='{env_vars['CELERY_BROKER_URL']}'")
            self.restart()

        # if "ready." not in self.logs():
        #     return False
        # if "pong" not in self.logs():
        #     return False
        return True

    def client(self):
        print(self.logs())
        # env_vars = self.env
        # env_vars["CELERY_BROKER_URL"] = "memory://tomer"
        # self.exec_run(f"export CELERY_BROKER_URL='{env_vars['CELERY_BROKER_URL']}'")
        # self.restart()
        # self.attrs["Config"]["Env"][0] = "CELERY_BROKER_URL=memory://tomer"
        # self.reload()
        # print(self.logs())
        # current_app.conf.broker_url = "memory://tomer"
        # print(self.logs())
        # self.reload()
        # self.kill()
        # self.restart()
        # print(self.logs())
        return self
