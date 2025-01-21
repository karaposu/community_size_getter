import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the model and base
from models import CommunitySize, Base

# Import your CommunitySizeGetter class
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

    # Instantiate your CommunitySizeGetter
    csg = CommunitySizeGetter(
        subreddit_name="pepecoin",
        twitter_handle="",  # or whatever handle you need
        discord_invite_link="https://discord.com/invite/6NXJt25q2J",
        telegram_channel_name="",  # or your telegram channel
        use_ssl=False,
        cert_path=None
    )

    # Fetch the sizes (returns a dict like {"subreddit_size": X, "discord_size": Y, "date": "YYYY-MM-DD"})
    results = csg.get_all()
    print("Fetched results:", results)

    # Convert results to your CommunitySize model
    # Make sure the `date` field in your CommunitySize model matches a DATE or DATETIME type
    # and you parse it appropriately:
    result_date = datetime.strptime(results["date"], "%Y-%m-%d").date()

    new_entry = CommunitySize(
        reddit=results["subreddit_size"],
        discord=results["discord_size"],
        value_date=result_date, 
        fill_date=result_date
        
    )
    
    # Add and commit
    session.add(new_entry)
    session.commit()
    print(f"Saved data to DB with ID: {new_entry.id}")

if __name__ == "__main__":
    main()
