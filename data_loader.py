import pandas as pd
import ahocorasick
import re


def load_automaton():
    df1 = pd.read_csv("Data/skills.csv")
    df2 = pd.read_csv("Data/skillsIT.csv")

    skills = pd.concat([df1["skill"], df2["IT_skills"]])

    skills = (
        skills
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .unique()
    )


    A = ahocorasick.Automaton()

    for skill in skills:
        A.add_word(skill, skill)

    A.make_automaton()
    return A


AUTOMATON = load_automaton()
