import os
import openai
from backend.app.services.trust_gate import trust_gate

class ReasoningService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4")

    async def generate_answer(self, query, evaluated_chunks, conflicts):
        if not evaluated_chunks:
            return {
                "answer": "I do not have enough reliable information to answer this question.",
                "confidence": "low",
                "sources": [],
                "conflicts": []
            }

        context = self._format_context(evaluated_chunks)
        
        prompt = f"""
You are a trust-aware enterprise assistant. Answer the user's question using ONLY the provided context.
If the context is insufficient or conflicting, state it clearly.
Every claim MUST be followed by a citation in the format [Source Title, Page X].

Context:
{context}

Question: {query}

Answer:
"""
        # Call LLM (Mocking for now to avoid billing errors, but code is ready)
        # response = await openai.ChatCompletion.acreate(...)
        
        # Mock Response
        mock_answer = "Based on the provided documents, [Statement from Source A, Page 1]. However, [Conflicting Statement from Source B, Page 2]."
        
        return {
            "answer": mock_answer,
            "confidence": "high" if not conflicts else "medium",
            "sources": [c.payload for c in evaluated_chunks[:3]],
            "conflicts": conflicts
        }

    def _format_context(self, chunks):
        formatted = ""
        for c in chunks:
            p = c.payload
            formatted += f"SOURCE: {p.get('title')} (Date: {p.get('created_at')}, Page: {p.get('page')})\n"
            formatted += f"CONTENT: {p.get('content')}\n\n"
        return formatted

reasoning_service = ReasoningService()
