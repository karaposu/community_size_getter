# check_last_20_days.py
import datetime
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CommunitySize, Base

def main():
    # Visualizing step:
    #  - Imagine we're stepping into a big library (the database).
    #  - We open the "community_size" book (the table), but only want
    #    the pages from the last 20 days.
    #  - We read them and print them out.

    # 1. Create an engine to the local SQLite database
    engine = create_engine('sqlite:///community.db')

    # 2. Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()

    # 3. Calculate the date 20 days ago
    twenty_days_ago = datetime.now() - timedelta(days=20)

    # 4. Query the rows whose value_date is >= twenty_days_ago
    rows = session.query(CommunitySize).filter(
        CommunitySize.value_date >= twenty_days_ago
    ).all()

    # 5. Print out each row
    for row in rows:
        print(
            f"ID={row.id}, "
            f"value_date={row.value_date}, "
            f"fill_date={row.fill_date}, "
            f"twitter={row.twitter}, "
            f"reddit={row.reddit}, "
            f"discord={row.discord}, "
            f"telegram={row.telegram}, "
            f"price_in_usdt={row.price_in_usdt}, "
            f"marcetcap={row.marcetcap}"
        )
    
    # 6. Close the session when done
    session.close()

if __name__ == "__main__":
    main()
