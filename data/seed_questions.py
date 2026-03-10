"""Seed script: inserts 50 GRE-style questions into MongoDB.

Usage:
    python -m data.seed_questions
"""

import os
import random

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

QUESTIONS = [
    # ── ALGEBRA (25 questions) ──
    # Easy (0.1-0.3) - 5 questions
    {
        "_id": "alg_1",
        "question": "Solve: x + 7 = 12",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "5",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_2",
        "question": "Solve: 3x = 21",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_3",
        "question": "If 2x + 4 = 10, find x",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "3",
        "difficulty": 0.15,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_4",
        "question": "Simplify: x + x + x",
        "options": ["3x", "x³", "x + 3", "x"],
        "correct_answer": "3x",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["simplification"],
    },
    {
        "_id": "alg_5",
        "question": "Find x: x - 5 = 8",
        "options": ["11", "12", "13", "14"],
        "correct_answer": "13",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    # Medium-Easy (0.35-0.45) - 5 questions near 0.5
    {
        "_id": "alg_6",
        "question": "Solve: 4x - 3 = 13",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "4",
        "difficulty": 0.35,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_7",
        "question": "If x = 2, what is 3x²?",
        "options": ["6", "9", "12", "18"],
        "correct_answer": "12",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "alg_8",
        "question": "Solve: x/4 = 7",
        "options": ["24", "26", "28", "30"],
        "correct_answer": "28",
        "difficulty": 0.35,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_9",
        "question": "What is the value of x if x² = 25?",
        "options": ["3 or -3", "5 or -5", "4 or -4", "6 or -6"],
        "correct_answer": "5 or -5",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["quadratic equations"],
    },
    {
        "_id": "alg_10",
        "question": "Simplify: 2(x + 3)",
        "options": ["2x + 3", "2x + 6", "x + 6", "2x + 5"],
        "correct_answer": "2x + 6",
        "difficulty": 0.45,
        "topic": "Algebra",
        "tags": ["distribution"],
    },
    # Medium (0.5-0.55) - 5 questions at/around 0.5
    {
        "_id": "alg_11",
        "question": "Simplify: (x³)(x²)",
        "options": ["x⁵", "x⁶", "x", "x⁹"],
        "correct_answer": "x⁵",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "alg_12",
        "question": "Solve: 2x + 3 = x + 7",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    {
        "_id": "alg_13",
        "question": "If f(x) = x + 2, find f(5)",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["functions"],
    },
    {
        "_id": "alg_14",
        "question": "Simplify: (4x²) / (2x)",
        "options": ["2x", "2", "x", "4x"],
        "correct_answer": "2x",
        "difficulty": 0.55,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "alg_15",
        "question": "Solve: 3(x - 2) = 12",
        "options": ["4", "5", "6", "7"],
        "correct_answer": "6",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["linear equations"],
    },
    # Medium-Hard (0.6-0.75) - 5 questions
    {
        "_id": "alg_16",
        "question": "Solve for x: |2x - 1| = 5",
        "options": ["2 or -3", "3 or -2", "3 or -3", "2 or -1"],
        "correct_answer": "3 or -2",
        "difficulty": 0.65,
        "topic": "Algebra",
        "tags": ["absolute value"],
    },
    {
        "_id": "alg_17",
        "question": "If f(x) = 2x² - x, find f(3)",
        "options": ["12", "15", "18", "21"],
        "correct_answer": "15",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["functions"],
    },
    {
        "_id": "alg_18",
        "question": "Solve: x² - 5x + 6 = 0",
        "options": ["1, 6", "2, 3", "-2, -3", "1, 5"],
        "correct_answer": "2, 3",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["quadratic equations"],
    },
    {
        "_id": "alg_19",
        "question": "Simplify: (x + 2)²",
        "options": ["x² + 2", "x² + 4", "x² + 4x + 4", "x² + 4x + 2"],
        "correct_answer": "x² + 4x + 4",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["expansion"],
    },
    {
        "_id": "alg_20",
        "question": "If x + y = 10 and x - y = 4, find x",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.75,
        "topic": "Algebra",
        "tags": ["systems"],
    },
    # Hard (0.8-1.0) - 5 questions
    {
        "_id": "alg_21",
        "question": "Solve: x² + 4x - 12 = 0",
        "options": ["2, -6", "-2, 6", "3, -4", "-3, 4"],
        "correct_answer": "2, -6",
        "difficulty": 0.85,
        "topic": "Algebra",
        "tags": ["quadratic equations"],
    },
    {
        "_id": "alg_22",
        "question": "If f(x) = x³ - 3x, find f(-2)",
        "options": ["-2", "2", "-8", "8"],
        "correct_answer": "-2",
        "difficulty": 0.9,
        "topic": "Algebra",
        "tags": ["functions"],
    },
    {
        "_id": "alg_23",
        "question": "Solve: 2^(x+1) = 8",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "2",
        "difficulty": 0.85,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "alg_24",
        "question": "Simplify: (x⁴)/(x²)",
        "options": ["x²", "x", "x⁶", "1"],
        "correct_answer": "x²",
        "difficulty": 0.8,
        "topic": "Algebra",
        "tags": ["exponents"],
    },
    {
        "_id": "alg_25",
        "question": "If x² + 6x + 9 = 0, find x",
        "options": ["-3", "3", "0", "-3, -3"],
        "correct_answer": "-3",
        "difficulty": 0.95,
        "topic": "Algebra",
        "tags": ["quadratic equations"],
    },

    # ── ARITHMETIC (25 questions) ──
    # Easy (0.1-0.3)
    {
        "_id": "arith_1",
        "question": "What is 25 + 37?",
        "options": ["52", "60", "62", "58"],
        "correct_answer": "62",
        "difficulty": 0.1,
        "topic": "Arithmetic",
        "tags": ["addition"],
    },
    {
        "_id": "arith_2",
        "question": "What is 84 - 29?",
        "options": ["53", "55", "57", "51"],
        "correct_answer": "55",
        "difficulty": 0.15,
        "topic": "Arithmetic",
        "tags": ["subtraction"],
    },
    {
        "_id": "arith_3",
        "question": "What is 12 × 7?",
        "options": ["74", "82", "84", "94"],
        "correct_answer": "84",
        "difficulty": 0.15,
        "topic": "Arithmetic",
        "tags": ["multiplication"],
    },
    {
        "_id": "arith_4",
        "question": "What is 156 ÷ 12?",
        "options": ["11", "12", "13", "14"],
        "correct_answer": "13",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["division"],
    },
    {
        "_id": "arith_5",
        "question": "What is 10% of 250?",
        "options": ["20", "25", "30", "35"],
        "correct_answer": "25",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    # Medium-Easy (0.35-0.45) - near 0.5
    {
        "_id": "arith_6",
        "question": "What is 35% of 200?",
        "options": ["60", "65", "70", "75"],
        "correct_answer": "70",
        "difficulty": 0.35,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "arith_7",
        "question": "A shirt costs $60. What is the price after a 20% discount?",
        "options": ["$40", "$42", "$48", "$52"],
        "correct_answer": "$48",
        "difficulty": 0.4,
        "topic": "Arithmetic",
        "tags": ["percentages", "discounts"],
    },
    {
        "_id": "arith_8",
        "question": "What is the ratio of 8 to 24?",
        "options": ["1:2", "1:3", "1:4", "2:3"],
        "correct_answer": "1:3",
        "difficulty": 0.4,
        "topic": "Arithmetic",
        "tags": ["ratios"],
    },
    {
        "_id": "arith_9",
        "question": "What is 3/5 as a decimal?",
        "options": ["0.5", "0.6", "0.7", "0.8"],
        "correct_answer": "0.6",
        "difficulty": 0.35,
        "topic": "Arithmetic",
        "tags": ["fractions"],
    },
    {
        "_id": "arith_10",
        "question": "If 4 workers complete a task in 6 hours, how long for 8 workers?",
        "options": ["2 hours", "3 hours", "4 hours", "5 hours"],
        "correct_answer": "3 hours",
        "difficulty": 0.45,
        "topic": "Arithmetic",
        "tags": ["work problems"],
    },
    # Medium (0.5-0.55)
    {
        "_id": "arith_11",
        "question": "What is 0.75 as a fraction in simplest form?",
        "options": ["3/4", "2/3", "3/5", "4/5"],
        "correct_answer": "3/4",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["fractions"],
    },
    {
        "_id": "arith_12",
        "question": "A car travels 240 km in 3 hours. What is its average speed?",
        "options": ["70 km/h", "75 km/h", "80 km/h", "85 km/h"],
        "correct_answer": "80 km/h",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["speed"],
    },
    {
        "_id": "arith_13",
        "question": "What is 15% of 80 plus 25% of 40?",
        "options": ["20", "22", "24", "26"],
        "correct_answer": "22",
        "difficulty": 0.55,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "arith_14",
        "question": "Find the average of 12, 18, 24, and 30.",
        "options": ["20", "21", "22", "23"],
        "correct_answer": "21",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["averages"],
    },
    {
        "_id": "arith_15",
        "question": "What is 2/3 + 1/6?",
        "options": ["5/6", "3/4", "1/2", "2/3"],
        "correct_answer": "5/6",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["fractions"],
    },
    # Medium-Hard (0.6-0.75)
    {
        "_id": "arith_16",
        "question": "A number is increased by 20% to become 72. What was the original number?",
        "options": ["54", "56", "58", "60"],
        "correct_answer": "60",
        "difficulty": 0.65,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "arith_17",
        "question": "If 40% of a number is 64, what is 60% of the same number?",
        "options": ["84", "90", "96", "102"],
        "correct_answer": "96",
        "difficulty": 0.7,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "arith_18",
        "question": "What is the compound interest on $1000 at 10% for 2 years?",
        "options": ["$200", "$210", "$220", "$250"],
        "correct_answer": "$210",
        "difficulty": 0.75,
        "topic": "Arithmetic",
        "tags": ["interest"],
    },
    {
        "_id": "arith_19",
        "question": "If a:b = 3:4 and b:c = 4:5, find a:c",
        "options": ["3:5", "4:5", "3:4", "5:3"],
        "correct_answer": "3:5",
        "difficulty": 0.7,
        "topic": "Arithmetic",
        "tags": ["ratios"],
    },
    {
        "_id": "arith_20",
        "question": "A shopkeeper sells at 20% profit. If cost is $150, what is selling price?",
        "options": ["$165", "$170", "$180", "$190"],
        "correct_answer": "$180",
        "difficulty": 0.7,
        "topic": "Arithmetic",
        "tags": ["profit"],
    },
    # Hard (0.8-1.0)
    {
        "_id": "arith_21",
        "question": "If the price increases by 25% then decreases by 20%, what is net change?",
        "options": ["+5%", "0%", "-5%", "+10%"],
        "correct_answer": "0%",
        "difficulty": 0.85,
        "topic": "Arithmetic",
        "tags": ["percentages"],
    },
    {
        "_id": "arith_22",
        "question": "A man covers 1/4 of journey at 60 km/h and remaining at 80 km/h. Average speed?",
        "options": ["65 km/h", "68 km/h", "70 km/h", "72 km/h"],
        "correct_answer": "68 km/h",
        "difficulty": 0.9,
        "topic": "Arithmetic",
        "tags": ["speed", "average"],
    },
    {
        "_id": "arith_23",
        "question": "What is the sum of first 20 natural numbers?",
        "options": ["190", "200", "210", "220"],
        "correct_answer": "210",
        "difficulty": 0.85,
        "topic": "Arithmetic",
        "tags": ["series"],
    },
    {
        "_id": "arith_24",
        "question": "If 3^x = 81, find x",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "difficulty": 0.9,
        "topic": "Arithmetic",
        "tags": ["exponents"],
    },
    {
        "_id": "arith_25",
        "question": "A sum becomes 3 times in 6 years at simple interest. Rate per annum?",
        "options": ["25%", "33.33%", "40%", "50%"],
        "correct_answer": "33.33%",
        "difficulty": 0.95,
        "topic": "Arithmetic",
        "tags": ["interest"],
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

    coll.delete_many({})
    
    inserted = 0
    for q in QUESTIONS:
        coll.insert_one(q)
        inserted += 1

    print(f"Seeding complete: {inserted} questions inserted.")
    client.close()


if __name__ == "__main__":
    seed()
