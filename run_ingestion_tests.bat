@echo off
cd backend
call .venv\Scripts\activate.bat
python -m pytest tests\test_properties_ingestion.py -v --tb=short -x
