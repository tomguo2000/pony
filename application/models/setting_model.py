from application.common.foundation import db


class SettingModel(db.Model):
    __tablename__ = 'setting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    value = db.Column(db.String(200))
    timestamp = db.Column(db.BigInteger)

    def __repr__(self):
        return '<SettingModel %r>' % (self.id)