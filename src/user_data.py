# user_data.py
"""
Module defining a `User` class that can retrieve user records from MongoDB and save them to a CSV file.
"""
import csv
import os
from pymongo import MongoClient

class User:
    def __init__(self, age: int, gender: str, income: float, expenses: dict):
        """
        :param age: User age
        :param gender: User gender
        :param income: Total income
        :param expenses: Dict of expense categories and amounts
        """
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses or {}

    def to_dict(self) -> dict:
        """
        Convert User instance into a flat dict for CSV writing.
        """
        data = {'age': self.age, 'gender': self.gender, 'income': self.income}
        for cat, amt in self.expenses.items():
            data[cat] = amt
        return data

    @staticmethod
    def load_from_mongo(uri: str,
                        db_name: str = 'user_data_db',
                        collection_name: str = 'user_details') -> list:
        """
        Fetch all user documents from MongoDB and return a list of User instances.
        :param uri: MongoDB connection URI
        :param db_name: Database name
        :param collection_name: Collection name
        :return: List of User objects
        """
        client = MongoClient(uri)
        db = client[db_name]
        coll = db[collection_name]
        users = []
        for doc in coll.find({}):
            age = doc.get('age')
            gender = doc.get('gender')
            income = doc.get('income')
            expenses = doc.get('expenses', {})
            users.append(User(age=age, gender=gender, income=income, expenses=expenses))
        return users

    @staticmethod
    def save_to_csv(users: list, filename: str = None) -> str:
        """
        Save a list of User instances to a CSV file.
        :param users: List of User objects
        :param filename: CSV filename (defaults to 'user_data.csv')
        :return: Absolute path to the written CSV file
        """
        if filename is None:
            filename = 'user_data.csv'
        # Determine all fields: fixed + expense categories across users
        expense_fields = set()
        for u in users:
            expense_fields.update(u.expenses.keys())
        fieldnames = ['age', 'gender', 'income'] + sorted(expense_fields)

        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for u in users:
                writer.writerow(u.to_dict())
        return os.path.abspath(filename)
