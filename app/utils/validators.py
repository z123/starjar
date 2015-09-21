from wtforms.validators import ValidationError

class Unique(object):
    def __init__(self, column, message="This element already exists."):
        self.column = column 
        self.model = column.class_

    def __call__(self, form, field):
        check = self.model.query.filter(self.column == field.data).first()
        if check:
            raise ValidationError(self.message)
