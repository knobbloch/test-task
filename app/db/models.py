from sqlalchemy import Column,  ForeignKey, JSON,  Integer, BigInteger, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from app.db.column_annotations import (int_pk, str_nullable, str_not_nullable,
                                   float_nullable)


class OrganizationActivity(Base):
    __tablename__ = 'organization_activity'
    #id: Mapped[int_pk]
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activities.id', ondelete='CASCADE'), primary_key=True)

class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int_pk]
    name: Mapped[str_nullable]
    phone_numbers: Mapped[list] = mapped_column(JSON)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey('buildings.id'))

    building: Mapped['Building'] = relationship('Building', uselist=False, back_populates='organizations')
    activities: Mapped[list['Activity']] = relationship('Activity', uselist=True, secondary='organization_activity', back_populates='organizations')


class Building(Base):
    __tablename__ = 'buildings'

    id: Mapped[int_pk]
    address: Mapped[str_not_nullable]
    latitude: Mapped[float_nullable]
    longitude: Mapped[float_nullable]

    organizations: Mapped[list['Organization']] = relationship('Organization', uselist=True, back_populates='building')


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int_pk]
    name: Mapped[str_nullable]
    parent_id: Mapped[int] = Column(Integer, ForeignKey('activities.id'), nullable=True)

    parent: Mapped['Activity'] = relationship('Activity', uselist=False, remote_side='Activity.id', backref='children')
    organizations: Mapped[list['Organization']] = relationship('Organization', uselist=True, secondary='organization_activity', back_populates='activities')