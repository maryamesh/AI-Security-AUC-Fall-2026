from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8_000)

    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "What is Compound X-104?"}]
        }
    }


class ChatResponse(BaseModel):
    response: str
    request_id: str
