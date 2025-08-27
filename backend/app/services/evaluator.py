from schemas.compare import CompareRequest, CompareResponse

def evaluate_definition(payload):
    # TO DO: llm logic
    if len(payload.word) % 2:
        similarity = "1.0"
    else:
        similarity = "-1.0"
    
    return CompareResponse(
        word = payload.word,
        similarity = similarity,
        explanation = f"length of word is {len(payload.word)}"
    )
