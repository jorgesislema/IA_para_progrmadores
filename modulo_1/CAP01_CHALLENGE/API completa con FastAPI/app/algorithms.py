# librerias necesarias 

from fastapi import APIRouter, HTTPException, Query
from app.models import Payload, BinarySearchPayload
from app.utils import bubble_sort, filter_even, sum_elements, find_max, binary_search
from app.auth import verify_token

router = APIRouter()

@router.post("/bubble-sort")
def sort_numbers(data: Payload, token: str = Query(...)):
    verify_token(token)
    return {"numbers": bubble_sort(data.numbers)}

@router.post("/filter-even")
def filter_numbers(data: Payload, token: str = Query(...)):
    verify_token(token)
    return {"even_numbers": filter_even(data.numbers)}

@router.post("/sum-elements")
def sum_numbers(data: Payload, token: str = Query(...)):
    verify_token(token)
    return {"sum": sum_elements(data.numbers)}

@router.post("/max-value")
def max_number(data: Payload, token: str = Query(...)):
    verify_token(token)
    try:
        return {"max": find_max(data.numbers)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/binary-search")
def search_number(data: BinarySearchPayload, token: str = Query(...)):
    verify_token(token)
    sorted_list = bubble_sort(data.numbers)
    index = binary_search(sorted_list, data.target)
    found = index != -1
    return {"found": found, "index": index if found else -1}
