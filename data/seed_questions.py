"""Seed script: inserts 20+ GRE-style questions into MongoDB.

Usage:
    python -m data.seed_questions
"""

import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

QUESTIONS = [
    # ── Algebra (6 questions) ──
    {
        "_id": "q1",
        "question": "Solve: 2x + 5 = 11",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "3",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "q2",
        "question": "If 3(x − 2) = 12, what is x?",
        "options": ["4", "5", "6", "7"],
        "correct_answer": "6",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "q3",
        "question": "What is the value of x if x² − 9 = 0?",
        "options": ["±2", "±3", "±4", "±9"],
        "correct_answer": "±3",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["quadratic equations"],
    },
    {
        "_id": "q4",
        "question": "Simplify: (2x³)(3x²)",
        "options": ["5x⁵", "6x⁵", "6x⁶", "5x⁶"],
        "correct_answer": "6x⁵",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "q5",
        "question": "Solve for x: |2x − 3| = 7",
        "options": ["5 or −2", "5 or 2", "−5 or 2", "−5 or −2"],
        "correct_answer": "5 or −2",
        "difficulty": 0.65,
        "topic": "Algebra",
        "tags": ["absolute value"],
    },
    {
        "_id": "q6",
        "question": "If f(x) = 2x² − 3x + 1, what is f(3)?",
        "options": ["8", "10", "12", "14"],
        "correct_answer": "10",
        "difficulty": 0.55,
        "topic": "Algebra",
        "tags": ["functions"],
    },
    # ── Arithmetic (4 questions) ──
    {
        "_id": "q7",
        "question": "What is 15% of 240?",
        "options": ["30", "34", "36", "40"],
        "correct_answer": "36",
        "difficulty": 0.15,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "q8",
        "question": "A shirt costs $80 after a 20% discount. What was the original price?",
        "options": ["$90", "$96", "$100", "$110"],
        "correct_answer": "$100",
        "difficulty": 0.35,
        "topic": "Arithmetic",
        "tags": ["percentages", "word problems"],
    },
    {
        "_id": "q9",
        "question": "What is the ratio of 2 hours to 45 minutes?",
        "options": ["4:3", "8:3", "3:8", "2:1"],
        "correct_answer": "8:3",
        "difficulty": 0.3,
        "topic": "Arithmetic",
        "tags": ["ratios"],
    },
    {
        "_id": "q10",
        "question": "If a train travels 360 km in 4 hours, what is its speed in km/h?",
        "options": ["80", "85", "90", "95"],
        "correct_answer": "90",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["speed"],
    },
    # ── Geometry (4 questions) ──
    {
        "_id": "q11",
        "question": "What is the area of a triangle with base 10 and height 6?",
        "options": ["25", "28", "30", "60"],
        "correct_answer": "30",
        "difficulty": 0.2,
        "topic": "Geometry",
        "tags": ["area", "triangles"],
    },
    {
        "_id": "q12",
        "question": "A circle has a radius of 7 cm. What is its circumference? (Use π ≈ 22/7)",
        "options": ["42 cm", "44 cm", "48 cm", "50 cm"],
        "correct_answer": "44 cm",
        "difficulty": 0.35,
        "topic": "Geometry",
        "tags": ["circles"],
    },
    {
        "_id": "q13",
        "question": "In a right triangle, if two legs are 3 and 4, what is the hypotenuse?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "5",
        "difficulty": 0.3,
        "topic": "Geometry",
        "tags": ["pythagorean theorem"],
    },
    {
        "_id": "q14",
        "question": "What is the volume of a cylinder with radius 3 and height 10? (Use π ≈ 3.14)",
        "options": ["251.2", "267.3", "282.6", "314.0"],
        "correct_answer": "282.6",
        "difficulty": 0.6,
        "topic": "Geometry",
        "tags": ["volume", "cylinders"],
    },
    # ── Probability & Statistics (3 questions) ──
    {
        "_id": "q15",
        "question": "A bag has 3 red, 4 blue, and 5 green balls. What is the probability of picking a blue ball?",
        "options": ["1/4", "1/3", "4/12", "5/12"],
        "correct_answer": "1/3",
        "difficulty": 0.3,
        "topic": "Probability",
        "tags": ["basic probability"],
    },
    {
        "_id": "q16",
        "question": "Two dice are rolled. What is the probability the sum is 7?",
        "options": ["1/6", "1/9", "1/12", "5/36"],
        "correct_answer": "1/6",
        "difficulty": 0.55,
        "topic": "Probability",
        "tags": ["dice", "combinations"],
    },
    {
        "_id": "q17",
        "question": "What is the median of the set {3, 7, 9, 15, 21}?",
        "options": ["7", "9", "11", "15"],
        "correct_answer": "9",
        "difficulty": 0.25,
        "topic": "Probability",
        "tags": ["statistics", "median"],
    },
    # ── Number Properties (3 questions) ──
    {
        "_id": "q18",
        "question": "How many prime numbers are between 1 and 20?",
        "options": ["6", "7", "8", "9"],
        "correct_answer": "8",
        "difficulty": 0.35,
        "topic": "Number Properties",
        "tags": ["primes"],
    },
    {
        "_id": "q19",
        "question": "What is the greatest common divisor (GCD) of 36 and 48?",
        "options": ["6", "8", "12", "18"],
        "correct_answer": "12",
        "difficulty": 0.4,
        "topic": "Number Properties",
        "tags": ["GCD"],
    },
    {
        "_id": "q20",
        "question": "What is the remainder when 2^10 is divided by 7?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "2",
        "difficulty": 0.75,
        "topic": "Number Properties",
        "tags": ["modular arithmetic"],
    },
    # ── Higher difficulty (2 bonus questions) ──
    {
        "_id": "q21",
        "question": "If the sum of the interior angles of a polygon is 1440°, how many sides does it have?",
        "options": ["8", "9", "10", "12"],
        "correct_answer": "10",
        "difficulty": 0.7,
        "topic": "Geometry",
        "tags": ["polygons"],
    },
    {
        "_id": "q22",
        "question": "A group of 5 people is to be seated in a row. How many distinct arrangements are possible?",
        "options": ["60", "100", "120", "150"],
        "correct_answer": "120",
        "difficulty": 0.8,
        "topic": "Probability",
        "tags": ["permutations"],
    },
]


def seed():
    uri = os.getenv("MONGO_URI", "")
    if not uri:
        print("ERROR: MONGO_URI not set in .env")
        return

    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client["adaptive_engine"]
    coll = db["questions"]

    inserted = 0
    skipped = 0
    for q in QUESTIONS:
        existing = coll.find_one({"_id": q["_id"]})
        if existing:
            skipped += 1
        else:
            coll.insert_one(q)
            inserted += 1

    print(f"Seeding complete: {inserted} inserted, {skipped} skipped (already exist).")
    client.close()


if __name__ == "__main__":
    seed()
