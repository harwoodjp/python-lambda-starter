curl \
	-X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -H "Content-Type: application/json"	\
	-d @bin/request_local_body.json