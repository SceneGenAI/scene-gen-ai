frontend-test - simple frontend config with streamlit

http://localhost:8000/docs - api documentation

http://localhost:8501 - streamlit frontend


### before running, make sure all requirements are satisfied:
```
pip install -r requirements.txt

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --no-cache-dir
pip install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0.0 --no-cache-dir
```


### to run locally                                                                                              
one window
```
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

second window
```
cd frontend-test
streamlit run app.py
```

### to run the whole app with docker (need to fix gpu support)
```
docker-compose build
docker-compose up
```