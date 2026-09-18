"""
Single-table schema for now — strains only, no brand attached.

When you're ready to distinguish "Ice Cream Cake by Brand A" from
"Ice Cream Cake by Brand B", this is where a Brand table + a strain_id/
brand_id join table comes back in (that version existed earlier — ask if
you want it restored instead of rebuilt).
"""

from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Strain(Base):
    __tablename__ = "strains"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    strain_type: Mapped[str | None] = mapped_column(String(20), nullable=True)  # indica/sativa/hybrid
    genetics: Mapped[str | None] = mapped_column(Text,nullable=True)
    profiles: Mapped[list["StrainProfile"]] = relationship(
        back_populates="strain",
        cascade="all, delete-orphan"
    )


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    profiles: Mapped[list["StrainProfile"]] = relationship(
        back_populates="source"
    )


class StrainProfile(Base):
    __tablename__ = "strain_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    strain_id: Mapped[int] = mapped_column(ForeignKey("strains.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    terpenes: Mapped[list] = mapped_column(JSON, default=list)
    top_effects: Mapped[list] = mapped_column(JSON, default=list)
    top_flavors: Mapped[list] = mapped_column(JSON, default=list)
    cannabinoids: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    raw_data: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )
    strain: Mapped["Strain"] = relationship(
        back_populates="profiles"
    )
    source: Mapped["Source"] = relationship(
        back_populates="profiles"
    )
