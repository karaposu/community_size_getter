import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the Base and the CommunitySize model from your models module
from models import Base, CommunitySize

def main():
    # Build the path to your SQLite database
    base_dir = os.path.dirname(__file__)
    # main_db_path = os.path.join(base_dir, "..", "data", "community.db")
    main_db_path = os.path.join(base_dir, "community.db")
    main_db_path = os.path.abspath(main_db_path)
    
    # Create a SQLite connection string
    main_db_url = f"sqlite:///{main_db_path}"
    
    # Create an engine for SQLite
    engine = create_engine(main_db_url, echo=True)
    
    # Create all tables defined by the Base (includes CommunitySize)
    Base.metadata.create_all(engine)
    
    print(f"Database created (or found) at: {main_db_path}")
    print("community_size table created successfully!")

if __name__ == "__main__":
    main()
