
class BaseHandler:
    def __init__(self, db, waiting, bot):
        self.db = db
        self.waiting = waiting
        self.bot = bot

    def handler(self):
        raise NotImplementedError
    
    def handler_waiting(self):
        raise NotImplementedError
    
    def is_text(self, value) -> bool:
        return not value.isdigit()

    def is_digit(self, value, allow_zero=True) -> bool:
        value = value.replace(',','.')
        try:
           num = float(value)
        except ValueError:
             return False
        if num < 0:
            return False
        if num == 0:
            return allow_zero
        return True
    
    def calculate_bmi(self, height, weight):
        height_m = height / 100
        bmi = weight / (height_m * height_m)
        return round(bmi, 1)
    
    def calculate_rda(self, weight):
        return {
            'min_protein': weight,
            'max_protein': 2 * weight
        }
    
    def calculate_bmr(self, weight, height, age, gender):
        if gender == 'Муж':
            return (10*weight)+(6.25*height)-(5*age)+5
        else:
            return (10*weight)+(6.25*height)-(5*age)-161