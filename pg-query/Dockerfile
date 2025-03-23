FROM quay.io/daniel_casali/pdf_rag_milvus:latest # This is the image generated from ../streamlit/container/Dockerfile
USER 0
RUN /opt/conda/bin/pip install psycopg2-binary
COPY * /work/
USER 1001
EXPOSE 8501
CMD [ "/opt/conda/bin/streamlit" , "run" , "/work/streamlit.py" ]
