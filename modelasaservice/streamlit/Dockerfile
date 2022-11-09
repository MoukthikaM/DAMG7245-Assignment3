FROM python:3.8.10

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit
RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "ui.py"]
