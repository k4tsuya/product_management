# Snack Bar Product & Allergen Management API

## 📌 Project Overview

This project started from a **real, practical need** at my current **part-time job** in a snackbar in the Netherlands.

As a food business, we are legally required to:

* Maintain a clear and correct **allergen list**
* Be able to tell customers **which allergens are present in which products**
* Follow EU / NVWA (Nederlandse Voedsel- en Warenautoriteit) food allergen regulations

Managing this information manually quickly became error‑prone and time‑consuming. This project is my attempt to **solve that real-world problem with software**, while at the same time **learning and exploring new backend technologies**.

---

## 🚧 Project Status

This project is **actively under development** and is being built step by step as a learning project.

It is intended to become part of my **developer portfolio**, showcasing how I approach real-world backend problems, data modeling, and new technologies.

---

## 🎯 Goals of This Project

* Model food allergens **correctly and realistically**
* Link allergens to products in a flexible way
* Create a clean and understandable backend foundation
* Learn and practice technologies I have not used deeply before
* Build a meaningful portfolio project based on real business needs

---

## 🧠 Domain Modeling

A key design decision in this project is **how allergens are modeled**.

* Allergens are **not boolean fields** on a product
* Allergens are a **fixed, regulated list** (EU / NVWA)
* Products can contain **multiple allergens**
* One allergen can apply to **multiple products**

Because of this, the project uses a **many‑to‑many relationship** between:

* `Product`
* `Allergen`

This approach:

* Matches real‑world legislation
* Avoids fragile database schemas
* Makes the system easy to extend in the future (e.g. “may contain traces of”)

---

## 🧱 Tech Stack

I intentionally chose this tech stack to **learn and explore different tools** beyond what I already knew.

* **Python 3.13**
* **FastAPI** – modern, fast backend framework
* **SQLAlchemy 2.0** – ORM with explicit, type‑safe models
* **SQLite** – simple local database for development
* **Pydantic** – data validation and API schemas

Although I have previous experience with **Django + DRF**, this project focuses on:

* Understanding lower‑level ORM concepts
* Explicit database modeling
* Clear separation between models, schemas, and application logic


## 🧪 Example Data

The application automatically seeds:

### Allergens (simplified example)

* Gluten
* Milk
* Soy
* Mustard

### Products

* **Frikandel** → gluten, soy, mustard
* **Kroket** → gluten, milk
* **Bread** → gluten

This data is inserted on application startup and is safe to run multiple times.

---

## 🚀 Running the Project

### 1a. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 1b. OPTIONAL: Set the preferred language for the generated pdf file.

Set the `language` variable in the `download_products_pdf()` function (main.py) to `'en'` (English) or `'nl'` (Dutch).

```
language: str = "en"
```


### 2. Start the development server

```bash
uvicorn main:app --reload
```

### 3. Open the API documentation

```
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger documentation.

---

## 🔍 Available Endpoints

* `GET /products` – list products with their allergens
* `GET /allergens` – list all known allergens
* `GET /products/pdf` - generate a downloadable pdf file

---

## 📚 What I Learned From This Project

* How to model **many‑to‑many relationships** correctly
* The difference between **ORM models** and **API schemas**
* How to translate **legal/business requirements** into data models

---

## 🔮 Future Improvements

Planned extensions include:

* Product creation via API (`POST /products`)
* Support for **“may contain traces of”** allergens
* Exportable allergen reports (PDF)

---

📦 Product data source

This project ships with sample product data for demo and development purposes.

By default, the application loads data from an internal sample dataset:

`SAMPLE_PRODUCTS`

Using real product data

If you want to use your own (real) product data, you can provide it via an external module that is intentionally excluded from version control.

Create a file called:

`src/product_management/product_list.py`


Define a variable called products with the same structure as SAMPLE_PRODUCTS:

```python
products = {
    "Example product": ["gluten", "milk"],
    "Another product": ["nuts"],
    }
```


Make sure this file is git-ignored (it is not included in this repository).

When present, the application will automatically load this data instead of the sample data.
If the file is not found, the system safely falls back to the sample dataset.

This approach allows:

- running the project out-of-the-box

- keeping real data private

- avoiding configuration or environment variables for simple setups

---

## 💬 Final Note

This project is part of my **personal learning journey and portfolio** and will continue to evolve over time.

This project is intentionally **practical**.

It represents how I approach backend development:

* Start from real requirements
* Model the domain carefully
* Prefer clarity over complexity
* Learn by building

Feedback and suggestions are always welcome.
