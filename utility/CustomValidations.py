from datetime import datetime


class CustomValidations:
    def validate_string(self, value, min_length=3, max_length=75):
        if not isinstance(value, str):
            return False

        length = len(value)
        if length < min_length or length > max_length:
            return False

        return True

    def validate_descriptions(self, value):
        if not isinstance(value, str):
            return False
        return True
    def validate_bool(self, value):
        try:
            if bool(value):
                return True
        except ValueError as e:
            return False

    def validate_datetime(self, date_string, date_format="%Y-%m-%d %H:%M"):
        try:
            datetime.strptime(str(date_string), date_format)
            return True
        except ValueError as e:
            raise ValueError(e)
            return False

    def validate_int(self, value):
        try:
            price = int(value)
            if price >= 0:
                return True
            else:
                return False
        except ValueError:
            return False


customvalidations = CustomValidations()
