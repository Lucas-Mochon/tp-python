from database import Base
from sqlalchemy import Column, String, Integer, CheckConstraint
from sqlalchemy.orm import relationship

class Livre(Base):
    __tablename__ = "livre"

    isbn = Column(String(13), primary_key=True)
    titre = Column(String(200), nullable=False)
    editeur = Column(String(100))
    annee = Column(Integer)
    exemplaires_dispo = Column(Integer, default=1)
    emprunts = relationship("Emprunt", back_populates="livre", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('annee > 1900 AND annee < 2027'),
        CheckConstraint('exemplaires_dispo >= 0'),
    )

    def __repr__(self):
        return f"<Livre {self.isbn}: {self.titre}>"
