from sqlalchemy.orm import Session
from ..db.base import Base, engine
from ..models.user import User
from ..models.document import Document, DocumentStatus
from ..models.role import Role
from ..models.document_shared import DocumentShared
from ..models.user_role import UserRole
from ..models.log import Log
from datetime import datetime

def create_initial_data(db: Session):
    # Check and insert initial data for User
    if db.query(User).count() == 0:
        print("Inserting initial User data...")
        user1 = User(name="Alice", email="alice@example.com", password="hashedpassword1", responsability="Admin")
        user2 = User(name="Bob", email="bob@example.com", password="hashedpassword2", responsability="User")
        db.add_all([user1, user2])
        db.commit()
        print("Initial User data inserted.")

    # Check and insert initial data for Document
    if db.query(Document).count() == 0:
        print("Inserting initial Document data...")
        doc1 = Document(name="Report.pdf", type="pdf", size="10MB", status=DocumentStatus.uploaded)
        doc2 = Document(name="Presentation.pptx", type="pptx", size="20MB", status=DocumentStatus.process)
        db.add_all([doc1, doc2])
        db.commit()
        print("Initial Document data inserted.")

    # Check and insert initial data for Role
    if db.query(Role).count() == 0:
        print("Inserting initial Role data...")
        role_admin = Role(role_name="Admin", description="Administrator role")
        role_user = Role(role_name="User", description="Standard user role")
        db.add_all([role_admin, role_user])
        db.commit()
        print("Initial Role data inserted.")

    # Example for UserRole (requires existing users and roles)
    if db.query(UserRole).count() == 0:
        print("Inserting initial UserRole data...")
        # Assuming user1 and role_admin exist from previous insertions
        alice = db.query(User).filter(User.email == "alice@example.com").first()
        admin_role = db.query(Role).filter(Role.role_name == "Admin").first()
        if alice and admin_role:
            user_role_admin = UserRole(user_id=alice.id, role_id=admin_role.id)
            db.add(user_role_admin)
            db.commit()
            print("Initial UserRole data inserted.")

    # Example for DocumentShared (requires existing documents and users)
    if db.query(DocumentShared).count() == 0:
        print("Inserting initial DocumentShared data...")
        alice = db.query(User).filter(User.email == "alice@example.com").first()
        doc1 = db.query(Document).filter(Document.name == "Report.pdf").first()
        if alice and doc1:
            doc_shared1 = DocumentShared(document_id=doc1.id, user_id=alice.id)
            db.add(doc_shared1)
            db.commit()
            print("Initial DocumentShared data inserted.")

    # Example for Log (requires existing users)
    if db.query(Log).count() == 0:
        print("Inserting initial Log data...")
        alice = db.query(User).filter(User.email == "alice@example.com").first()
        if alice:
            log1 = Log(event="LOGIN", user_id=alice.id, event_description="User logged in")
            db.add(log1)
            db.commit()
            print("Initial Log data inserted.")
