from io import BytesIO
import requests
from PIL import Image
import base64
import ddddocr
import toml
import colorlog

class Log:
    def __init__(self, name="main", level="INFO"):
        self.name = name
        if level == "INFO":
            self.logger = colorlog.getLogger(self.name)
            self.logger.setLevel(colorlog.INFO)
            self.handler = colorlog.StreamHandler()
            self.handler.setLevel(colorlog.INFO)
        elif level == "DEBUG":
            self.logger = colorlog.getLogger(self.name)
            self.logger.setLevel(colorlog.DEBUG)
            self.handler = colorlog.StreamHandler()
            self.handler.setLevel(colorlog.DEBUG)
        # 修改日志格式，使其更美观
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s][%(name)s][%(levelname)s] [%(message)s]',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            })

    def main(self, level, message):
        message = str(message)
        # 检查是否已经添加了 handler
        if not self.logger.handlers:
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARN":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
        else:
            self.logger.error("日志输出等级设置错误")

class Login:
    def __init__(self):
        self.session = requests.Session()

        self.log = Log("Login")
        self.url_pic = "http://zhjw.qfnu.edu.cn/jsxsd/verifycode.servlet"
        self.Main_url = "http://zhjw.qfnu.edu.cn/jsxsd/framework/xsMain.jsp"
        self.login_url = "http://zhjw.qfnu.edu.cn/jsxsd/xk/LoginToXkLdap"
    def Get_pic(self):
        pic = self.session.get(self.url_pic).content
        image = Image.open(BytesIO(pic))
        return image

    def Get_code(self,image):
        code = ddddocr.DdddOcr(show_ad=False).classification(image)
        return code

    def Base_user(self):
        with open("./config.toml","r",encoding="utf-8") as f:
            config = toml.load(f)

        user_account = config["username"]
        user_password = config["password"]

        base_user = str(base64.b64encode(user_account.encode("utf-8")), "utf-8") + "%%%" + str(base64.b64encode(user_password.encode("utf-8")), "utf-8")

        return base_user

    def Main(self):
        self.session.get(self.Main_url)
        code = self.Get_code(self.Get_pic())
        base_user = self.Base_user()
        data = {
            "userAccount": "",
            "userPassword": "",
            "RANDOMCODE": code,
            "encoded": base_user
        }
        res = self.session.post(self.login_url,data=data).text

        print(res)

        return self.session # 返回session

if __name__ == '__main__':
    login = Login()
    login.Main()


