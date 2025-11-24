from fastapi import FastAPI, HTTPException

app = FastAPI()

# --- Temp ---

def to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32

def to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9

# --- Vol ---

CUP_ML = 240.0

def cups_to_ml(cups: float) -> float:
    return cups * CUP_ML

def ml_to_cups(ml: float) -> float:
    return ml / CUP_ML

@app.get("/convert")
def convert(
    celsius: float | None = None,
    fahrenheit: float | None = None,
    cup: float | None = None,
    ml: float | None = None,
):
    # Get param
    params = {
        "celsius": celsius,
        "fahrenheit": fahrenheit,
        "cup": cup,
        "ml": ml,
    }
    provided = {name: value for name, value in params.items() if value is not None}

    if len(provided) == 0:
        raise HTTPException(
            status_code=400,
            detail="Provide exactly one of: celsius, fahrenheit, cup, ml.",
        )

    if len(provided) > 1:
        raise HTTPException(
            status_code=400,
            detail="Provide only one parameter at a time.",
        )

    # get param val
    input_unit, input_value = next(iter(provided.items()))

    if input_unit == "celsius":
        return {
            "category": "temperature",
            "input_unit": "celsius",
            "output_unit": "fahrenheit",
            "input_value": input_value,
            "output_value": to_fahrenheit(input_value),
        }

    if input_unit == "fahrenheit":
        return {
            "category": "temperature",
            "input_unit": "fahrenheit",
            "output_unit": "celsius",
            "input_value": input_value,
            "output_value": to_celsius(input_value),
        }

    if input_unit == "cup":
        return {
            "category": "volume",
            "input_unit": "cup",
            "output_unit": "ml",
            "input_value": input_value,
            "output_value": cups_to_ml(input_value),
        }

    return {
        "category": "volume",
        "input_unit": "ml",
        "output_unit": "cup",
        "input_value": input_value,
        "output_value": ml_to_cups(input_value),
    }


