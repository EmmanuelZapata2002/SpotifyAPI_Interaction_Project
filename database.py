from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


# Define tables
class ArtistQuery(Base):
    __tablename__ = 'artist_queries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String, nullable=False)
    query_type = Column(String, nullable=False)


class ArtistData(Base):
    __tablename__ = 'artist_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    genres = Column(String)


class ArtistCoverPhotoLinks(Base):
    __tablename__ = 'artist_cover_photo_links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String, nullable=False)
    cover_photo_link = Column(String, nullable=False)




# Setup database
def get_database_session(db_url="sqlite:///spotify_queries.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()
