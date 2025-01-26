import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the model and base
from models import CommunitySize, Base
from community_size_getter import CommunitySizeGetter

def main():
    # Build the same SQLite DB path as in create_community_size_db.py
    base_dir = os.path.dirname(__file__)
    data_dir=base_dir 
    # data_dir = os.path.join(base_dir, "..", "data")
    # data_dir = os.path.join(base_dir)
    os.makedirs(data_dir, exist_ok=True)

    main_db_path = os.path.join(data_dir, "community.db")
    main_db_path = os.path.abspath(main_db_path)

    # Create the SQLite connection
    main_db_url = f"sqlite:///{main_db_path}"
    engine = create_engine(main_db_url, echo=True)

    # Create a Session
    Session = sessionmaker(bind=engine)
    session = Session()


    print(f"session created")

    # Instantiate your CommunitySizeGetter
    csg = CommunitySizeGetter(
        subreddit_name="pepecoin",
        twitter_handle="",  # or whatever handle you need
        discord_invite_link="https://discord.com/invite/6NXJt25q2J",
        telegram_channel_link="https://t.me/PepecoinGroup", 
        use_ssl=False,
        cert_path=None
    )

    print(f"csg created")


    # Fetch the sizes (returns a dict like {"subreddit_size": X, "discord_size": Y, "date": "YYYY-MM-DD"})
    results = csg.get_all()
    print("Fetched results:", results)

    # Convert results to your CommunitySize model
    # Make sure the `date` field in your CommunitySize model matches a DATE or DATETIME type
    # and you parse it appropriately:
    result_date = datetime.strptime(results["date"], "%Y-%m-%d").date()


    # Check if there's already an entry in the DB for this date
    existing_entry = session.query(CommunitySize).filter_by(value_date=result_date).one_or_none()
    
    if existing_entry:
        # Update the existing record
        existing_entry.reddit = results["subreddit_size"]
        existing_entry.discord = results["discord_size"]
        existing_entry.telegram = results["telegram_size"]
        existing_entry.fill_date = result_date  # or datetime.now().date(), depending on your logic

        session.commit()
        print(f"Updated data for date {result_date} (ID: {existing_entry.id})")
    else:
        # Create a new entry
        new_entry = CommunitySize(
            reddit=results["subreddit_size"],
            discord=results["discord_size"],
            telegram=results["telegram_size"],
            value_date=result_date, 
            fill_date=result_date
        )
        
        session.add(new_entry)
        session.commit()
        print(f"Saved new data to DB with ID: {new_entry.id} for date {result_date}")


    
  

if __name__ == "__main__":
    main()
