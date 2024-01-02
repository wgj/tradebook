docker volume create tradebook-pgdata
docker run -d \
	--name tradebook-postgres \
	-e POSTGRES_PASSWORD=password \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v tradebook-pgdata:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres

docker volume create tradebook-grafana
docker run -d \
	--name tradebook-grafana \
	-v tradebook-grafana:/var/lib/grafana \
	-p 3000:3000 \
	grafana/grafana
