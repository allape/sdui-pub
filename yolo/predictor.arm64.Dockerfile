FROM ultralytics/ultralytics:8.3.75-arm64

ADD predictor.py .

EXPOSE 8080

CMD ["python", "predictor.py"]
