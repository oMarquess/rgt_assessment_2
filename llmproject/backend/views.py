from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .config import llm, OPENAI_API_KEY
from .db_config import db
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Create your views here.
# Define the QA template
# Your existing template
template = """
Provide comprehensive answers from the documents/file. Desist from answering generic questions outside the document. Site your source after each answer.
{context}
Question: {question}
Helpful Answer:
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Set up QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

class QuestionAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Ensure JSON input
        if not request.data:
            return Response({"error": "Empty request body. Expecting JSON data."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Extract question from request
        question = request.data.get("question")
        if not question:
            return Response({"error": "No question provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Process question through the chain
        try:
            result = qa_chain({"query": question})
            answer = result["result"]
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return the result
        return Response({"answer": answer}, status=status.HTTP_200_OK)


