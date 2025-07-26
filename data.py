# import kagglehub
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.docstore.document import Document

# # Download latest version
# path = kagglehub.dataset_download("rishitmurarka/gym-exercises-dataset")


# print("Path to dataset files:", path)

# gym=pd.read_csv(f"{path}/gym_exercise_dataset.csv")




# gym.drop(['Stabilizer_Muscles', 'Antagonist_Muscles', 'parent_id'], axis=1, inplace=True)
# gym.drop(['Dynamic_Stabilizer_Muscles'], axis=1, inplace=True)

# ax=plt.axes()
# sns.heatmap(gym.isna().transpose(),cbar=False,ax=ax)
# plt.xlabel("coloumn")
# plt.ylabel("missing values")
# plt.show()

# def generate_exercise_description(row):
#     return f"""
#     Exercise Name: {row['Exercise Name']}
#     Equipment: {row['Equipment']}
#     Variation: {row['Variation']}
#     Utility: {row['Utility']}
#     Mechanics: {row['Mechanics']}
#     Force: {row['Force']}
#     Preparation: {row['Preparation']}
#     Execution: {row['Execution']}
#     Difficulty (1-5): {row['Difficulty (1-5)']}
#     Main Muscle: {row['Main_muscle']}
#     Synergist Muscles: {row['Synergist_Muscles']}
#     Secondary Muscles: {row['Secondary Muscles']}
#     """


# gym['llm_entry'] = gym.apply(generate_exercise_description, axis=1)
# embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# docs = [
#     Document(page_content=row['llm_entry'], metadata={'Main_muscle': row['Main_muscle']})
#     for _, row in gym.iterrows()
# ]

# vectorstore = FAISS.from_documents(docs, embedding)
# from rapidfuzz import process

# # Your canonical list of valid muscles
# VALID_MUSCLES = ['Neck', 'Shoulder', 'Upper Arms', 'Forearm', 'Back', 'Chest', 'Hips', 'Thighs', 'Calves']

# def correct_muscle_name(user_input, valid_list=VALID_MUSCLES, threshold=80):
#     """
#     Corrects a possibly misspelled muscle name using fuzzy matching.
#     Returns the best match if above the threshold, else None.
#     """
#     match, score, _ = process.extractOne(user_input, valid_list)
#     return match if score >= threshold else None


# def parse_query(query: str):
#     import spacy
#     import re
#     nlp = spacy.load("en_core_web_sm")
    
#     # Extract number
#     number_match = re.search(r'(\d+)', query)
#     num_exercises = int(number_match.group(1)) if number_match else 5

#     # Tokenize
#     doc = nlp(query.lower())
#     found_muscles = set()

#     for token in doc:
#         # Try to correct each token to a valid muscle
#         corrected = correct_muscle_name(token.text.capitalize())
#         if corrected:
#             found_muscles.add(corrected)

#     return num_exercises, list(found_muscles)

# def get_exercises(query: str, vectorstore):
#     num_exercises, muscles = parse_query(query)
#     if not muscles:
#         return [" No valid muscles found. Try 'Chest', 'Back', etc."]

#     per_muscle = max(1, num_exercises // len(muscles))
#     all_results = []
#     seen = set()

#     for muscle in muscles:
#         results = vectorstore.similarity_search(f"exercises for {muscle}", k=per_muscle * 2)
#         count = 0
#         for res in results:
#             if res.page_content not in seen and count < per_muscle:
#                 all_results.append(res)
#                 seen.add(res.page_content)
#                 count += 1

#     # Fallback if not enough
#     if len(all_results) < num_exercises:
#         extra_needed = num_exercises - len(all_results)
#         fallback = vectorstore.similarity_search(query, k=extra_needed * 2)
#         for res in fallback:
#             if res.page_content not in seen and len(all_results) < num_exercises:
#                 all_results.append(res)
#                 seen.add(res.page_content)

#     return [doc.page_content for doc in all_results[:num_exercises]]