all:	up

image:
	@docker build -t hotel-api-clo5:dev -f ./hotel-api/Dockerfile . 
	@docker build -t reservation-api-clo5:dev -f ./reservation-api/Dockerfile . 
	@docker build -t mailing-api-clo5:dev -f ./mailing-api/Dockerfile . 
	@docker build -t user-api-clo5:dev -f ./user-api/Dockerfile . 
	@docker build -t db-clo5:dev -f ./mysql/Dockerfile .
	@docker build -t traefik-clo5:dev -f ./traefik/Dockerfile . 

build:	image

down:
	@docker-compose stop

clean:
	docker volume rm dbdata

push-dev:
	docker tag db-clo5:dev 172.16.228.22:5000/vignan_q/db:dev
	docker tag traefik-clo5:dev 172.16.228.22:5000/vignan_q/traefik:dev
	docker tag user-api-clo5:dev 172.16.228.22:5000/vignan_q/user-api:dev
	docker tag mailing-api-clo5:dev 172.16.228.22:5000/vignan_q/mailing-api:dev
	docker tag reservation-api-clo5:dev 172.16.228.22:5000/vignan_q/reservation-api:dev
	docker tag hotel-api-clo5:dev 172.16.228.22:5000/vignan_q/hotel-api:dev
	docker push 172.16.228.22:5000/vignan_q/hotel-api:dev
	docker push 172.16.228.22:5000/vignan_q/reservation-api:dev
	docker push 172.16.228.22:5000/vignan_q/mailing-api:dev
	docker push 172.16.228.22:5000/vignan_q/user-api:dev
	docker push 172.16.228.22:5000/vignan_q/traefik:dev
	docker push 172.16.228.22:5000/vignan_q/db:dev

push-latest:
	docker tag db-clo5:dev 172.16.228.22:5000/vignan_q/db:latest
	docker tag traefik-clo5:dev  172.16.228.22:5000/vignan_q/traefik:latest
	docker tag user-api-clo5:dev 172.16.228.22:5000/vignan_q/user-api:latest
	docker tag mailing-api-clo5:dev 172.16.228.22:5000/vignan_q/mailing-api:latest
	docker tag reservation-api-clo5:dev 172.16.228.22:5000/vignan_q/reservation-api:latest
	docker tag hotel-api-clo5:dev 172.16.228.22:5000/vignan_q/hotel-api:latest
	docker push 172.16.228.22:5000/vignan_q/hotel-api:latest
	docker push 172.16.228.22:5000/vignan_q/reservation-api:latest
	docker push 172.16.228.22:5000/vignan_q/mailing-api:latest
	docker push 172.16.228.22:5000/vignan_q/user-api:latest
	docker push 172.16.228.22:5000/vignan_q/traefik:latest
	docker push 172.16.228.22:5000/vignan_q/db:latest
	

up:
	@docker-compose up -d

.PHONY:	all build up clean