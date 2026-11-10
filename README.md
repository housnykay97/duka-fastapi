1. When data is coming to the API it comes as JSON. Once a FastAPI Route receives that JSON it converts it to an object where a class you have previously defined has mapped every key of that json. e.g

-Define a ProductRequest class with properties matching request data: name, buying_price, selling_price, stock_quantity


-Define a ProductRequest class with properties matching request data: id, name, buying_price, selling_price, stock_quantity

pydantic changes an object to json

