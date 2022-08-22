import streamlit as st
import spacy
from annotated_text import annotated_text

@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_models():
    french_model = spacy.load("./models/fr/")
    english_model = spacy.load("./models/en/")
    models = {"en": english_model, "fr": french_model}
    return models


def process_text(doc,anonymize=False):
	tokens = []
	for token in doc:
		if token.ent_type_ == "PERSON":
			tokens.append((token.text,"PERSON","#faa"))
		elif token.ent_type_ in ["GPE","LOC"]:
			tokens.append((token.text,"LOCAITON","#fda"))
		elif token.ent_type_ == "ORG":
			tokens.append((token.text,"Orgnization","#afa"))
		else:
			tokens.append(" "+token.text+" ")
	
	if anonymize:
		anonymized_tokens = []
		for token in tokens:
			if type(token) == tuple:
				anonymized_tokens.append(("x"*len(token[0]),token[1],token[2]))
			else:
				anonymized_tokens.append(token)
		return anonymized_tokens

	return tokens


models = load_models()



selected_language = st.sidebar.selectbox("Select a Language ",options=["en","fr"])
selecte_entitites = st.sidebar.multiselect("Select the entities you want to detect",
											options=["LOC","PER","ORG"],
											default=["LOC","PER","ORG"],
										  )

selected_model = models[selected_language]

text_input = st.text_area("Type a text to anonymize")
uploaded_file = st.file_uploader("or upload a file",type=["doc","pdf","docx","txt"])

if(uploaded_file is not None):
	text_input = uploaded_file.getvalue()
	text_input = text_input.decode("utf-8")

anonymize = st.checkbox("Anonymize")

#st.markdown(f"text input : {text_input}")

doc = selected_model(text_input)
tokens = process_text(doc,anonymize=anonymize)
annotated_text(*tokens)

