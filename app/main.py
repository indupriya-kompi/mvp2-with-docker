# """
# Version 1.2
# """
# from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
# from fastapi.responses import JSONResponse
# from zipfile import ZipFile, BadZipFile
# from io import BytesIO
# import os
# import pandas as pd
# import time
# from google.cloud import storage

# app = FastAPI()

# CSV_OUTPUT_DIR = "converted_csvs"
# os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)

# # GCS bucket name
# GCS_BUCKET_NAME = "featurebox-ai-uploads"

# def upload_to_gcs_stream(file_obj, destination_blob_name: str):
#     print(f"Streaming to GCS: {destination_blob_name}...")
#     client = storage.Client()
#     bucket = client.bucket(GCS_BUCKET_NAME)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_file(file_obj, rewind=True)
#     print("ZIP uploaded to GCS.")
#     return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

# def download_from_gcs(blob_name: str) -> BytesIO:
#     client = storage.Client()
#     bucket = client.bucket(GCS_BUCKET_NAME)
#     blob = bucket.blob(blob_name)
#     data = blob.download_as_bytes()
#     return BytesIO(data)

# def process_zip_from_gcs(blob_name: str):
#     print(f"Processing ZIP from GCS: {blob_name}")
#     start_time = time.time()
#     try:
#         zip_data = download_from_gcs(blob_name)
#         with ZipFile(zip_data) as zip_ref:
#             file_list = [f for f in zip_ref.namelist() if not (f.startswith("__MACOSX/") or f.endswith(".DS_Store"))]
#             excel_files = [f for f in file_list if f.lower().endswith((".xls", ".xlsx"))]
#             file_count = len(excel_files)

#             for excel_file in excel_files:
#                 with zip_ref.open(excel_file) as excel_fp:
#                     df = pd.read_excel(BytesIO(excel_fp.read()))
#                     base_name = os.path.splitext(os.path.basename(excel_file))[0]
#                     csv_path = os.path.join(CSV_OUTPUT_DIR, f"{base_name}.csv")
#                     df.to_csv(csv_path, index=False)

#                     # Upload CSV to GCS
#                     gcs_path = f"converted_csvs/{base_name}.csv"
#                     client = storage.Client()
#                     bucket = client.bucket(GCS_BUCKET_NAME)
#                     blob = bucket.blob(gcs_path)
#                     blob.upload_from_filename(csv_path)
#                     print(f"CSV uploaded: {gcs_path}")

#         elapsed = round(time.time() - start_time, 2)
#         print(f"✅ Successfully processed all {file_count} Excel files in {elapsed} seconds.")

#     except BadZipFile:
#         print("Invalid or corrupt ZIP file.")
#     except Exception as e:
#         print(f"Error processing ZIP from GCS: {e}")

# @app.post("/upload/")
# async def upload_zip(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
#     if not file.filename.endswith(".zip"):
#         raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")

#     try:
#         zip_blob_name = f"uploaded_zips/{file.filename}"

#         # Upload ZIP directly to GCS from stream
#         zip_file_obj = await file.read()
#         zip_stream = BytesIO(zip_file_obj)
#         upload_to_gcs_stream(zip_stream, zip_blob_name)

#         # Schedule processing of the ZIP from GCS
#         background_tasks.add_task(process_zip_from_gcs, zip_blob_name)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload or processing failed: {str(e)}")

#     return JSONResponse(content={
#         "status": "processing",
#         "filename": file.filename,
#         "message": "ZIP uploaded to GCS. Processing and conversion will continue in the background."
#     })


# """
# Version 1.1
# """

# from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
# from fastapi.responses import JSONResponse
# from zipfile import ZipFile, BadZipFile
# from io import BytesIO
# import os
# import pandas as pd
# import time

# from google.cloud import storage

# app = FastAPI()

# CSV_OUTPUT_DIR = "converted_csvs"
# os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)

# # GCS bucket name
# GCS_BUCKET_NAME = "featurebox-ai-uploads"

# def upload_to_gcs(local_file_path: str, destination_blob_name: str):
#     print(f"Uploading {local_file_path} to {destination_blob_name}...")
#     client = storage.Client()
#     bucket = client.bucket(GCS_BUCKET_NAME)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_filename(local_file_path)
#     print("Upload complete.")
#     return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"


# def process_zip_file(zip_file_path: str):
#     print(f"Processing ZIP")
#     start_time = time.time()
#     try:
#         with ZipFile(zip_file_path) as zip_ref:
#             file_list = [f for f in zip_ref.namelist() if not (f.startswith("__MACOSX/") or f.endswith(".DS_Store"))]
#             excel_files = [f for f in file_list if f.lower().endswith((".xls", ".xlsx"))]
#             file_count = len(excel_files) 

#             for excel_file in excel_files:
#                 with zip_ref.open(excel_file) as excel_fp:
#                     df = pd.read_excel(BytesIO(excel_fp.read()))
#                     base_name = os.path.splitext(os.path.basename(excel_file))[0]
#                     csv_path = os.path.join(CSV_OUTPUT_DIR, f"{base_name}.csv")
#                     df.to_csv(csv_path, index=False)

#                     # Upload to GCS
#                     gcs_path = f"converted_csvs/{base_name}.csv"
#                     upload_to_gcs(csv_path, gcs_path)

#             print(f"Successfully processed all {file_count} from ZIP")

#         elapsed = round(time.time() - start_time, 2)
#         print(f"Successfully Completed processing in {elapsed} seconds")

#     except BadZipFile:
#         print("Invalid or corrupt ZIP file.")
#     except Exception as e:
#         print(f"Error processing files: {str(e)}")
#     finally:
#         # Clean up local ZIP file
#         if os.path.exists(zip_file_path):
#             os.remove(zip_file_path)

# @app.post("/upload/")
# async def upload_zip(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
#     if not file.filename.endswith(".zip"):
#         raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")

#     try:
#         contents = await file.read()
#         zip_path = f"/tmp/{file.filename}"
#         with open(zip_path, "wb") as f:
#             f.write(contents)

#         # Add background task to process the zip
#         background_tasks.add_task(process_zip_file, zip_path)

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

#     return JSONResponse(content={
#         "status": "processing",
#         "filename": file.filename,
#         "message": "ZIP file received. Processing and GCS upload will continue in the background."
#     })

"""
Version 1.0
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os
import pandas as pd
import time
from google.cloud import storage 

app = FastAPI()

CSV_OUTPUT_DIR = "converted_csvs"
os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)

# GCS bucket name
GCS_BUCKET_NAME = "featurebox-ai-uploads"

def upload_to_gcs(local_file_path: str, destination_blob_name: str):
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

@app.post("/upload/")
async def upload_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")
    start_time = time.time()
    try:
        contents = await file.read()  # Read uploaded file contents fully
        with ZipFile(BytesIO(contents)) as zip_ref:
            file_list = [f for f in zip_ref.namelist() if not (f.startswith("__MACOSX/") or f.endswith(".DS_Store"))]
            excel_files = [f for f in file_list if f.lower().endswith((".xls", ".xlsx"))]
            file_count = len(excel_files) 

            saved_files = []
            gcs_uris = []

            for excel_file in excel_files:
                with zip_ref.open(excel_file) as excel_fp:
                    df = pd.read_excel(BytesIO(excel_fp.read()))
                    base_name = os.path.splitext(os.path.basename(excel_file))[0]
                    csv_path = os.path.join(CSV_OUTPUT_DIR, f"{base_name}.csv")
                    df.to_csv(csv_path, index=False)
                    saved_files.append(csv_path)

                    # Upload to GCS
                    gcs_path = f"converted_csvs/{base_name}.csv"
                    gcs_uri = upload_to_gcs(csv_path, gcs_path)
                    gcs_uris.append(gcs_uri)
            print(f"Successfully processed all {file_count} from ZIP")

        elapsed = round(time.time() - start_time, 2)
        print(f"✅ Successfully Completed processing in {elapsed} seconds")


    except BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid or corrupt ZIP file.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing files: {str(e)}")

    return JSONResponse(content={
        "status": "success",
        "filename": file.filename,
        "total_files_in_zip": len(file_list),
        "excel_files_converted": len(saved_files),
        "csv_files_saved": saved_files,
        "csv_files_gcs": gcs_uris,
        "message": f"Converted {len(saved_files)} Excel files to CSV, saved locally, and uploaded to GCS."
    })


# """
# VERSION 1.4
# """

# from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
# from fastapi.responses import JSONResponse
# from zipfile import ZipFile, BadZipFile
# from io import BytesIO
# import os
# import pandas as pd
# import time
# from concurrent.futures import ThreadPoolExecutor
# from google.cloud import storage

# app = FastAPI()
# GCS_BUCKET_NAME = "featurebox-ai-uploads"

# def upload_to_gcs_stream(file_obj, destination_blob_name: str):
#     client = storage.Client()
#     bucket = client.bucket(GCS_BUCKET_NAME)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_file(file_obj, rewind=True)
#     return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

# def download_from_gcs(blob_name: str) -> BytesIO:
#     client = storage.Client()
#     bucket = client.bucket(GCS_BUCKET_NAME)
#     blob = bucket.blob(blob_name)
#     data = blob.download_as_bytes()
#     return BytesIO(data)

# def process_and_upload_excel(zip_ref, excel_file):
#     try:
#         with zip_ref.open(excel_file) as excel_fp:
#             df = pd.read_excel(BytesIO(excel_fp.read()))
#             base_name = os.path.splitext(os.path.basename(excel_file))[0]

#             # Convert to CSV in memory
#             csv_buffer = BytesIO()
#             df.to_csv(csv_buffer, index=False)
#             csv_buffer.seek(0)

#             # Upload to GCS
#             gcs_path = f"converted_csvs/{base_name}.csv"
#             upload_to_gcs_stream(csv_buffer, gcs_path)
#             print(f"[✓] Uploaded: {gcs_path}")
#     except Exception as e:
#         print(f"[!] Error processing {excel_file}: {e}")

# def process_zip_from_gcs(blob_name: str):
#     print(f"🚀 Starting processing for: {blob_name}")
#     start_time = time.perf_counter()

#     try:
#         zip_data = download_from_gcs(blob_name)
#         with ZipFile(zip_data) as zip_ref:
#             file_list = [f for f in zip_ref.namelist() if not (f.startswith("__MACOSX/") or f.endswith(".DS_Store"))]
#             excel_files = [f for f in file_list if f.lower().endswith((".xls", ".xlsx"))]
#             total_files = len(excel_files)
#             print(f"📁 Found {total_files} Excel files to process.")

#             with ThreadPoolExecutor(max_workers=8) as executor:
#                 executor.map(lambda f: process_and_upload_excel(zip_ref, f), excel_files)

#             print(f"✅ Completed processing {total_files} files.")
#     except BadZipFile:
#         print("[✘] Invalid or corrupt ZIP file.")
#     except Exception as e:
#         print(f"[✘] Error: {e}")
#     finally:
#         elapsed = time.perf_counter() - start_time
#         print(f"⏱️ Total processing time: {elapsed:.2f} seconds")

# @app.post("/upload/")
# async def upload_zip(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
#     if not file.filename.endswith(".zip"):
#         raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")

#     try:
#         zip_blob_name = f"uploaded_zips/{file.filename}"
#         zip_file_obj = await file.read()
#         zip_stream = BytesIO(zip_file_obj)

#         # Upload original ZIP to GCS
#         upload_to_gcs_stream(zip_stream, zip_blob_name)

#         # Process the file in the background
#         background_tasks.add_task(process_zip_from_gcs, zip_blob_name)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload or processing failed: {str(e)}")

#     return JSONResponse(content={
#         "status": "processing",
#         "filename": file.filename,
#         "message": "ZIP uploaded to GCS. Processing and conversion will continue in the background."
#     })
