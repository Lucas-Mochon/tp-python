from database import Base
from sqlalchemy import Column, Integer, String, Date, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date

class Etudiant(Base):
    __tablename__ = "etudiant"

    id_etud = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_inscription = Column(Date, default=date.today)
    solde_amende = Column(Numeric(5, 2), default=0.0)
    emprunts = relationship("Emprunt", back_populates="etudiant", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('solde_amende >= 0'),
    )

    def __repr__(self):
        return f"<Etudiant {self.id_etud}: {self.prenom} {self.nom}>"
