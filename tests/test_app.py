import unittest
from modals import User, Category, MobileItem, ItemField, db
import json
import app


class SomeTestCase(unittest.TestCase):
    def setUp(self):
        with app.app.app_context():
            app.initdb()

    def tearDown(self):
        with app.app.app_context():
            app.close_db()

    def testUserTable(self):
        assert 0 == len(User.query.all())

        user1 = User("user1", "user1@mail.com")
        db.add(user1)
        db.commit()
        assert 1 == len(User.query.all())

        user2 = User("user2", "user2@mail.com")
        db.add(user2)
        db.commit()
        assert 2 == len(User.query.all())

    def testCategoryTable(self):
        assert 0 == Category.query.count()

        user2 = Category("micromax")
        db.add(user2)
        db.commit()
        assert 1 == len(Category.query.all())
        print Category.query.filter_by(name="micromax").first()

        user3 = Category("nokia")
        db.add(user3)
        db.commit()
        assert 2 == Category.query.count()

    def testMobileItemTable(self):
        self.testUserTable()
        self.testCategoryTable()
        assert 0 == len(db.query(MobileItem).all())

        ctgry1 = db.query(Category).filter_by(name="nokia").first()
        user1 = db.query(User).filter_by(name="user1").first()
        itm1 = MobileItem("Nokia 230", ctgry1, user1)
        db.add(itm1)
        db.commit()
        assert 1 == len(db.query(MobileItem).all())

        itm2 = MobileItem("Nokia 100", ctgry1, user1)
        db.add(itm2)
        db.commit()
        assert 2 == len(db.query(MobileItem).all())

    def testFieldsTable(self):
        self.testMobileItemTable()
        assert 0 == len(db.query(ItemField).all())

        itm1 = db.query(MobileItem).all()[0]  # type:MobileItem
        db.add(ItemField("OS", "Android", itm1))
        db.add(ItemField("Colour", "Android", itm1))
        db.add(ItemField("Item model number", "NOKIA 230 DUAL SIM", itm1))
        db.add(ItemField("Special features", "Dual SIM, Primary Camera, Secondary Camera", itm1))
        db.commit()

        itm2 = db.query(MobileItem).all()[1]  # type:MobileItem
        db.add(ItemField("OS", "Android", itm2))
        db.add(ItemField("Colour", "Android", itm2))
        db.add(ItemField("Item model number", "NOKIA 230 DUAL SIM", itm2))
        db.add(ItemField("Special features", "Dual SIM, Primary Camera, Secondary Camera", itm2))
        db.commit()

        assert json.loads(itm1.to_json(db)) == json.loads(
            """
            {
              "fields": {
                "Colour": "Android",
                "Item model number": "NOKIA 230 DUAL SIM",
                "OS": "Android",
                "Special features": "Dual SIM, Primary Camera, Secondary Camera"
              },
              "item": "Nokia 230"
            }
            """
        )
        assert json.loads(itm2.to_json(db)) == json.loads(
            """{
            "fields": {
            "Colour": "Android",
            "Item model number": "NOKIA 230 DUAL SIM",
            "OS": "Android",
            "Special features": "Dual SIM, Primary Camera, Secondary Camera"
            },
            "item": "Nokia 100"
            }"""
        )
        assert json.loads(itm1.category.to_json(db)) == json.loads(
            """{
  "category": "nokia",
  "items": [
    {
      "fields": {
        "Colour": "Android",
        "Item model number": "NOKIA 230 DUAL SIM",
        "OS": "Android",
        "Special features": "Dual SIM, Primary Camera, Secondary Camera"
      },
      "item": "Nokia 230"
    },
    {
      "fields": {
        "Colour": "Android",
        "Item model number": "NOKIA 230 DUAL SIM",
        "OS": "Android",
        "Special features": "Dual SIM, Primary Camera, Secondary Camera"
      },
      "item": "Nokia 100"
    }
  ]
}"""
        )


if __name__ == '__main__':
    unittest.main()
