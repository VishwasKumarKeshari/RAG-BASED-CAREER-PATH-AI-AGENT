import streamlit as st
import joblib
import json
from nlp_module import NLPCareerMatcher
import os
import pandas as pd


st.title("🎯 Career Compass — AI-Powered Career Path Detector")


# Load resources
try:
	with open('resources/resources.json') as f:
		resources = json.load(f)
except Exception as e:
	resources = {}
	st.warning(f"Could not load resources file: {e}")


# Load ML model (optional — may be unavailable until training is run)
ml_model = None
try:
	ml_model = joblib.load('models/career_classifier.pkl')
except Exception as e:
	st.warning(f"Could not load ML model (Structured mode disabled): {e}")


# Initialize NLP matcher
nlp_model = None
try:
	nlp_model = NLPCareerMatcher()
except Exception as e:
	nlp_model = None
	st.warning(f"Could not initialize NLP matcher: {e}")


st.sidebar.header("Enter Your Information")

mode = st.sidebar.radio("Input Mode", ["Structured", "Natural Language"])


if mode == "Structured":
	degree = st.selectbox("Degree", ["B.Tech", "B.Sc", "MCA", "MBA"])
	branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "ME", "Civil"])
	skills = st.text_input("Enter skills (comma separated)")

	if st.button("Predict Career"):
		if ml_model is None:
			st.error("ML model not available. Please run `train_model.py` to generate 'models/career_classifier.pkl' or use Natural Language mode.")
		else:
			# Build a single-row DataFrame so the saved sklearn Pipeline (ColumnTransformer)
			# can pick columns by name and apply preprocessing.
			X = pd.DataFrame([{
				'degree': degree,
				'branch': branch,
				'skills': skills
			}])
			try:
				prediction = ml_model.predict(X)
				career = prediction[0]
				st.success(f"🎓 Recommended Career: {career}")

				if career in resources:
					st.write("### 📚 Study Resources:")
					for link in resources[career]:
						st.markdown(f"- [{link['title']}]({link['url']})")
				else:
					st.info("No learning resources found for this career.")

			except Exception as e:
				st.error(f"Prediction failed: {e}.\nNote: the saved model may require preprocessing (encoders/pipeline) before it can accept raw inputs.")

else:
	text_input = st.text_area("Describe your interests and goals")
	if st.button("Find Career Path"):
		if not text_input.strip():
			st.warning("Please enter some text describing your interests/goals.")
		elif nlp_model is None:
			st.error("NLP matcher is not available (model initialization failed).")
		else:
			try:
				career, score = nlp_model.predict(text_input)
				st.success(f"✨ You seem suitable for: {career} (Confidence: {round(score,2)})")

				if career in resources:
					st.write("### 📚 Study Resources:")
					for link in resources[career]:
						st.markdown(f"- [{link['title']}]({link['url']})")
				else:
					st.info("No learning resources found for this career.")

			except Exception as e:
				st.error(f"NLP prediction failed: {e}")