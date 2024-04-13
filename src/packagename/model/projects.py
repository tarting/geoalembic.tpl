from sqlalchemy import Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from geoalchemy2 import Geometry
from geoalchemy2 import WKBElement


from .base import Base

class Projects(Base):
    __tablename__ = 'projects'
    fid : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(Text, unique=True)
    geom: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=25832, spatial_index=True))

