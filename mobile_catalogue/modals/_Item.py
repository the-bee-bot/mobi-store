from modals import db
import json


class MobileItem(db.Model):
    """
        individual mobile item details
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    # title for a Mobile Item, mostly the model name
    name = db.Column(db.String(100), nullable=False)
    # URL to mobile image
    img = db.Column(db.String())
    # category that the item belongs to
    category = db.relationship('Category', backref=db.backref("items", lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, img, ctgry, user):
        self.name = name
        self.category = ctgry
        self.user = user
        self.img = img

    def to_json(self):
        """
        Args:
            sess(session.Session): a session object; used for querying

        Returns: JSON formatted string with name and its fields
        """
        return json.dumps(self.to_dict(), sort_keys=True, indent=2)

    def to_dict(self):
        """
        Args:
            sess(session.Session): a session object; used for querying

        Returns: returns a dictioanry to format JSON with name and its fields
        """
        itmjson = {}
        itmjson["item"] = self.name
        itmjson["img"] = self.img
        itmjson["username"] = self.user.name
        itmjson["fields"] = {fld.name: fld.value for fld in self.fields.all()}
        return itmjson


class ItemField(db.Model):
    """
        a single field in a Mobile Item
    """
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(300))
    # the item that this field belongs to
    item = db.relationship('MobileItem', backref=db.backref('fields', lazy='dynamic'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __init__(self, name, content, item=None):
        self.name = name
        self.value = content
        self.item = item
