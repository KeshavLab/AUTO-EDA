import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ✅ Use a lightweight model
MODEL_NAME = "google/flan-t5-small"  

# Load model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
except Exception as e:
    print(f"Error loading model: {e}")
    model, tokenizer = None, None

def chatbot_response(user_query, df=None):
    """Generates a chatbot response based on user_query and dataset."""
    if model is None or tokenizer is None:
        return "⚠️ Error: Chatbot model failed to load."
    
    # Check if dataset is provided
    if df is not None:
        num_rows, num_columns = df.shape  
        column_names = ", ".join(df.columns.tolist())
        
        # Handle dataset-related queries
        if "number of columns" in user_query.lower():
            return f"The dataset has {num_columns} columns."
        elif "number of rows" in user_query.lower():
            return f"The dataset has {num_rows} rows."
        elif "column names" in user_query.lower():
            return f"The dataset contains the following columns: {column_names}."
        elif "data type" in user_query.lower():
            col_data_types = df.dtypes.astype(str).to_dict()
            return f"Column data types: {col_data_types}"
        elif "missing values" in user_query.lower():
            missing_counts = df.isnull().sum().to_dict()
            return f"Missing values per column: {missing_counts}"
        elif "unique values" in user_query.lower():
            col_name = user_query.split("unique values in")[-1].strip()
            if col_name in df.columns:
                unique_values = df[col_name].nunique()
                return f"The column '{col_name}' has {unique_values} unique values."
            else:
                return f"⚠️ Column '{col_name}' not found in the dataset."
        else:
            dataset_info = f"Dataset has {num_rows} rows and {num_columns} columns."
    else:
        dataset_info = ""

    # Prepare input prompt
    input_text = f"{dataset_info} {user_query}".strip()

    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=128)

    try:
        output = model.generate(**inputs, max_new_tokens=200)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        response = f"⚠️ Error generating response: {e}"

    return response
