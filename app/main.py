import os

from fastapi import FastAPI, UploadFile, File, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import pandas as pd

app = FastAPI()

# Configure CORS
origins = [os.getenv('ALLOWED_HOST')]

# Include CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable to store the results from the data comparison. This will represent the 'persistent store' for the results.
comparison = []

@app.post('/process_csv')
def process_csv(response: Response, files: List[UploadFile] = File(...)):
    """An endpoint to reconcile the 2 csv files.

    Args:
        response (Response): fastAPI response object 
        files (List[UploadFile]): 2 csv files to process

    Returns:
        json object: contains a sucess message and processed data on success or error message on fail
    """
    try:
        if len(files) != 2:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Please upload 2 csv files"}

        # read files
        file_1 = pd.read_csv(files[0].file, index_col=False)
        file_2 = pd.read_csv(files[1].file, index_col=False)

        # Convert the 3 columns to float type.
        file_1[['TransactionAmount', 'TransactionID', 'TransactionType']] = file_1[['TransactionAmount', 'TransactionID', 'TransactionType']].astype(float)
        file_2[['TransactionAmount', 'TransactionID', 'TransactionType']] = file_2[['TransactionAmount', 'TransactionID', 'TransactionType']].astype(float)

        # eliminate duplicates.
        file_1 = file_1.drop_duplicates(file_1.columns.difference(['TransactionID']))
        file_2 = file_2.drop_duplicates(file_2.columns.difference(['TransactionID']))

        # Merge the 2 dataframes.
        result = file_1.merge(file_2, indicator=True, how='outer')

        form = {
            "left_only": "file_1",
            "right_only": "file_2",
            "both": "both"
        }

        # Rename the _merge fields to something more understandable.
        result['_merge'] = result['_merge'].map(form).astype(str)

        # Store the results of the reconcialiation for file_1.
        file_1_result = {
            "file_name": files[0].filename,
            "total_records" : len(file_1),
            "matching": len(result.loc[lambda v: v['_merge'] == 'both']),
            "unmatched_records_length": len(result.loc[lambda v: v['_merge'] == 'file_1']),
            "unmatched_records": result.loc[lambda v: v['_merge'] == 'file_1'].to_dict('records')
        }
        
        # Store the results of the reconcialiation for file_2
        file_2_result = {
            "file_name": files[1].filename,
            "total_records" : len(file_2),
            "matching": len(result.loc[lambda v: v['_merge'] == 'both']),
            "unmatched_records_length": len(result.loc[lambda v: v['_merge'] == 'file_2']),
            "unmatched_records": result.loc[lambda v: v['_merge'] == 'file_2'].to_dict('records')
        }

        # Clear the data store when we reconcile another data set
        if len(comparison) > 0:
            comparison.clear()

        # Add our results to the datastore
        comparison.append(file_1_result)
        comparison.append(file_2_result)

        return {"message": "Files successfully compared", "result": comparison}
    except Exception:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "There is an issue with the app"}

@app.get('/comparison_results')
def get_comparison():
    """An endpoint to get the result of the comparison.

    Returns:
        json object : json object containing the processed data
    """
    return {"result": comparison}

@app.post('/clear_data')
def clear_data():
    """An endpoint to clear the persistent store.

    Returns:
        json object: a success message
    """
    comparison.clear()
    return {'message': "Data has been cleared"}