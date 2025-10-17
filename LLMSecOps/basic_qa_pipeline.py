from transformers import pipeline

# references
# https://huggingface.co/docs/transformers/en/main_classes/pipelines

# initialize a question-answering pipeline with a pre-trained model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# define your context and question
context = "Hugging Face is a technology company that provides open-source NLP libraries and tools for natural language processing. They have created the transformers library which is widely used for machine learning models. The company focuses on democratizing AI through open source contributions."
question = "What does Hugging Face provide?"

# let the pipeline find the best answer based on the context provided
answer = qa_pipeline(question=question, context=context)
print(f"Question: {question}")
print(f"Answer: {answer['answer']}")
print(f"Confidence: {answer['score']:.4f}")