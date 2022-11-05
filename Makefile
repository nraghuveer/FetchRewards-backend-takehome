app:
	python src/main.py
test:
	python src/useraccount_test.py
package:
	pip install -r src/requirements.txt
docker:
	docker build -t raghuveer-backend-takehome:1.0 .
	docker run -it -p 8001:8001 raghuveer-backend-takehome:1.0