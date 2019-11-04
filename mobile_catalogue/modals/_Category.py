import json
from modals import db


class Category(db.Model):
    """
        Brand names
    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name

    def to_json(self):
        """
        Args:
            sess(session.Session): a session object; used for querying

        Returns: JSON formatted string for all items in a category
        """

        return json.dumps(self.to_json(), sort_keys=True, indent=2)

    def to_dict(self):
        ctgry = {}
        ctgry["id"] = self.id
        ctgry["category"] = self.name
        ctgry["items"] = [itm.to_dict() for itm in self.items.all()]
        return ctgry

    def item_count(self):
        """
        Returns(int): number of items in this category
        """
        return self.items.count()
