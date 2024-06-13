# Scene Generation AI

This project consists of two frontends: one using React and another using Streamlit.

## Project Structure
- **Frontend**: Main frontend built with React.
- **Frontend-Test**: Test frontend built with Streamlit.

## Documentation and Frontend URLs
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **React Frontend**: [http://localhost:5173/](http://localhost:5173/)
- **Streamlit Frontend**: [http://localhost:8501](http://localhost:8501)

## Requirements
Before running the project, ensure all requirements are satisfied:

```sh
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --no-cache-dir
pip install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0.0 --no-cache-dir
```
Additionally, Node.js and npm are required.

## Running the Project Locally

### Step 1: Start the Backend
Open a terminal window and run:
```sh
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 2: Start the React Frontend
Open a second terminal window and run:
```sh
cd frontend
npm install
npm run dev
```

### Alternative: Run the Streamlit Frontend
To run the automated pipeline, open a terminal window and run:
```sh
cd frontend-test
streamlit run app.py
```

## Running with Docker

To run the entire app using Docker (GPU support needs to be fixed), use the following commands:
```sh
docker-compose build
docker-compose up
```

