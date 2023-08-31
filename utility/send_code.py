
from abc import ABC, abstractmethod

class OtpSender(ABC):
    @abstractmethod
    def send_sms(self, otp):
        pass

    def login_with_otp(self, username, otp):
        # انجام عملیات لاگین با استفاده از otp
        if self.send_sms(otp):
            print("عملیات لاگین با موفقیت انجام شد")
        else:
            print("عملیات لاگین با خطا مواجه شد")



class KavenegarSmsSender(OtpSender):
    def send_sms(self, otp):
        # ارسال پیام اس ام اس با استفاده از سرویس کاوه نگار
        print(f"پیام اس ام اس با متن {otp} از طریق کاوه نگار ارسال شد")

class SignalSmsSender(OtpSender):
    def send_sms(self, otp):
        # ارسال پیام اس ام اس با استفاده از سرویس سیگنال
        print(f"پیام اس ام اس با متن {otp} از طریق شرکت سیگنال ارسال شد")


kavenegar_sender = KavenegarSmsSender()
signal_sender = SignalSmsSender()



