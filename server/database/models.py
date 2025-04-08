from sqlalchemy import Column, Integer, String
from server.database.db_config import Base

class CodeBlock(Base):
    __tablename__ = "code_blocks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    initial_code = Column(String, nullable=False)
    solution_code = Column(String, nullable=False)
