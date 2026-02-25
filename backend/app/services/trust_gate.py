from datetime import datetime, timezone
import os

RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", 0.7))
FRESHNESS_PENALTY_DAYS = int(os.getenv("FRESHNESS_PENALTY_DAYS", 365))

class TrustGate:
    def __init__(self):
        pass

    def evaluate_retrieval(self, retrieved_chunks):
        """
        Evaluates chunks based on relevance, freshness, and potential conflicts.
        """
        if not retrieved_chunks:
            return [], "Insufficient reliable information"

        # 1. Relevance already handled by VectorStore.search(score_threshold)
        
        # 2. Freshness Evaluation
        scored_chunks = self._apply_freshness_scores(retrieved_chunks)
        
        # 3. Sort by combined score
        scored_chunks.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # 4. Conflict Detection (Basic heuristic for MVP)
        conflicts = self._detect_conflicts(scored_chunks)
        
        return scored_chunks, conflicts

    def _apply_freshness_scores(self, chunks):
        now = datetime.now(timezone.utc)
        for chunk in chunks:
            payload = chunk.payload
            created_at_str = payload.get("created_at")
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                age_days = (now - created_at).days
                # Penalty based on age
                freshness_score = max(0, 1 - (age_days / (FRESHNESS_PENALTY_DAYS * 10)))
            else:
                freshness_score = 0.5 # Neutral
            
            chunk_relevance = chunk.score
            chunk.combined_score = (chunk_relevance * 0.7) + (freshness_score * 0.3)
        
        return chunks

    def _detect_conflicts(self, chunks):
        """
        MVP heuristic: If two chunks from different sources have high semantic similarity 
        but different dates, or if they contain opposing keywords.
        For MVP, we will rely on identifying high similarity between chunks with different dates.
        """
        conflicts = []
        # Simple implementation: compare top N chunks for temporal conflicts
        for i in range(len(chunks)):
            for j in range(i + 1, len(chunks)):
                c1 = chunks[i]
                c2 = chunks[j]
                
                # If they are very different dates but relevant to the same topic
                # (This is a placeholder for more advanced NLP conflict detection)
                d1 = c1.payload.get("created_at")
                d2 = c2.payload.get("created_at")
                
                if d1 and d2 and d1[:10] != d2[:10]:
                    # Potential temporal conflict if similarity is high
                    # For MVP, we flag if they both contribute significantly but come from different years
                    year1 = d1[:4]
                    year2 = d2[:4]
                    if year1 != year2:
                        conflicts.append({
                            "type": "temporal",
                            "sources": [c1.payload.get("title"), c2.payload.get("title")],
                            "description": f"Information from {year1} and {year2} might conflict."
                        })
        return conflicts

trust_gate = TrustGate()
