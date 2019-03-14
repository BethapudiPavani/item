from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from university_db import University, Base, College, User
engine = create_engine('sqlite:///university.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loades into the
# database session object. Any change made against the objests in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

session = DBSession()

# Dummy User
User1 = User(
    name="Pavani",
    email="pavanikruthikaa@gmail.com",
    picture="https://pbs.twimg.com/profile_images/ "
            "2671170543/18debd694829ed78203a5a36dd364160_400x400.png")
session.add(User1)
session.commit()

# Menu(list of player) for University JNTUK

university1 = University(name="Jntuk", user_id=1)
session.add(university1)
session.commit()

# Vishnu Institute Of Technology info
college1 = College(
                   name="VIT",
                   address="Vishnupur,KovvadaRd,Kovvada,AndhraPradesh-534202",
                   founded="2008",
                   phone="08816251333",
                   place="Bhimavaram",
                   college_id=1,
                   user_id=1
                 )
session.add(college1)
session.commit()

# Sagi Ramakrishnam Raju Engineering info
college2 = College(
                   name="SRKR",
                   address="Chinnamiram, Bhimavaram, Andhra Pradesh 534204",
                   founded="1980",
                   phone="088162 23332",
                   place="Bhimavaram",
                   college_id=1,
                   user_id=1
                 )
session.add(college2)
session.commit()

# Grandhi Varalakshmi Venkata Rao Institute of Technology info
college3 = College(
                    name="GVIT",
                    address="VempaRoad, Bhimavaram,AndhraPradesh 534207",
                    founded=2008,
                    phone="088162 44919",
                    place="Bhimavaram",
                    college_id=1,
                    user_id=1
                 )
session.add(college3)
session.commit()

# Aditya Engineering College info
college4 = College(
                    name="Aditya Engineering College",
                    address="ADB Road, Aditya Nagar, Surampalem, AP-533437",
                    founded=2001,
                    phone="099498 76662",
                    place="Rajahmundry",
                    college_id=1,
                    user_id=1
                 )
session.add(college4)
session.commit()

# Rajamahendri Institute of Engineering & Technology info
college5 = College(
                    name="RIET",
                    address="Bhoopalapatnam Near, Rajahmundry, AP-533107",
                    founded=2001,
                    phone="083744 45046",
                    place="Rajahmundry",
                    college_id=1,
                    user_id=1
                 )
session.add(college5)
session.commit()

# Menu(list of university) for University jntuh
university2 = University(name="Jntuh", user_id=1)
session.add(university2)
session.commit()

# Avanthi Institute Of Engineering & Technology info
college1 = College(
                    name="AVIH",
                    address="Near Ramoji Film City, Telangana 501512",
                    founded=2014,
                    phone=" 098666 64631",
                    place="Hyderabad",
                    college_id=2,
                    user_id=1
                 )
session.add(college1)
session.commit()

#  BVRITH info
college2 = College(
                    name="BVRIT",
                    address="8-5/4 Bachupally, Rajiv Colony, Telangana-500090",
                    founded=2012,
                    phone="040 4241 7773 ",
                    place="Hyderabad",
                    college_id=2,
                    user_id=1
                 )
session.add(college2)
session.commit()

# Jawaharlal Nehru Technological University, Hyderabad info
college3 = College(
                   name="JNTUH",
                   address="Kukatpally, Hyderabad, Telangana 500085",
                   founded=1965,
                   phone="040 2315 8661",
                   place="Hyderabad",
                   college_id=2,
                   user_id=1
                 )
session.add(college3)
session.commit()

# Adam's Engineering College info
college4 = College(
                   name="Adam's Engineering College",
                   address="Palwancha, Telangana 507115",
                   founded=1998,
                   phone="087442 53001",
                   place="Hyderabad",
                   college_id=2,
                   user_id=1
                  )
session.add(college4)
session.commit()


print("List of Colleges are added!!!")
