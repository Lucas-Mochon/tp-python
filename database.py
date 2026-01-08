from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


try:
    DATABASE_URL = f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    print("Connexion à la base de données réussie")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    raise

def get_session():
    """Retourne une nouvelle session SQLAlchemy"""
    return SessionLocal()

def init_db():
    """Crée toutes les tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès")
    except Exception as e:
        print(f"Erreur création tables : {e}")
        raise
