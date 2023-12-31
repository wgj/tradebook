docker run -d \
	--name tradebook-postgres \
	-e POSTGRES_PASSWORD=password \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v tradebook-pgdata:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres
