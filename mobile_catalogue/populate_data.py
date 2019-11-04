from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modals import Category, db, User, ItemField, MobileItem

engine = create_engine('sqlite:///app.db', echo=True)
db.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sess = DBSession()

db.metadata.drop_all()
db.metadata.create_all(engine)

# adding users
user1 = User("user1", "user1@mail.com")
sess.add(user1)
sess.commit()
user2 = User("user2", "user2@mail.com")
sess.add(user2)
sess.commit()

# adding categories
nokia = Category("Nokia")
sess.add(nokia)
mx = Category("Micromax")
sess.add(mx)
sony = Category("Sony")
sess.add(sony)
krbm = Category("Karbonn")
sess.add(krbm)
sess.commit()

# adding mobile modals
itm1 = MobileItem("Nokia 230", nokia, user1)
sess.add(itm1)
sess.commit()

itm2 = MobileItem("Nokia 100", nokia, user1)
sess.add(itm2)
sess.commit()

# adding field to those items
sess.add(ItemField("OS", "Android", itm1))
sess.add(ItemField("Colour", "Android", itm1))
sess.add(ItemField("Item model number", "NOKIA 230 DUAL SIM", itm1))
sess.add(ItemField("Special features", "Dual SIM, Primary Camera, Secondary Camera", itm1))
sess.commit()

sess.add(ItemField("OS", "Android", itm2))
sess.add(ItemField("Colour", "Android", itm2))
sess.add(ItemField("Item model number", "NOKIA 230 DUAL SIM", itm2))
sess.add(ItemField("Special features", "Dual SIM, Primary Camera, Secondary Camera", itm2))
sess.commit()
