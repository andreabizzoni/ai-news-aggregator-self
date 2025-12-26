from repository import Repository


def init_db():
    """Create all database tables."""
    repository = Repository()
    repository.create_tables()


if __name__ == "__main__":
    init_db()
