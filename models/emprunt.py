from database import Base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date

class Emprunt(Base):
    __tablename__ = "emprunt"

    id_emprunt = Column(Integer, primary_key=True, autoincrement=True)
    id_etud = Column(Integer, ForeignKey("etudiant.id_etud", ondelete="RESTRICT"), nullable=False)
    isbn = Column(String(13), ForeignKey("livre.isbn", ondelete="RESTRICT"), nullable=False)
    date_emprunt = Column(Date, default=date.today, nullable=False)
    date_retour = Column(Date, nullable=True)
    amende = Column(Numeric(5, 2), default=0.0)
    etudiant = relationship("Etudiant", back_populates="emprunts")
    livre = relationship("Livre", back_populates="emprunts")

    __table_args__ = (
        CheckConstraint('amende >= 0'),
    )

    def __repr__(self):
        return f"<Emprunt {self.id_emprunt}: Étudiant {self.id_etud} - Livre {self.isbn}>"
