"""Insert data into products table

Revision ID: 11c2e5b369be
Revises: 02d3a97e44a3
Create Date: 2026-11-19 21:20:53.271324

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '11c2e5b369be'
down_revision = '02d3a97e44a3'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table(
        "categories",
        column("name", sa.String(128)),
    )
    products_table = table(
        "products",
        column("name", sa.String(100)),
        column("price", sa.Float),
        column("active", sa.Boolean),
        column("category_id", sa.Integer),
    )

    op.bulk_insert(categories_table, [
        {"name": "Electronics"},
        {"name": "Books"},
        {"name": "Clothing"},
    ])

    op.bulk_insert(products_table, [
        {"name": "Laptop", "price": 1200.0, "active": True, "category_id": 1},
        {"name": "Smartphone LG", "price": 800.0, "active": True, "category_id": 1},
        {"name": "Novel", "price": 20.0, "active": True, "category_id": 2},
        {"name": "T-Shirt", "price": 25.0, "active": False, "category_id": 3},
    ])


def downgrade():
    op.execute(
        "DELETE FROM products "
        "WHERE name IN ('Laptop', 'Smartphone LG', 'Novel', 'T-Shirt')"
    )
    op.execute(
        "DELETE FROM categories "
        "WHERE name IN ('Electronics', 'Books', 'Clothing')"
    )
