import json

from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

from backend.products import (
    search_products,
    compare_products,
    get_product_by_name
)

client = Groq(api_key=GROQ_API_KEY)



SYSTEM_PROMPT = """
You are Sarang AI, a professional AI guitar shopping assistant.

You are NOT a general-purpose chatbot.
Your primary job is helping customers discover and
choose guitars from the Sarang guitar catalogue.

MANDATORY CATALOGUE RULES:

1. Whenever a customer asks:
   - What guitars do you have?
   - What types of guitars are available?
   - Show me your guitars.
   - Which brands do you have?
   - What products can I choose from?

   You MUST call search_guitars with all filters set to null.

2. Whenever a customer asks for guitars within a budget,
   you MUST use search_guitars.

3. Whenever a customer asks for recommendations,
   use recommend_guitars.

4. Whenever a customer compares two models,
   use compare_guitars.

5. Never invent products, prices or specifications.
   Only use information returned by catalogue tools.

6. Clearly identify prices and availability as
   illustrative demonstration data, not real inventory.

7. If no products match, tell the customer honestly.

8. Explain guitar terminology and general guitar knowledge
   without using catalogue tools when appropriate.

RESPONSE STYLE:

- Friendly and conversational.
- Professional music-store personality.
- Simple explanations.
- Use bullet points when listing guitars.
- Highlight relevant guitar models and their prices.
- Ask useful follow-up questions.
"""



# Tools available to the AI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_guitars",
            "description": "Search the guitar catalogue using brand, category and price filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "brand": {"type": ["string", "null"]},
                    "category": {
                        "type": ["string", "null"],
                        "enum": [
                            "acoustic",
                            "classical",
                            "electric",
                            "bass",
                            None
                        ]
                    },
                    "min_price": {"type": ["integer", "null"]},
                    "max_price": {"type": ["integer", "null"]}
                },
                "required": [
                    "brand",
                    "category",
                    "min_price",
                    "max_price"
                ],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_guitars",
            "description": "Recommend guitars according to experience, category and budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "experience": {
                        "type": ["string", "null"],
                        "enum": ["beginner", "intermediate", "null"]
                    },
                    "category": {
                        "type": ["string", "null"],
                        "enum": [
                            "acoustic",
                            "classical",
                            "electric",
                            "bass",
                            None
                        ]
                    },
                    "max_budget": {"type": ["integer", "null"]}
                },
                "required": [
                    "experience",
                    "category",
                    "max_budget"
                ],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_guitars",
            "description": "Compare two guitar models from the catalogue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_a": {"type": "string"},
                    "model_b": {"type": "string"}
                },
                "required": ["model_a", "model_b"],
                "additionalProperties": False
            }
        }
    }
]


# Validate and execute only approved functions
def execute_tool(name, arguments):

    if not isinstance(arguments, dict):
        return {"error": "Invalid tool arguments."}

    try:

        if name == "search_guitars":

            allowed = {"brand", "category", "min_price", "max_price"}

            if set(arguments) != allowed:
                return {"error": "Invalid search parameters."}

            brand = arguments["brand"]
            category = arguments["category"]
            min_price = arguments["min_price"]
            max_price = arguments["max_price"]

            if brand is not None and (
                not isinstance(brand, str) or len(brand) > 50
            ):
                return {"error": "Invalid brand."}

            if category is not None and category not in [
                "acoustic", "classical", "electric", "bass"
            ]:
                return {"error": "Invalid category."}

            for price in [min_price, max_price]:
                if price is not None and (
                    type(price) is not int or price < 0 or price > 1000000
                ):
                    return {"error": "Invalid price."}

            if (
                min_price is not None
                and max_price is not None
                and min_price > max_price
            ):
                return {"error": "Minimum price exceeds maximum price."}

            return search_products(
                brand=brand,
                category=category,
                min_price=min_price,
                max_price=max_price
            )

        elif name == "recommend_guitars":

            if set(arguments) != {
                "experience", "category", "max_budget"
            }:
                return {"error": "Invalid recommendation parameters."}

            experience = arguments["experience"]
            category = arguments["category"]
            budget = arguments["max_budget"]

            if experience not in [None, "beginner", "intermediate"]:
                return {"error": "Invalid experience level."}

            if category not in [
                None, "acoustic", "classical", "electric", "bass"
            ]:
                return {"error": "Invalid category."}

            if budget is not None and (
                type(budget) is not int or budget < 0 or budget > 1000000
            ):
                return {"error": "Invalid budget."}

            products = search_products(
                category=category,
                max_price=budget
            )

            if experience:
                products = [
                    guitar for guitar in products
                    if guitar["experience"] == experience
                ]

            return products

        elif name == "compare_guitars":

            if set(arguments) != {"model_a", "model_b"}:
                return {"error": "Invalid comparison parameters."}

            model_a = arguments["model_a"]
            model_b = arguments["model_b"]

            if not all(
                isinstance(model, str) and len(model) <= 100
                for model in [model_a, model_b]
            ):
                return {"error": "Invalid model names."}

            result = compare_products(model_a, model_b)

            if not result:
                return {"error": "One or both guitar models were not found."}

            return result

        return {"error": "Unknown tool."}

    except Exception:
        return {"error": "Unable to retrieve catalogue information."}


# Main AI function
def get_ai_response(user_message, conversation_history=None):

    if not isinstance(user_message, str) or not user_message.strip():
        return "Please enter a message."

    if len(user_message) > 4000:
        return "Please keep your message under 4000 characters."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add recent conversation context
    if conversation_history:
        for item in conversation_history[-10:]:

            if (
                isinstance(item, dict)
                and item.get("role") in ["user", "assistant"]
                and isinstance(item.get("content"), str)
            ):
                messages.append({
                    "role": item["role"],
                    "content": item["content"][:4000]
                })

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        # Allow a maximum of three tool execution rounds
        for _ in range(3):

            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.4,
                max_completion_tokens=1500
            )

            message = response.choices[0].message

            if not message.tool_calls:

                return message.content or (
                    "I couldn't generate a response. Please try again."
                )

            messages.append(message.model_dump(exclude_none=True))

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except (json.JSONDecodeError, TypeError):
                    arguments = None

                result = execute_tool(tool_name, arguments)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str
                    )
                })

        return "I couldn't complete that product search. Please try again."

    except Exception as error:

        print("Groq API error:", error)

        return (
            "I'm having trouble connecting right now. "
            "Please try again in a moment."
        )
