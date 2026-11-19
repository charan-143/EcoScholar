"""Initial EcoScholar schema: courses, quiz attempts and users."""
from alembic import op
import sqlalchemy as sa
revision="0001_initial"
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.create_table("courses",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("slug",sa.String(length=80),nullable=False),
        sa.Column("title",sa.String(length=180),nullable=False),
        sa.Column("category",sa.String(length=80),nullable=False),
        sa.Column("level",sa.String(length=40),nullable=False),
        sa.Column("duration",sa.String(length=40),nullable=False),
        sa.Column("description",sa.Text(),nullable=False),
        sa.Column("content",sa.Text(),nullable=False))
    op.create_index("ix_courses_slug","courses",["slug"],unique=True)
    op.create_table("users",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("email",sa.String(length=320),nullable=False),
        sa.Column("display_name",sa.String(length=120),nullable=False),
        sa.Column("password_hash",sa.String(length=255),nullable=False),
        sa.Column("role",sa.String(length=20),nullable=False,server_default="learner"),
        sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.text("CURRENT_TIMESTAMP")))
    op.create_index("ix_users_email","users",["email"],unique=True)
    op.create_table("quiz_attempts",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("learner_id",sa.String(length=80),nullable=False,server_default="demo-learner"),
        sa.Column("course_slug",sa.String(length=80),nullable=False),
        sa.Column("score",sa.Float(),nullable=False),
        sa.Column("total",sa.Integer(),nullable=False),
        sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.text("CURRENT_TIMESTAMP")))
    op.create_index("ix_quiz_attempts_learner_id","quiz_attempts",["learner_id"])
    op.create_index("ix_quiz_attempts_course_slug","quiz_attempts",["course_slug"])

def downgrade():
    op.drop_index("ix_quiz_attempts_course_slug",table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_learner_id",table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
    op.drop_index("ix_users_email",table_name="users")
    op.drop_table("users")
    op.drop_index("ix_courses_slug",table_name="courses")
    op.drop_table("courses")
