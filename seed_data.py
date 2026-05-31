from app import app
from models.models import (
    db,
    TechnicalQuestion
)


with app.app_context():

    # Clear old records to allow complete re-seeding
    db.session.query(TechnicalQuestion).delete()
    db.session.commit()

    # =========================================
    # TECHNICAL QUESTIONS
    # =========================================

    questions = [
        # DSA
        TechnicalQuestion(
            topic="DSA",
            question="What is a Stack?",
            answer="A Stack is a linear data structure that follows LIFO (Last In First Out).",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="DSA",
            question="What is a Queue?",
            answer="A Queue is a linear data structure that follows FIFO (First In First Out).",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="DSA",
            question="What is Binary Search?",
            answer="Binary Search is a searching algorithm that works on sorted arrays with O(log n) complexity.",
            difficulty="Medium"
        ),

        # DBMS
        TechnicalQuestion(
            topic="DBMS",
            question="What is Normalization?",
            answer="Normalization is the process of organizing data to reduce redundancy and improve consistency.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="DBMS",
            question="What is a Primary Key?",
            answer="A Primary Key uniquely identifies each record in a table.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="DBMS",
            question="What is a Foreign Key?",
            answer="A Foreign Key establishes a relationship between two tables.",
            difficulty="Easy"
        ),

        # OS
        TechnicalQuestion(
            topic="OS",
            question="What is a Process?",
            answer="A Process is a program in execution with its own memory space.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="OS",
            question="What is a Thread?",
            answer="A Thread is the smallest unit of execution within a process sharing process resources.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="OS",
            question="What is Deadlock?",
            answer="Deadlock occurs when processes wait indefinitely for resources held by each other.",
            difficulty="Medium"
        ),

        # CN
        TechnicalQuestion(
            topic="CN",
            question="What is an IP Address?",
            answer="An IP Address uniquely identifies a device on a network.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="CN",
            question="What is DNS?",
            answer="DNS translates human-readable domain names into IP addresses.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="CN",
            question="What is HTTP?",
            answer="HTTP is the protocol used for communication between web browsers and servers.",
            difficulty="Easy"
        ),

        # OOP
        TechnicalQuestion(
            topic="OOP",
            question="What is Encapsulation?",
            answer="Encapsulation binds data and methods together and restricts direct access.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="OOP",
            question="What is Inheritance?",
            answer="Inheritance allows one class to acquire properties and methods of another class.",
            difficulty="Easy"
        ),
        TechnicalQuestion(
            topic="OOP",
            question="What is Polymorphism?",
            answer="Polymorphism allows the same interface to be used for different implementations.",
            difficulty="Medium"
        )
    ]

    db.session.add_all(questions)
    print("Technical Questions Added")

    db.session.commit()
    print("Database Seeded Successfully")