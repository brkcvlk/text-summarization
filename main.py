from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.output_parsers.string import StrOutputParser
import mlflow

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("text_summarization")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", max_length=130, min_length=30, do_sample=False)

llm = HuggingFacePipeline(pipeline=summarizer)

prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize this text:\n{text}",
)

chain = prompt | llm | StrOutputParser()
