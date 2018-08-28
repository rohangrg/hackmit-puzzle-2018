from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hackflix.config import DATABASE_URL

Base = declarative_base()

class GenerateVideoRequest(Base):
    __tablename__ = 'generate_video_requests'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    claimed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def __str__(self):
        return "<GenerateVideoRequest %s>" % self.username


class VerifySolutionRequest(Base):
    __tablename__ = 'verify_solution_requests'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    upload_filename = Column(String)

    claimed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    result = Column(JSON)

    def __str__(self):
        return "<VerifySolutionRequest u=%s uf=%s>" % (self.username, self.upload_filename)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
