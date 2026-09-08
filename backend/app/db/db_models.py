"""
Single-table schema for now — strains only, no brand attached.

When you're ready to distinguish "Ice Cream Cake by Brand A" from
"Ice Cream Cake by Brand B", this is where a Brand table + a strain_id/
brand_id join table comes back in (that version existed earlier — ask if
you want it restored instead of rebuilt).
"""

from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Strain(Base):
    __tablename__ = "strains"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    strain_type: Mapped[str | None] = mapped_column(String(20), nullable=True)  # indica/sativa/hybrid
    thc_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    cbd_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    terpenes: Mapped[list] = mapped_column(JSON, default=list)
    top_effects: Mapped[list] = mapped_column(JSON, default=list)
    top_flavors: Mapped[list] = mapped_column(JSON, default=list)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    source_name: Mapped[str] = mapped_column(String(40), default="manual")  # "leafly", "weedmaps", "manual"
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
